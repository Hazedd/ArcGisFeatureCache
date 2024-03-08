class ImmutableList:
    def __init__(self, items):
        self._items = tuple(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def __repr__(self):
        return f"ImmutableList({self._items})"

    # Additional methods for your use case:
    def index(self, item):
        return self._items.index(item)

    def count(self, item):
        return self._items.count(item)

    def __eq__(self, other):
        if isinstance(other, ImmutableList):
            return self._items == other._items
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ImmutableList):
            return self._items != other._items
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, ImmutableList):
            return ImmutableList(list(self._items) + list(other._items))
        raise TypeError(  # noqa: TRY003
            f"unsupported operand type(s) for +: 'ImmutableList' and {type(other).__name__}"  # noqa: TRY003
        )  # noqa: TRY003

    def __radd__(self, other):
        if isinstance(other, (list | tuple)):
            return ImmutableList(list(other) + list(self._items))
        raise TypeError(  # noqa: TRY003
            f"unsupported operand type(s) for +: {type(other).__name__} and 'ImmutableList'"  # noqa: TRY003
        )  # noqa: TRY003

    def __mul__(self, n):
        return ImmutableList(list(self._items) * n)

    def __rmul__(self, n):
        return self.__mul__(n)
