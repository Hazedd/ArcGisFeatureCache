import asyncio
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import SupportsIndex, overload

from shapely import LineString, Point, Polygon  # type: ignore

from arcGisFeatureCache.models.attributes import FeatureAttributes, FeatureField
from arcGisFeatureCache.models.geometry import (
    EsriGeometryTypeEnum,
    parse_line,
    parse_point,
    parse_polygon,
)
from arcGisFeatureCache.utils.helpers import clear_temp_data


@dataclass
class Feature:
    """A class representing a feature in an ArcGIS feature service.

    Generates a UUID for the feature and initializes its attributes.

    """

    _data: dict | None

    attributes: FeatureAttributes = field(init=False)
    geometry: Point | LineString | Polygon = field(init=False)
    uuid: str = field(init=False)
    dataset: str | None = field(init=False)
    measure_geometry: LineString | None = field(default=None)

    def __post_init__(self) -> None:
        self.uuid = str(uuid.uuid4())
        if self._data is not None and "attributes" in self._data.keys():
            self.attributes = FeatureAttributes(self._data["attributes"])

    def __repr__(self) -> str:
        return f"<Feature {self.attributes.__dict__}>"

    async def set_geometry(self, function: Callable) -> None:
        """
        Set the geometry of the feature.

        Parameters:
            function (Callable): The function to parse and set the geometry.
        """
        if self._data is not None:
            self.geometry = await function(self._data["geometry"])

    async def set_m_values(self) -> None:
        """
        Set M values for the feature's geometry.
        """
        if self._data is not None:
            geometry_data = self._data["geometry"]
        else:
            geometry_data = []

        if (
            "hasM" in geometry_data
            and geometry_data["hasM"]
            and len(geometry_data["paths"]) != 0
        ):
            if "hasZ" in geometry_data and geometry_data["hasZ"]:
                self.measure_geometry = LineString(
                    [[item[0], item[2], item[3]] for item in geometry_data["paths"][0]]
                )
            else:
                self.measure_geometry = LineString(
                    [[item[0], item[1], item[2]] for item in geometry_data["paths"][0]]
                )

    async def clean_data(self) -> None:
        """Asynchronously clean temporary data."""

        clear_temp_data(self)


@dataclass
class Features(list):
    """A class representing a collection of features.

    Converts input data to a list of Feature instances.
    """

    _data: dict | None
    _items: list[Feature] = field(init=False)

    def __post_init__(self) -> None:
        if self._data is not None:
            self._items = [Feature(_) for _ in self._data]
        clear_temp_data(self)

    def __iter__(self) -> Iterator[Feature]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> Feature: ...

    @overload
    def __getitem__(self, idx: slice) -> list[Feature]: ...

    def __getitem__(self, idx: SupportsIndex | slice) -> Feature | list[Feature]:
        """Get a feature by index or slice."""

        return self._items[idx]

    def __repr__(self) -> str:
        return str(self._items)

    def _set_value(self, field_list: list[FeatureField], function: Callable) -> None:
        """
        Set values for specific fields in the feature attributes.

        Parameters:
            field_list (List[FeatureField]): List of fields to set values for.
            function (Callable): The function to apply to the attribute values.
        """
        for feature in self._items:
            for field_item in field_list:
                feature.attributes.set_attribute(field_item, function)

    async def set_geometry(self, geometry_type: EsriGeometryTypeEnum) -> None:
        """
        Set the geometry for all features.

        Parameters:
            geometry_type (EsriGeometryTypeEnum): The type of geometry to parse.
        """
        match geometry_type:
            case EsriGeometryTypeEnum.esriGeometryPoint:
                function = parse_point
            case EsriGeometryTypeEnum.esriGeometryPolyline:
                function = parse_line
            case EsriGeometryTypeEnum.esriGeometryPolygon:
                function = parse_polygon
            case _:
                raise NotImplementedError

        tasks = [feature.set_geometry(function) for feature in self._items]
        await asyncio.gather(*tasks)

    async def set_measure(self) -> None:
        """
        Set M values for all features.
        """
        tasks = [feature.set_m_values() for feature in self._items]
        await asyncio.gather(*tasks)

    async def clean_data(self) -> None:
        """
        Clean temporary data for all features.
        """
        tasks = [feature.clean_data() for feature in self._items]
        await asyncio.gather(*tasks)
