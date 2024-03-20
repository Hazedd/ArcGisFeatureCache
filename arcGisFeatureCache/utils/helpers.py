from typing import Any, Protocol


class HasTempDataProtocol(Protocol):
    _data: Any


def clear_temp_data(self: HasTempDataProtocol) -> None:
    del self._data
    self._data = None
