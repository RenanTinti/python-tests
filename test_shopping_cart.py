from unittest.mock import Mock
from item_database import ItemDatabase
from shopping_cart import ShoppingCart
import pytest

# Fixtures are used to avoid code repetition. Can be passed as argument in functions that will execute the same code 
@pytest.fixture
def cart():
    # All setup for the cart here...
    return ShoppingCart(5)

def test_can_add_item_to_cart(cart):
    cart.add('apple')
    assert cart.size() == 1

def test_when_item_added_cart_contains_item(cart):
    cart.add('apple')
    cart.add('orange')
    assert 'orange' in cart.get_items()

def test_when_add_more_than_max_items_should_fail(cart):
    for _ in range(5):
        cart.add('apple')

    with pytest.raises(OverflowError):
        cart.add('apple')

def test_can_get_total_price(cart):
    cart.add('apple')
    cart.add('orange')

    # Let's suppose our ItemDatabase().get has not been implemented yet, but we need to test it. We can mock this method to force it to pass items, using the return_value=, like the commented example below (I commented the example because it will return the value 1.0 two times, not passing the test, that should be 3.0)
    item_database = ItemDatabase()
    # item_database.get = Mock(return_value=1.0)

    # Using Mock side_effect, we can custom the values of each item
    def mock_get_item(item: str):
        if item == 'apple':
            return 1.0
        if item == 'orange':
            return 2.0

    item_database.get = Mock(side_effect=mock_get_item)

    '''price_map = {
        'apple': 1.0,
        'orange': 2.0,
    }'''

    assert cart.get_total_price(item_database) == 3.0