import pytest

from arcGisFeatureCache.utils.immutableList import ImmutableList

# Test data
data = [1, 2, 3, 4, 5]
immutable_list = ImmutableList(data)


# Test cases
def test_getitem():
    assert immutable_list[0] == 1
    assert immutable_list[2] == 3
    with pytest.raises(IndexError):
        immutable_list[10]


def test_len():
    assert len(immutable_list) == len(data)


def test_contains():
    assert 3 in immutable_list
    assert 10 not in immutable_list


def test_repr():
    assert repr(immutable_list) == f"ImmutableList({tuple(data)})"


def test_index():
    assert immutable_list.index(3) == 2
    with pytest.raises(ValueError):
        immutable_list.index(10)


def test_count():
    assert immutable_list.count(3) == 1
    assert immutable_list.count(10) == 0


def test_equality():
    assert immutable_list == ImmutableList(data)
    assert immutable_list != ImmutableList([5, 4, 3, 2, 1])


def test_equality_same_lists():
    assert immutable_list == ImmutableList(data)


def test_equality_different_lists():
    assert not (immutable_list == ImmutableList([5, 4, 3, 2, 1]))


def test_equality_with_non_immutable_list():
    assert immutable_list.__eq__(1) is NotImplemented


def test_addition():
    new_list = immutable_list + ImmutableList([6, 7])
    assert len(new_list) == len(data) + 2


def test_multiplication():
    new_list = immutable_list * 3
    assert len(new_list) == len(data) * 3


def test_reflected_addition():
    new_list = [6, 7] + immutable_list
    assert len(new_list) == len(data) + 2


def test_invalid_operations():
    with pytest.raises(TypeError):
        immutable_list + [6, 7]
    with pytest.raises(TypeError):
        immutable_list * "invalid"


def test_radd_invalid_operand():
    with pytest.raises(TypeError):
        immutable_list.__radd__(1)


def test_inequality_same_lists():
    assert not (immutable_list != ImmutableList(data))


def test_inequality_different_lists():
    assert immutable_list != ImmutableList([5, 4, 3, 2, 1])


def test_inequality_with_non_immutable_list():
    assert immutable_list.__ne__(1) is NotImplemented


def test_rmul():
    n = 3
    multiplied_list = immutable_list.__rmul__(n)
    assert multiplied_list == immutable_list * n


def test_iteration():
    # Convert ImmutableList to a list for direct comparison
    assert list(immutable_list) == data
