import math
import pathlib
import sys

import pytest

# Импорт приложения
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.app import (
    app as flask_app,
    calculate,
    bad_expression_msg,
    json_error_msg,
)

# ----
# Хелперы
TOLERANCE = 1e-12  # погрешность для float

import unittest.mock
from backend.app import store

# Mock the database for all tests
@pytest.fixture(autouse=True)
def mock_database():
    with unittest.mock.patch.object(store, 'add') as mock_add:
        yield mock_add

# Your existing client fixture
@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def assert_num_equal(actual, expected):
    if isinstance(expected, float):
        assert math.isclose(actual, expected, rel_tol=TOLERANCE, abs_tol=0.0)
    else:
        assert actual == expected


# Фикстура Flask
@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

# ----
# Наборы тест‑данных для calculate()
BASIC_CASES = [
    ("1+1", 2),
    ("2*3", 6),
    ("10/4", 2.5),
    ("(5-2)**2", 9),
]

# Огромные целые (проверка отсутствия переполнения)
LONG = "9" * 105
BIG_INT_CASES = [
    (f"{LONG}+1", int(LONG) + 1),
    (f"{LONG}*2", int(LONG) * 2),
]

# Дроби
FRACTION_CASES = [
    ("1/8", 0.125),
    ("1/7", 0.14285714285714285),
]

# Отрицательные
NEGATIVE_CASES = [
    ("-5/2", -2.5),
    ("(-10)*(-3)", 30),
    ("-2**3", -8),
]

# Остаток
MODULO_CASES = [
    ("10%3", 1),
    ("-7%5", 3),
]

# Округление вниз
FLOORDIV_CASES = [
    ("7//3", 2),
    ("-7//3", -3),
]

# Порядок со скобками
PRECEDENCE_CASES = [
    ("2+3*4", 14),
    ("2+2*2", 6),
    ("2*(3+4)", 14),
    ("-(3+2)*4", -20),
    ("(10+5)%4", 3),
]

ALL_SUCCESS_CASES = (
    BASIC_CASES
    + BIG_INT_CASES
    + FRACTION_CASES
    + NEGATIVE_CASES
    + MODULO_CASES
    + FLOORDIV_CASES
    + PRECEDENCE_CASES
)

# ----
# Юнит‑тесты calculate()
@pytest.mark.parametrize("expr, expected", ALL_SUCCESS_CASES)
def test_calculate_success(expr, expected):
    ok, res = calculate(expr)
    assert ok is True
    assert_num_equal(res, expected)


def test_division_by_zero():
    ok, res = calculate("1/0")
    assert ok is False and res is None


# Неверные выражения
@pytest.mark.parametrize("expr", [
    "2+*2",
    "unknown_var",
    "1/0",
])
def test_calculate_failure(expr):
    ok, res = calculate(expr)
    assert ok is False and res is None


# ----
# Тесты округления до 3‑х знаков
FMT3 = lambda x: f"{x:.3f}"

@pytest.mark.parametrize("expr, expected_fmt", [
    ("10/3", "3.333"),
    ("2/7",  "0.286"),
    ("1/8",  "0.125"),
])
def test_rounding_3dp(expr, expected_fmt):
    ok, res = calculate(expr)
    assert ok
    assert FMT3(res) == expected_fmt


# ----
# API‑тесты
API_OK_CASES = [
    ("3*3", "9"),
    ("10/4", "2.5"),
    ("10%3", "1"),
]

API_BAD_CASES = ["2+*", "unknown_var"]

@pytest.mark.parametrize("expression, expected", API_OK_CASES)
def test_calculate_handler_ok(client, expression, expected):
    r = client.post("/v1/calculate", json={"expression": expression})
    assert r.status_code == 200
    assert r.get_json() == {"result": expected}


@pytest.mark.parametrize("expression", API_BAD_CASES)
def test_calculate_handler_bad_expr(client, expression):
    r = client.post("/v1/calculate", json={"expression": expression})
    assert r.status_code == 400
    assert r.get_json() == {"error": bad_expression_msg}


def test_calculate_handler_non_json(client):
    r = client.post("/v1/calculate", data="expression=1+1")
    assert r.status_code == 400
    assert r.get_json() == {"error": json_error_msg}
