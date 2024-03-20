from datetime import datetime

import pytest

from arcGisFeatureCache.models.attributes import (
    EsriFieldTypeEnum,
    FeatureAttribute,
    FeatureAttributes,
    FeatureField,
    FeatureFields,
    parse_date,
)


@pytest.fixture
def sample_feature_field_data():
    return {
        "name": "field_name",
        "alias": "Field Alias",
        "type": EsriFieldTypeEnum.esriFieldTypeString.value,
        "length": 50,
    }


@pytest.fixture
def sample_feature_attribute_data():
    return {"attr1": "value1", "attr2": "value2", "attr3": "value3"}


@pytest.fixture
def sample_feature_fields(sample_feature_field_data):
    return FeatureFields([sample_feature_field_data])


@pytest.fixture
def sample_feature_attributes(sample_feature_attribute_data):
    return FeatureAttributes(sample_feature_attribute_data)


def test_feature_field_init(sample_feature_field_data):
    field = FeatureField(sample_feature_field_data)
    assert field.name == sample_feature_field_data["name"]
    assert field.alias == sample_feature_field_data["alias"]
    assert field.type == EsriFieldTypeEnum.esriFieldTypeString
    assert field.length == sample_feature_field_data["length"]


def test_feature_fields_get_date_fields(sample_feature_fields):
    date_field = {
        "name": "date_field",
        "alias": "Date Field",
        "type": EsriFieldTypeEnum.esriFieldTypeDate.value,
    }
    sample_feature_fields._items.append(FeatureField(date_field))
    date_fields = sample_feature_fields.get_date_fields()
    assert len(date_fields) == 1
    assert date_fields[0].name == "date_field"
    assert date_fields[0].type == EsriFieldTypeEnum.esriFieldTypeDate


def test_feature_attribute_set_attribute(sample_feature_attributes):
    field = FeatureField(
        {
            "name": "attr1",
            "type": EsriFieldTypeEnum.esriFieldTypeString.value,
            "alias": "",
        }
    )
    sample_feature_attributes.set_attribute(field, lambda x: x.upper())
    assert sample_feature_attributes[0].value == "VALUE1"


def test_feature_attributes_get_all_fields(sample_feature_attributes):
    fields = sample_feature_attributes.get_all_fields()
    assert len(fields) == 3
    assert "attr1" in fields
    assert "attr2" in fields
    assert "attr3" in fields


def test_parse_date():
    timestamp = 1616198400000  # March 20, 2021
    expected_date = datetime(2021, 3, 20)
    parsed_date = parse_date(timestamp)
    assert parsed_date == expected_date


def test_feature_attribute_get_value(sample_feature_attributes):
    value = sample_feature_attributes.get_value("attr1")
    assert value == "value1"


def test_feature_attribute_get_value_nonexistent_key(sample_feature_attributes):
    value = sample_feature_attributes.get_value("nonexistent_key")
    assert value is None


def test_feature_attribute_get_value_duplicate_key(sample_feature_attributes):
    sample_feature_attributes._items.append(FeatureAttribute("attr1", "value2"))
    with pytest.raises(Exception):
        sample_feature_attributes.get_value("attr1")


def test_feature_attribute_len(sample_feature_attributes):
    assert len(sample_feature_attributes) == 3


def test_feature_attribute_delitem_not_allowed(sample_feature_attributes):
    with pytest.raises(NotImplementedError):
        del sample_feature_attributes[0]


def test_feature_attribute_setitem_not_allowed(sample_feature_attributes):
    with pytest.raises(NotImplementedError):
        sample_feature_attributes[0] = FeatureAttribute("attr", "value")


def test_feature_attribute_repr(sample_feature_attributes):
    expected_repr = "[attr1=value1, attr2=value2, attr3=value3]"
    assert repr(sample_feature_attributes) == expected_repr


def test_feature_fields_get_item_by_index(sample_feature_fields):
    field = sample_feature_fields[0]
    assert field.name == "field_name"
    assert field.alias == "Field Alias"
    assert field.type == EsriFieldTypeEnum.esriFieldTypeString
    assert field.length == 50


def test_feature_fields_get_item_by_slice(sample_feature_fields):
    fields = sample_feature_fields[:]
    assert len(fields) == 1
    assert fields[0].name == "field_name"
    assert fields[0].alias == "Field Alias"
    assert fields[0].type == EsriFieldTypeEnum.esriFieldTypeString
    assert fields[0].length == 50


def test_feature_fields_iter(sample_feature_fields):
    fields = [field for field in sample_feature_fields]
    assert len(fields) == 1
    assert fields[0].name == "field_name"
    assert fields[0].alias == "Field Alias"
    assert fields[0].type == EsriFieldTypeEnum.esriFieldTypeString
    assert fields[0].length == 50
