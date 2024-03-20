import asyncio
import json
import math
import ssl

import httpx
from httpx import Limits

from arcGisFeatureCache.utils.log import logger

# seems arcgis feature service usages LEGACY_RENEGOTIATION, its a thing on 3.11 and above
CUSTOM_SSL_CONTEXT = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
CUSTOM_SSL_CONTEXT.options |= (
    0x00040000  # OP flag SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
)
CUSTOM_SSL_CONTEXT.check_hostname = False
CUSTOM_SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class ArcGisScraper:
    """A class for scraping data from ArcGIS Feature Services.

    Attributes:
        feature_service_info: Information about the feature service.
        feature_layers: List of feature layers.
        layer_info: Information about individual layers.

    """

    def __init__(
        self,
        feature_service_url: str,
        _max_connections: int = 5,
        _max_keepalive_connections: int = 5,
    ):
        self._base_url = feature_service_url
        self.feature_service_info: dict | None = None
        self.feature_layers: list[dict] | None = None
        self._limits = Limits(
            max_connections=_max_connections,
            max_keepalive_connections=_max_keepalive_connections,
        )
        self._transport = httpx.HTTPTransport(retries=1)
        self.layer_info: dict = {}

    @classmethod
    async def factory(cls, url):
        """
        Create an ArcGisScraper instance.

        Parameters:
            url: The URL of the ArcGIS Feature Service.

        Returns:
            An instance of ArcGisScraper.

        Raises:
            ValueError: If the URL is invalid.
        """
        self = ArcGisScraper(url, 100, 20)
        await self._process_all_layers()
        return self

    async def _fetch(self, url: str) -> dict:
        """
        Asynchronously fetch data from the specified URL.

        Parameters:
            url: The URL to fetch data from.

        Returns:
            The fetched data.

        Raises:
            ValueError: If the response cannot be parsed as JSON.
        """
        async with httpx.AsyncClient(
            timeout=None, limits=self._limits, verify=CUSTOM_SSL_CONTEXT
        ) as client:
            success = False
            while not success:
                try:
                    r = await client.get(url)
                    logger.info(f"fetched data, status {r.status_code}: {url}")
                    response = json.loads(r.text)
                    if isinstance(response, dict):
                        return response
                    raise ValueError(f"Can bake json from response {url}")  # noqa: TRY003, TRY301
                except Exception as e:
                    logger.debug(f"error: {e}")
                    await asyncio.sleep(3)
        raise ValueError(f"cant fetch data {url}")  # noqa: TRY003

    async def _get_json_data_async(self, url: str) -> dict:
        """
        Asynchronously fetch JSON data from the specified URL.

        Parameters:
            url: The URL to fetch JSON data from.

        Returns:
            The fetched JSON data.
        """
        retry_seconds = 60
        json_data = await self._fetch(url)
        if "error" in json_data.keys():
            success = False
            while not success:
                logger.error(f"fetched data got error: {url}")
                logger.info(f"retry in {retry_seconds} seconds")
                await asyncio.sleep(retry_seconds)
                json_data = await self._fetch(url)
                if "error" not in json_data.keys():
                    success = True

        return json_data

    async def _get_all_data_async(
        self, base_url: str, feature_offset: int = 2000
    ) -> dict:
        """
        Asynchronously fetch all data from the feature service.

        Parameters:
            base_url: The base URL of the feature service.
            feature_offset: Offset for fetching features.

        Returns:
            All fetched data.
        """
        self.layer_info = await self._get_json_data_async(base_url + "?f=pjson")

        # get all data
        feature_service_url = (
            base_url + "/query?returnZ=true&returnM=true&f=json&outfields=*&where=1%3D1"
        )
        count_response = await self._get_json_data_async(
            feature_service_url + "&returnCountOnly=true"
        )

        # create batches
        feature_total_count = count_response["count"]
        if feature_total_count == 0:
            return {
                "dataset": base_url,
                "features": [],
                "geometryType": self.layer_info["geometryType"],
                "fields": self.layer_info["fields"],
                "objectIdFieldName": self.layer_info["objectIdField"],
                "globalIdFieldName": self.layer_info["globalIdField"],
                "spatialReference": {"latestWkid": None, "wkid": None},
            }

        batch_count = math.ceil(feature_total_count / feature_offset)
        batch_list = []
        offset = 0
        for n in range(batch_count):
            batch_list.append(feature_service_url + f"&resultOffset={offset}")
            offset += feature_offset

        # create and await all task
        tasks = [self._get_json_data_async(url) for url in batch_list]
        feature_data = await asyncio.gather(*tasks)

        logger.debug(f"Merging data {base_url}")

        features: list[dict] = sum([item["features"] for item in feature_data], [])

        feature_data[0]["features"] = features
        logger.debug(f"Done merging data {base_url}")

        # TODO: make succeeded check on feature count
        feature_data[0]["dataset"] = base_url
        if isinstance(feature_data[0], dict):
            return feature_data[0]
        else:
            raise ValueError("")  # noqa: TRY004

    async def _get_layer_data(self, feature_service_layer_url: str) -> dict:
        """
        Asynchronously fetch data for a specific layer.

        Parameters:
            feature_service_layer_url: The URL of the layer.

        Returns:
            Data for the layer.
        """
        return await self._get_all_data_async(feature_service_layer_url)

    async def _process_all_layers(self):
        """
        Asynchronously process all layers of the feature service.
        """
        self.feature_service_info = await self._get_json_data_async(
            self._base_url + "?f=pjson"
        )
        batch_list = [
            f"{self._base_url}/{item['id']}"
            for item in self.feature_service_info["layers"]
        ]
        tasks = [self._get_layer_data(url) for url in batch_list]
        feature_data = await asyncio.gather(*tasks)
        self.feature_layers = feature_data
