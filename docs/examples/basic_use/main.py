import asyncio

from arcGisFeatureCache import ArcGisFeatureService

feature_service_instance = asyncio.run(
    ArcGisFeatureService.factory(
        "https://xxxx.xxx/arcgis/rest/services/xxxxxx/FeatureServer"
    )
)

# get all features from service
feature_service_instance.get_all_features()

# get features from one or more layers
feature_service_instance.get_layer_features(["layer_a", "layer_b"])
