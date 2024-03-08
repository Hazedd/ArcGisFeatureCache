
<p align="center">
   <em><h1>ArcGisFeatureCache</h1></em>
</p>

[![build](https://github.com/Hazedd/ArcGisFeatureCache/workflows/Build/badge.svg)](https://github.com/Hazedd/ArcGisFeatureCache/actions)
[![codecov](https://codecov.io/gh/Hazedd/ArcGisFeatureCache/branch/master/graph/badge.svg)](https://codecov.io/gh/Hazedd/ArcGisFeatureCache)
[![PyPI version](https://badge.fury.io/py/ArcGisFeatureCache.svg)](https://badge.fury.io/py/ArcGisFeatureCache)

The ArcGIS Feature Layer Caching Library is a Python library designed to cache ArcGIS feature layers locally, enabling faster data access and improved performance for applications that frequently access the same data from an ArcGIS server. By storing data locally, this library reduces server load, conserves bandwidth, and allows for offline access to ArcGIS feature layers.

---

**Documentation**: <a href="https://Hazedd.github.io/ArcGisFeatureCache/" target="_blank">https://Hazedd.github.io/ArcGisFeatureCache/</a>

**Source Code**: <a href="https://github.com/Hazedd/ArcGisFeatureCache" target="_blank">https://github.com/Hazedd/ArcGisFeatureCache</a>

---

## Install

```batch
pip install arcGisFeatureCache
```

## Usage

```py
import asyncio
from arcGisFeatureCache import ArcGisFeatureService, get_feature_service

url = "https://xxxx.xxx/arcgis/rest/services/xxxxxx/FeatureServer"

if async:
    feature_service_instance = await ArcGisFeatureService.factory(url)
else:
    feature_service_instance = get_feature_service(url)


# get all features from service
feature_service_instance.get_all_features()

# get features from one or more layers
feature_service_instance.get_layer_features(["layer_a", "layer_b"])




```

## Roadmap:

- [X] pr and github actions setup
- [X] docs as website
- [ ] init release
- [ ] 100% code coverage
- [ ] ....


## Contributing
Contributions to the ArcGIS Feature Layer Caching Library are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.


##


thx frankie for coociecutter hipster stuff
https://github.com/frankie567/cookiecutter-hipster-pypackage


## License

This project is licensed under the terms of the MIT license.
