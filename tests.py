from typing import List
from prep5 import LinkedList, _Node

def test_contains_empty() -> None:
    """Test LinkedList.__contains__ for an empty linked list."""
    lst = LinkedList()
    target = 5
    the_test = target in lst
    assert the_test is False


def test_contains_start() -> None:
    """Test LinkedList.__contains__ with target at index 0."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node4 = _Node(4)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    lst._first = node1
    assert (1 in lst) is True


def test_contains_last() -> None:
    """Test LinkedList.__contains__ with target in the last."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    assert (3 in lst) is True


def test_contains_middle() -> None:
    """Test LinkedList.__contains__ with target in middle."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    assert (2 in lst) is True


def test_contains_not_in() -> None:
    """Test LinkedList.__contains__ with target not in list."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    assert (4 in lst) is False


def test_contains_multiple() -> None:
    """Test LinkedList.__contains__ with multiple target."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(1)
    node3 = _Node(1)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    assert (1 in lst) is True



# Below are provided sample test cases for your use. You are encouraged
# to add additional test cases.
# WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
# Add your own to practice writing tests and to be confident your code is
# correct.
def test_len_empty() -> None:
    """Test LinkedList.__len__ for an empty linked list."""
    lst = LinkedList()
    assert len(lst) == 0


def test_len_three() -> None:
    """Test LinkedList.__len__ on a linked list of length 3."""
    lst = LinkedList()
    node1 = _Node(10)
    node2 = _Node(20)
    node3 = _Node(30)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert len(lst) == 3


def test_contains_doctest() -> None:
    """Test LinkedList.__contains__ on the given doctest."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert 2 in lst
    assert not (4 in lst)


def test_append_empty() -> None:
    """Test LinkedList.append on an empty list."""
    lst = LinkedList()
    lst.append(1)
    assert lst._first.item == 1


def test_append_one() -> None:
    """Test LinkedList.append on a list of length 1."""
    lst = LinkedList()
    lst._first = _Node(1)
    lst.append(2)
    assert lst._first.next.item == 2


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])

