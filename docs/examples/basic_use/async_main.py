import asyncio

from arcGisFeatureCache import ArcGisFeatureService


async def main():
    url = "https://maps.prorail.nl/arcgis/rest/services/Tekeningen_schematisch/FeatureServer"
    feature_service = await ArcGisFeatureService.factory(url)

    # get all features from service
    all_features = feature_service.get_all_features()
    first_feature = all_features[0]

    # get the layer name
    print(first_feature.dataset)

    # we use shapley for geometry 😊
    print(first_feature.geometry)

    # dynamic attributes
    print(first_feature.attributes)

    # get them by field
    fields = first_feature.attributes.get_all_fields()
    for field in fields:
        print(f"{field}: {first_feature.attributes.get_value(field)}")

    # get features from one or more layers
    layer_features = feature_service.get_layer_features(["OBE blad"])
    print(layer_features[-1].dataset)


if __name__ == "__main__":
    asyncio.run(main())
