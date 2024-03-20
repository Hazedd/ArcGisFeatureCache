import asyncio

import numpy as np
from numpy.typing import NDArray
from shapely import STRtree  # type: ignore

from arcGisFeatureCache.arcGisScraper import ArcGisScraper
from arcGisFeatureCache.featureLayer import ArcGisFeatureLayer
from arcGisFeatureCache.models.feature import Feature


class ArcGisFeatureService:
    """A class representing an ArcGIS Feature Service.

    Attributes:
        name (str): The name of the feature service extracted from the URL.
        feature_service_layers (List[ArcGisFeatureLayer]): List of layers in the feature service.

    """

    def __init__(self, feature_service_url: str):
        self._base_url: str = feature_service_url
        self.name: str = feature_service_url.split(r"/")[-2]
        self.feature_service_layers: list[ArcGisFeatureLayer] = []
        self._tree: STRtree = STRtree([])
        self._tree_keys: NDArray = np.array([])

    @classmethod
    async def factory(cls, url) -> "ArcGisFeatureService":
        """
        Create an ArcGisFeatureService instance.

        Parameters:
            url: The URL of the ArcGIS Feature Service.

        Returns:
            An instance of ArcGisFeatureService.
        """
        self = ArcGisFeatureService(url)
        arc_gis_scraper = await ArcGisScraper.factory(url)
        layer_legenda = {
            f"{item['id']}": item["name"]
            for item in arc_gis_scraper.feature_service_info["layers"]
        }

        # TODO: get layer name here so we allso can use it when no feature returns (returns count=0)

        tasks = [
            ArcGisFeatureLayer.factory(item, layer_legenda)
            for item in arc_gis_scraper.feature_layers
        ]
        self.feature_service_layers = await asyncio.gather(*tasks)
        records = [
            {"geometry": item.geometry, "key": item.uuid}
            for layer in self.feature_service_layers
            for item in layer.features
        ]

        self._tree = STRtree([record["geometry"] for record in records])
        self._tree_keys = np.array([record["key"] for record in records])

        return self

    def get_all_features(self, feature_layer: list[str] | None = None) -> list[Feature]:
        """
        Get all features from the feature service.

        Parameters:
            feature_layer List of layer names to filter features (default: None).

        Returns:
            List of all features.
        """
        out_list = []
        for item in self.feature_service_layers:
            if feature_layer:
                out_list.extend(
                    [item2 for item2 in item.features if item2.dataset in feature_layer]
                )
            else:
                out_list.extend([item2 for item2 in item.features])
        return out_list

    def get_all_datasets(self) -> list[str]:
        """
        Retrieve a list of all datasets present..

        Returns:
            list[str]: A list containing the dataset names of all feature service layers.
        """
        return [_.dataset for _ in self.feature_service_layers]

    def get_layer_features(self, layers: list[str]) -> list[Feature]:
        """
        Get all features of a or some by dataset name(s).

        Parameters:
            layers: List of UUIDs to search for.

        Returns:
            List of features with matching dataset names.

        """
        out_list = []
        for item in self.feature_service_layers:
            out_list.extend([_ for _ in item.features if _.dataset in layers])
        return out_list

    # def get_features_in_box(
    #     self, bbox: box, layers: list[str] | None = None
    # ) -> list[Feature]:
    #     if layers is None:
    #         layers = []
    #     """
    #     Get features within a bounding box.
    #
    #     Parameters:
    #         bbox: The bounding box (Shapely box object).
    #         layers: layers to query
    #
    #     Returns:
    #         List of features within the bounding box.
    #
    #     """
    #     query = self._tree.query(bbox)
    #     keys = self._tree_keys.take(query).tolist()
    #     return self.get_layer_features(keys)

    # def get_features_matching_field_value(
    #     self,
    #     field: FeatureAttribute,
    #     value: Any,
    #     feature_layer: Optional[List[str]] = None,
    # ):
    #     # TODO: attribute query on layer
    #     out_list = []
    #     for item in self.feature_service_layers:
    #         pass
    #     return out_list


def get_feature_service(url: str) -> ArcGisFeatureService:
    return asyncio.run(ArcGisFeatureService.factory(url))
