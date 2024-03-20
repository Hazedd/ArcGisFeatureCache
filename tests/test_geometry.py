import pytest
from shapely.geometry import LineString, Point, Polygon

from arcGisFeatureCache.models.geometry import (
    FeatureSpatialReference,
    parse_line,
    parse_point,
    parse_polygon,
)


@pytest.mark.asyncio
async def test_parse_point():
    geometry_value = {"x": 1, "y": 2}
    expected_point = Point(1, 2)
    assert await parse_point(geometry_value) == expected_point


@pytest.mark.asyncio
async def test_parse_point_empty_geometry():
    # Testing empty geometry
    assert await parse_point("") == Point()


@pytest.mark.asyncio
async def test_parse_line():
    geometry_value = {"paths": [[[1, 2], [3, 4]]]}
    expected_line = LineString([(1, 2), (3, 4)])
    assert await parse_line(geometry_value) == expected_line


@pytest.mark.asyncio
async def test_parse_line_empty_geometry():
    # Testing empty geometry
    assert await parse_line({}) == LineString()

    # Testing empty paths
    geometry_value_empty_paths = {"paths": []}
    assert await parse_line(geometry_value_empty_paths) == LineString()


@pytest.mark.asyncio
async def test_parse_line_has_z():
    geometry_value_with_z = {"paths": [[[1, 2, 3], [4, 5, 6]]], "hasZ": True}
    expected_line_with_z = LineString([(1, 2, 3), (4, 5, 6)])
    assert await parse_line(geometry_value_with_z) == expected_line_with_z


@pytest.mark.asyncio
async def test_parse_polygon():
    geometry_value = {"rings": [[[1, 2], [3, 4], [5, 6], [1, 2]]]}
    expected_polygon = Polygon([(1, 2), (3, 4), (5, 6), (1, 2)])
    assert await parse_polygon(geometry_value) == expected_polygon


@pytest.mark.asyncio
async def test_parse_polygon_empty_geometry():
    # Testing empty geometry
    assert await parse_polygon({}) == Polygon()

    # Testing empty rings
    geometry_value_empty_rings = {"rings": [[]]}
    assert await parse_polygon(geometry_value_empty_rings) == Polygon()


def test_feature_spatial_reference():
    data = {"wkid": "4326", "latestWkid": "4326"}
    spatial_ref = FeatureSpatialReference(data)
    assert spatial_ref.wkid == "4326"
    assert spatial_ref.latest_wkid == "4326"
