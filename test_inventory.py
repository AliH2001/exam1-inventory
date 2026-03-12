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
# ============================================================

def test_add_product_fields_are_correct():
    # Arrange
    name = "Computer"
    price = 500.00
    stock = 20
    # Act
    result = add_product("A1", name, price, stock)
    # Assert
    assert result["product_id"] == "A1"
    assert result["name"] == name
    assert result["price"] == price
    assert result["stock"] == stock

def test_add_product_with_zero_stock():
    # Arrange + Act
    result = add_product("A2", "Headphones", 30.00, 0)
    # Assert
    assert result["stock"] == 0

def test_get_product_after_adding_it():
    # Arrange
    add_product("A1", "Mouse", 25.00, 15)
    # Act
    result = get_product("A1")
    # Assert
    assert result["name"] == "Mouse"
    assert result["price"] == 25.00
    assert result["stock"] == 15

def test_update_stock_going_up():
    # Arrange
    add_product("A1", "Keyboard", 15.50, 10)
    # Act
    update_stock("A1", 5)
    product = get_product("A1")
    # Assert
    assert product["stock"] == 15

def test_update_stock_going_down():
    # Arrange
    add_product("A1", "Monitor", 150.00, 8)
    # Act
    update_stock("A1", -3)
    product = get_product("A1")
    # Assert
    assert product["stock"] == 5

def test_calculate_total_multiplies_correctly():
    # Arrange
    add_product("A1", "Webcam", 45.00, 12)
    # Act
    total = calculate_total("A1", 4)
    # Assert
    assert total == 180.00

def test_get_product_returns_none_when_missing():
    # Act
    result = get_product("DOESNOTEXIST")
    # Assert
    assert result is None

def test_list_products_when_empty():
    # Act
    result = list_products()
    # Assert
    assert result == []

def test_list_products_count_is_correct():
    # Arrange
    add_product("A1", "Item A", 10.00, 5)
    add_product("A2", "Item B", 20.00, 10)
    # Act
    result = list_products()
    # Assert
    assert len(result) == 2


# ============================================================
# PART B - Exception Testing (12 marks)
# ============================================================

def test_add_product_empty_id_raises_error():
    with pytest.raises(ValueError, match="required"):
        add_product("", "Laptop", 500.00, 10)

def test_add_product_empty_name_raises_error():
    with pytest.raises(ValueError, match="required"):
        add_product("A1", "", 500.00, 10)

def test_add_product_negative_price_raises_error():
    with pytest.raises(ValueError, match="positive"):
        add_product("A1", "Monitor", -10.00, 5)

def test_add_product_duplicate_raises_error():
    add_product("A1", "Computer", 200.00, 10)
    with pytest.raises(ValueError, match="already exists"):
        add_product("A1", "Computer", 250.00, 15)

def test_update_stock_below_zero_raises_error():
    add_product("A1", "Mouse", 10.00, 5)
    with pytest.raises(ValueError, match="zero"):
        update_stock("A1", -6)

def test_calculate_total_zero_quantity_raises_error():
    add_product("A1", "Laptop", 500.00, 10)
    with pytest.raises(ValueError, match="positive"):
        calculate_total("A1", 0)


# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
# ============================================================

@pytest.fixture
def s_products():
    add_product("A1", "Headphones", 50.00, 10)
    add_product("A2", "Printer", 60.00, 50)
    add_product("A3", "Scanner", 70.00, 25)
    return ["A1", "A2", "A3"]

def test_list_products_shows_three_items(s_products):
    result = list_products()
    assert len(result) == 3

def test_calculate_total_for_sample_product(s_products):
    result = calculate_total("A1", 2)
    assert result == 100.00

@pytest.mark.parametrize("total, quantity, expected", [
    (100.00,  3, 100.00),
    (100.00, 10,  95.00),
    (100.00, 25,  90.00),
    (100.00, 50,  85.00),
    (200.00, 30, 180.00),
])
def test_apply_bulk_discount(total, quantity, expected):
    result = apply_bulk_discount(total, quantity)
    assert result == expected


# ============================================================
# PART D - Mocking (5 marks)
# ============================================================

@patch("inventory._send_restock_alert")
def test_restock_alert_called_when_stock_drops(mock_alert):
    add_product("A1", "Webcam", 45.00, 6)
    update_stock("A1", -3)
    mock_alert.assert_called_once_with("A1", "Webcam", 3)

@patch("inventory._send_restock_alert")
def test_restock_alert_not_called_when_stock_stays_high(mock_alert):
    add_product("A1", "Webcam", 45.00, 20)
    update_stock("A1", -5)
    mock_alert.assert_not_called()


# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# ============================================================

def test_update_stock_product_not_found_raises_error():
    with pytest.raises(ValueError, match="not found"):
        update_stock("DOESNOTEXIST", 5)

def test_add_product_negative_stock_raises_error():
    with pytest.raises(ValueError, match="negative"):
        add_product("A1", "Laptop", 500.00, -1)

def test_apply_bulk_discount_negative_quantity_raises_error():
    with pytest.raises(ValueError, match="negative"):
        apply_bulk_discount(100.00, -1)

def test_apply_bulk_discount_negative_total_raises_error():
    with pytest.raises(ValueError, match="negative"):
        apply_bulk_discount(-50.00, 5)


# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================

# TODO: Write your bonus tests here (optional)
