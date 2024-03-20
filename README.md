
<p align="center">
   <em><h1>ArcGisFeatureCache</h1></em>
</p>

[![build](https://github.com/Hazedd/ArcGisFeatureCache/workflows/Build/badge.svg)](https://github.com/Hazedd/ArcGisFeatureCache/actions)
[![codecov](https://codecov.io/gh/Hazedd/ArcGisFeatureCache/branch/master/graph/badge.svg)](https://codecov.io/gh/Hazedd/ArcGisFeatureCache)
[![PyPI version](https://badge.fury.io/py/ArcGisFeatureCache.svg)](https://badge.fury.io/py/ArcGisFeatureCache)

The ArcGIS Feature Layer Caching Library is a Python library designed to cache ArcGIS feature layers locally, enabling faster data access and improved performance for applications that frequently access the same data from an ArcGIS server. By storing data locally, this library reduces server load, conserves bandwidth, and allows for offline access to ArcGIS feature layers.

---

**Documentation**: <a href="https://Hazedd.github.io/ArcGisFeatureCache/" target="_blank">https://Hazedd.github.io/Hazedd/ArcGisFeatureCache/</a>

**Source Code**: <a href="https://github.com/Hazedd/ArcGisFeatureCache" target="_blank">https://github.com/Hazedd/ArcGisFeatureCache</a>

---

## Install

```batch
pip install arcGisFeatureCache
```

## Usage

```py
from arcGisFeatureCache import get_feature_service

url = "https://xxxx.xxx/arcgis/rest/services/xxxxxx/FeatureServer"
feature_service = get_feature_service(url)

# get all features from service
feature_service.get_all_features()

# get features from one or more layers
feature_service.get_layer_features(["layer_a", "layer_b"])

```

### async
```py
from arcGisFeatureCache import ArcGisFeatureService

url = "https://xxxx.xxx/arcgis/rest/services/xxxxxx/FeatureServer"
feature_service = await ArcGisFeatureService.factory(url)

```


## Roadmap:

- [X] pr and github actions setup
- [X] docs as website
- [X] init release 0.1.0
- [ ] 100% code coverage
- [ ] query by intersect geometry (rtree)
- [ ] query by attribute
- [ ] make pickle work so we can safe and load state


## Contributing
Contributions to the ArcGIS Feature Layer Caching Library are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.


## License
This project is licensed under the terms of the MIT license.
