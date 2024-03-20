from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, SupportsIndex, overload

from arcGisFeatureCache.utils.helpers import clear_temp_data
from arcGisFeatureCache.utils.immutableList import ImmutableList


class EsriFieldTypeEnum(Enum):
    """An enumeration representing Esri field types.

    Attributes:
        esriFieldTypeOID: esriFieldTypeOID
        esriFieldTypeString: esriFieldTypeString
        esriFieldTypeInteger: esriFieldTypeInteger
        esriFieldTypeSmallInteger: esriFieldTypeSmallInteger
        esriFieldTypeDouble: esriFieldTypeDouble
        esriFieldTypeDate: esriFieldTypeDate
        esriFieldTypeGeometry: esriFieldTypeGeometry
        esriFieldTypeBlob: esriFieldTypeBlob
    """

    esriFieldTypeOID = "esriFieldTypeOID"
    esriFieldTypeString = "esriFieldTypeString"
    esriFieldTypeInteger = "esriFieldTypeInteger"
    esriFieldTypeSmallInteger = "esriFieldTypeSmallInteger"
    esriFieldTypeDouble = "esriFieldTypeDouble"
    esriFieldTypeDate = "esriFieldTypeDate"
    esriFieldTypeGeometry = "esriFieldTypeGeometry"
    esriFieldTypeBlob = "esriFieldTypeBlob"


@dataclass
class FeatureField:
    """A class representing a field in a feature."

    Parameters:
        name (str): Name of the field.
        alias:(str): Alias name of the field.
        type :(EsriFieldTypeEnum)
        length: Length of the Field.
    """

    _data: dict[str, Any] | None

    name: str = field(init=False)
    alias: str = field(init=False)
    type: EsriFieldTypeEnum = field(init=False)
    length: int | None = field(init=False)

    def __post_init__(self) -> None:
        if self._data is not None:
            if self._data["name"] is not None:
                self.name = self._data["name"]
            self.name = self._data["name"]
            self.alias = self._data["alias"]
            self.type = EsriFieldTypeEnum[self._data["type"]]
            if "length" in self._data.keys():
                self.length = self._data["length"]
            else:
                self.length = None

        clear_temp_data(self)


@dataclass
class FeatureFields(ImmutableList):
    """A class representing a list of feature fields.

    Converts input data to a list of FeatureField instances.
    """

    _data: list | None
    _items: list[FeatureField] = field(init=False)

    def __post_init__(self) -> None:
        if self._data is not None and isinstance(self._data, list):
            self._items = [FeatureField(item) for item in self._data]
        else:
            self._items = []

        clear_temp_data(self)

    def __iter__(self) -> Iterator[FeatureField]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> FeatureField: ...

    @overload
    def __getitem__(self, idx: slice) -> list[FeatureField]: ...

    def __getitem__(
        self, idx: SupportsIndex | slice
    ) -> FeatureField | list[FeatureField]:
        """Get a feature field by index or slice."""
        return self._items[idx]

    def get_date_fields(self) -> list[FeatureField]:
        """
        Get fields of type 'date'.

        Returns:
            List[FeatureField]: List of fields of type 'esriFieldTypeDate'.
        """
        return [
            item
            for item in self._items
            if item.type == EsriFieldTypeEnum.esriFieldTypeDate
        ]


@dataclass
class FeatureAttribute:
    """A class representing an attribute of a feature.

    Parameters:
        key (str): Name of the attribute.
        value (str): Value of the attribute.
    """

    key: str
    value: Any

    def __repr__(self) -> str:
        return f"{self.key}={self.value}"


@dataclass
class FeatureAttributes(list[FeatureAttribute]):
    """A class representing a list of feature attributes.

    Converts input data to a list of FeatureAttribute instances.
    """

    _data: dict | None
    _items: list[FeatureAttribute] = field(init=False)

    def __post_init__(self) -> None:
        if self._data is not None:
            self._items = [
                FeatureAttribute(key, value) for key, value in self._data.items()
            ]
        else:
            self._items = []
        clear_temp_data(self)

    def __iter__(self) -> Iterator[FeatureAttribute]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> FeatureAttribute: ...

    @overload
    def __getitem__(self, idx: slice) -> list[FeatureAttribute]: ...

    def __getitem__(
        self, idx: SupportsIndex | slice
    ) -> FeatureAttribute | list[FeatureAttribute]:
        """Get a feature attribute by index or slice."""
        return self._items[idx]

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, idx):
        raise NotImplementedError("This method is not allowed in FeatureAttributes")

    def __setitem__(self, idx, value):
        raise NotImplementedError("This method is not allowed in FeatureAttributes")

    def __repr__(self) -> str:
        return repr(self._items)

    def set_attribute(self, field_: FeatureField, function: Callable) -> None:
        for item in self._items:
            if item.key == field_.name:
                item.value = function(item.value)
                break
        else:
            raise KeyError(f"Key '{field_.name}' not found in FeatureAttributes")  # noqa: TRY003

    def get_all_fields(self) -> list[str]:
        """
        Get all field names.

        Returns:
            List[str]: List of all field names.
        """
        return [item.key for item in self._items]

    def get_value(self, key: str) -> FeatureAttribute | None:
        """
        Get the value of a field.

        Parameters:
            key (str): The key of the field.

        Returns:
            Optional[FeatureAttribute]: The value of the field.
        """
        response = [item.value for item in self._items if item.key == key]
        if len(response) == 0:
            return None
        elif len(response) > 1:
            raise Exception(f"Duplicated key: {key}")  # noqa: TRY002, TRY003
        return response[0]


def parse_date(date_value: int) -> datetime | None:
    """
    Parse a date value.

    Parameters:
        date_value (int): The date value to parse.

    Returns:
        Optional[datetime]: The parsed date.
    """
    return datetime.utcfromtimestamp(date_value / 1000)
