"""
Exam 1 - Test Inventory Module
================================
Write your tests below. Each section (Part A through E) is marked.
Follow the instructions in each part carefully.

Run your tests with:
    pytest test_inventory.py -v

Run with coverage:
    pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
"""

import pytest
from unittest.mock import patch
from inventory import (
    add_product,
    get_product,
    update_stock,
    calculate_total,
    apply_bulk_discount,
    list_products,
)


# ============================================================
# FIXTURE: Temporary inventory file (provided for you)
# This ensures each test gets a clean, isolated inventory.
# ============================================================

@pytest.fixture(autouse=True)
def clean_inventory(tmp_path, monkeypatch):
    """Use a temporary inventory file for each test."""
    db_file = str(tmp_path / "inventory.json")
    monkeypatch.setattr("inventory.INVENTORY_FILE", db_file)
    yield


# ============================================================
# PART A - Basic Assertions (18 marks)
# Write at least 8 tests using plain assert statements.
# Cover: add_product, get_product, update_stock,
#        calculate_total, and list_products.
# Follow the AAA pattern (Arrange, Act, Assert).
# ============================================================

# TODO: Write your Part A tests here


# ============================================================
# PART B - Exception Testing (12 marks)
# Write at least 6 tests using pytest.raises.
# Cover: empty name, negative price, duplicate product,
#        stock going below zero, product not found, etc.
# ============================================================

# TODO: Write your Part B tests here
def test_add_product_fields_are_correct():
    # Arrange
    name = "Cumputer"
    price = 50.00
    stock = 20

    # Act
    product_id = add_product(name, price, stock)
    product = get_product(product_id)

    # Assert
    assert product["name"] == name
    assert product["price"] == price
    assert product["stock"] == stock

def test_add_product_with_zero_stock():
    # Arrange
    name = "Headphones"
    price = 30.00
    stock = 0

    # Act
    product_id = add_product(name, price, stock)
    product = get_product(product_id)

    # Assert
    assert product["name"] == name
    assert product["price"] == price
    assert product["stock"] == stock

def test_get_product_after_adding_it():
    # Arrange
    name = "Mouse"
    price = 25.00
    stock = 15

    # Act
    product_id = add_product(name, price, stock)
    product = get_product(product_id)

    # Assert
    assert product["name"] == name
    assert product["price"] == price
    assert product["stock"] == stock

def test_update_stock_going_up():
    # Arrange
    name = "Keyboard"
    price = 15.50
    stock = 10
    product_id = add_product(name, price, stock)

    # Act
    update_stock(product_id, 5)
    product = get_product(product_id)

    # Assert
    assert product["stock"] == stock + 5

def test_update_stock_going_down():
    # Arrange
    name = "Monitor"
    price = 150.00
    stock = 8
    product_id = add_product(name, price, stock)

    # Act
    update_stock(product_id, -3)
    product = get_product(product_id)

    # Assert
    assert product["stock"] == stock - 3

def test_calculate_total_multiplies_correctly():
    # Arrange
    name = "Webcam"
    price = 45.00
    stock = 12
    product_id = add_product(name, price, stock)
    quantity = 4

    # Act
    total = calculate_total(product_id, quantity)

    # Assert
    assert total == price * quantity

def test_get_product_returns_none_when_missing():
    # Act
    result = get_product("DOESNOTEXIST") 

    # Assert
    assert result is None

def test_list_products_when_empty():
    # Act
    products = list_products()

    # Assert
    assert products == []

def test_list_products_count_is_correct():
    # Arrange
    add_product("Item A", 10.00, 5)
    add_product("Item B", 20.00, 10)

    # Act
    products = list_products()

    # Assert
    assert len(products) == 2

# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
#
# C1: Create a @pytest.fixture called "sample_products" that
#     adds 3 products to the inventory and returns their IDs.
#     Write 2 tests that use this fixture.
#
# C2: Use @pytest.mark.parametrize to test apply_bulk_discount
#     with at least 5 different (total, quantity, expected) combos.
# ============================================================

# TODO: Write your Part C tests here


# ============================================================
# PART D - Mocking (5 marks)
# Use @patch to mock _send_restock_alert.
# Write 2 tests:
#   1. Verify the alert IS called when stock drops below 5
#   2. Verify the alert is NOT called when stock stays >= 5
# ============================================================

# TODO: Write your Part D tests here


# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# You must achieve 90%+ coverage on inventory.py.
# If lines are missed, add more tests above to cover them.
# ============================================================


# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================

# TODO: Write your bonus tests here (optional)
