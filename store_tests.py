import pytest

from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError
from store import Store


@pytest.fixture
def store() -> Store:
    return Store('items.yml')


@pytest.mark.search
def test_lexical_sort_with_empty_shopping_cart_search_by_name(store):
    expected_items_list = store.get_items()
    expected_items_list.sort(key=lambda item: item.name)
    assert expected_items_list == store.search_by_name('')


@pytest.mark.search
def test_lexical_sort_with_empty_shopping_cart_and_search_for_item(store):
    search_phrase = 'the '
    expected_items_list = list(filter(lambda item: search_phrase in item.name, store.get_items()))
    expected_items_list.sort(key=lambda item: item.name)
    assert expected_items_list == store.search_by_name(search_phrase)


@pytest.mark.search
def test_search_hashtag_empty_shopping_cart(store):
    hashtag = 'Technology'
    expected_items_list = [item for item in store.get_items() if hashtag in item.hashtags]
    expected_items_list.sort(key=lambda item: item.name)
    assert expected_items_list == store.search_by_hashtag(hashtag)


@pytest.mark.search
def test_search_no_existing_hashtag(store):
    assert len(store.search_by_hashtag('qqq')) == 0


@pytest.mark.search
def test_search_no_existing_name(store):
    assert len(store.search_by_name('qqq')) == 0


@pytest.mark.search
def test_sort_with_shopping_cart_example(store):
    store.add_item('Shopping Cart 1')
    store.add_item('Shopping Cart 2')
    expected_items_names = ['Bbbb', 'Cccc', 'Aaaa']
    result_list = [i.name for i in store.search_by_name('')[:len(expected_items_names)]]
    assert result_list == expected_items_names


@pytest.mark.search
def test_sort_with_hashtag_search_non_empty_cart(store):
    store.add_item('Bbbb')
    expected_items_names = ['Shopping Cart 1', 'Shopping Cart 2']
    result_list = [i.name for i in store.search_by_hashtag('H1')]
    assert result_list == expected_items_names


@pytest.mark.checkout
def test_checkout_empty_shopping_cart(store):
    assert store.checkout() == 0


@pytest.mark.checkout
def test_correct_total(store):
    expected_sum = sum([item.price for item in store.get_items()])
    for item in store.get_items():
        store.add_item(item.name)

    assert store.checkout() == expected_sum


@pytest.mark.remove
def test_remove_non_existing_item(store):
    with pytest.raises(ItemNotExistError):
        store.remove_item('some_name')


@pytest.mark.remove
def test_remove_item_with_too_generic_name(store):
    items = store.get_items()
    store.add_item(items[0].name)
    store.add_item(items[1].name)

    with pytest.raises(TooManyMatchesError):
        store.remove_item('')


@pytest.mark.remove
@pytest.mark.add
@pytest.mark.checkout
def test_add_and_remove_same_item(store):
    item = store.get_items()[0]

    store.add_item(item.name)
    store.remove_item(item.name)

    assert store.checkout() == 0


@pytest.mark.add
def test_add_item_twice(store):
    some_item = store.get_items()[0]
    store.add_item(some_item.name)
    with pytest.raises(ItemAlreadyExistsError):
        store.add_item(some_item.name)


@pytest.mark.add
def test_add_item_with_too_generic_name(store):
    with pytest.raises(TooManyMatchesError):
        store.add_item('')


@pytest.mark.add
def test_add_non_existing_item(store):
    with pytest.raises(ItemNotExistError):
        store.add_item('blah_blah_blah')
