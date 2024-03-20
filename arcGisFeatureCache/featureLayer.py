from dataclasses import dataclass, field

from arcGisFeatureCache.models.attributes import FeatureFields, parse_date
from arcGisFeatureCache.models.feature import Features
from arcGisFeatureCache.models.geometry import (
    EsriGeometryTypeEnum,
    FeatureSpatialReference,
)
from arcGisFeatureCache.utils.helpers import clear_temp_data
from arcGisFeatureCache.utils.log import logger


@dataclass
class ArcGisFeatureLayer:
    """A class representing a layer in an ArcGIS Feature Service.

    Sets attributes based on input data.
    """

    _data: dict

    object_id_field_name: str = field(init=False, default="")
    global_id_field_name: str = field(init=False, default="")
    geometry_type: EsriGeometryTypeEnum = field(init=False)
    spatial_reference: FeatureSpatialReference = field(init=False)
    fields: FeatureFields = field(init=False)
    features: Features = field(init=False)
    dataset: str = field(init=False, default="")
    has_m: bool = False

    def __post_init__(self):
        self.object_id_field_name = self._data["objectIdFieldName"]
        self.global_id_field_name = self._data["globalIdFieldName"]
        self.geometry_type = EsriGeometryTypeEnum[self._data["geometryType"]]
        self.spatial_reference = FeatureSpatialReference(self._data["spatialReference"])
        self.fields = FeatureFields(self._data["fields"])
        self.features = Features(self._data["features"])
        self.dataset = self._data["dataset"].split(r"/")[-1]

        clear_temp_data(self)

    async def _set_dataset_name(self, layer_legenda: dict) -> None:
        """
        sets the layer name based on a legend.

        Parameters:
            layer_legenda: A dictionary containing the legend for layer names.
        """
        self.dataset = layer_legenda[self.dataset]
        for item in self.features:
            item.dataset = self.dataset

    async def _process_dates(self) -> None:
        """
        processes date fields in features.
        """
        self.features._set_value(self.fields.get_date_fields(), parse_date)

    async def _process_geometry(self) -> None:
        """
        Processes geometry in features.
        """
        await self.features.set_geometry(self.geometry_type)
        await self.features.set_measure()
        await self.features.clean_data()

    @classmethod
    async def factory(cls, _data: dict, layer_legenda: dict) -> "ArcGisFeatureLayer":
        """
        Creates an ArcGisFeatureServiceLayer instance.

        Parameters:
            _data: Data for creating the layer.
            layer_legenda: Legend for layer names.

        Returns:
            An instance of ArcGisFeatureServiceLayer.
        """
        self = ArcGisFeatureLayer(_data)
        dataset_name = layer_legenda[_data["dataset"].split("/")[-1]]

        logger.debug(f"Processing new Feature Layer: {dataset_name}")
        await self._set_dataset_name(layer_legenda)
        await self._process_dates()
        await self._process_geometry()
        if len(self.features) != 0:
            self.has_m = False
        else:
            self.has_m = (
                True if self.features[0].measure_geometry is not None else False
            )

        logger.debug(f"Done, created dataset: {dataset_name}")

        return self

    def get_all_features(self) -> Features:
        """
        Get all features from the dataset.

        Returns:
            All features in the layer.
        """
        return self.features
