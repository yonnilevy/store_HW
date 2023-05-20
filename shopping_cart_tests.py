import pytest

from errors import ItemNotExistError, ItemAlreadyExistsError
from shopping_cart import ShoppingCart
from store import Store


@pytest.fixture
def store():
    return Store('items.yml')


def test_empty_shopping_cart():
    assert ShoppingCart().get_subtotal() == 0


def test_remove_non_existing_item():
    with pytest.raises(ItemNotExistError):
        ShoppingCart().remove_item('some_name')


def test_add_item_twice(store):
    some_item = store.get_items()[0]
    shopping_cart = ShoppingCart()
    shopping_cart.add_item(some_item)
    with pytest.raises(ItemAlreadyExistsError):
        shopping_cart.add_item(some_item)


def test_correct_subtotal(store):
    expected_sum = sum([item.price for item in store.get_items()])
    shopping_cart = ShoppingCart()
    for item in store.get_items():
        shopping_cart.add_item(item)

    assert shopping_cart.get_subtotal() == expected_sum


def test_add_and_remove_same_item(store):
    shopping_cart = ShoppingCart()
    item = store.get_items()[0]

    shopping_cart.add_item(item)
    shopping_cart.remove_item(item.name)

    assert shopping_cart.get_subtotal() == 0
