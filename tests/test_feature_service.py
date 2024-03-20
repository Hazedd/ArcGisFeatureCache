import asyncio

import pytest

from arcGisFeatureCache import ArcGisFeatureService

feature_service_instance_km = asyncio.run(
    ArcGisFeatureService.factory(
        "https://mapservices.prorail.nl/arcgis/rest/services/Referentiesysteem_004/FeatureServer"
    )
)


@pytest.mark.parametrize(
    "feature_service_instance,feature_layer,layers_count,layer_name",
    [
        (
            feature_service_instance_km,
            "Referentiesysteem_004",
            9,
            "Koppelpunt kilometerlint",
        ),
    ],
)
@pytest.mark.asyncio
async def test_feature_service_layers(
    feature_service_instance: ArcGisFeatureService,
    feature_layer: str,
    layers_count: int,
    layer_name: str,
):
    assert len(feature_service_instance.feature_service_layers) == layers_count
    assert feature_service_instance.name == feature_layer

    layer_features = feature_service_instance.get_layer_features([layer_name])
    assert layer_features[0].dataset == layer_name
    assert layer_features[-1].dataset == layer_name


@pytest.mark.parametrize(
    "feature_service_instance",
    [
        feature_service_instance_km,
    ],
)
def test_feature_service(feature_service_instance: ArcGisFeatureService):
    all_layers = [_.dataset for _ in feature_service_instance.feature_service_layers]
    for layer_name in all_layers:
        first_item = feature_service_instance.get_all_features([layer_name])[0]
        last_item = feature_service_instance.get_all_features([layer_name])[-1]
        assert first_item.dataset == layer_name
        assert last_item.dataset == layer_name
        for feature in [
            _
            for _ in feature_service_instance.feature_service_layers
            if _.dataset == layer_name
        ][0].features:
            assert feature.dataset == layer_name
            # TODO: check if line point polygon or else
            assert feature.geometry is not None
            all_fields = feature.attributes.get_all_fields()
            for field in all_fields:
                assert feature.attributes.get_value(field) is not any
