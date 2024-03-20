from dataclasses import dataclass, field
from enum import Enum

from shapely import LineString, Point, Polygon  # type: ignore

from arcGisFeatureCache.utils.helpers import clear_temp_data


class EsriGeometryTypeEnum(Enum):
    """
    Enumeration representing Esri geometry types.

    Attributes:
        esriGeometryPoint: esri Point geometry.
        esriGeometryMultipoint: esri Multipoint geometry.
        esriGeometryPolyline: esri Polyline geometry.
        esriGeometryPolygon: esri Polygon geometry.
        esriGeometryEnvelope: esri Envelope geometry.
    """

    esriGeometryPoint = "esriGeometryPoint"
    esriGeometryMultipoint = "esriGeometryMultipoint"
    esriGeometryPolyline = "esriGeometryPolyline"
    esriGeometryPolygon = "esriGeometryPolygon"
    esriGeometryEnvelope = "esriGeometryEnvelope"


@dataclass
class FeatureSpatialReference:
    """
    Dataclass representing the spatial reference of a feature.

    Attributes:
        wkid (str): Well-known ID (WKID) of the spatial reference.
        latest_wkid (str): Latest well-known ID (WKID) of the spatial reference.
    """

    _data: dict | None
    wkid: str = field(init=False)
    latest_wkid: str = field(init=False)

    def __post_init__(self):
        if not hasattr(self, "wkid"):
            self.wkid = self._data["wkid"]

        if not hasattr(self, "latestWkid"):
            self.latest_wkid = self._data["latestWkid"]

        clear_temp_data(self)


async def parse_point(geometry_value: dict) -> Point:
    """
    Asynchronously parse a point geometry.

    Parameters:
        geometry_value (Dict): Dictionary containing point geometry data.

    Returns:
        Point: Shapely Point object representing the parsed point geometry.
    """
    # TODO: implement 3d
    if geometry_value == "":
        return Point()
    return Point(geometry_value["x"], geometry_value["y"])


async def parse_line(geometry_value: dict) -> LineString:
    """
    Asynchronously parse a line geometry.

    Parameters:
        geometry_value (Dict): Dictionary containing line geometry data.

    Returns:
        LineString: Shapely LineString object representing the parsed line geometry.
    """
    if geometry_value == {} or (
        "paths" in geometry_value and len(geometry_value["paths"]) == 0
    ):
        return LineString()
    elif "hasZ" in geometry_value.keys() and geometry_value["hasZ"]:
        return LineString(
            [[item[0], item[1], item[2]] for item in geometry_value["paths"][0]]
        )
    else:
        return LineString(geometry_value["paths"][0])


async def parse_polygon(geometry_value: dict) -> Polygon:
    """
    Asynchronously parse a polygon geometry.

    Parameters:
        geometry_value (Dict): Dictionary containing polygon geometry data.

    Returns:
        Polygon: Shapely Polygon object representing the parsed polygon geometry.
    """
    # TODO: implement 3d and inner outer stuff
    if geometry_value == {}:
        return Polygon()
    return Polygon(geometry_value["rings"][0])
