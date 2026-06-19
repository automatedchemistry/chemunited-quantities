import pytest

from chemunited_quantities import ChemUnitQuantity, units_for_dimension, ureg

# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_from_string():
    q = ChemUnitQuantity("5 ml")
    assert q.magnitude == 5.0
    assert str(q.units) == "milliliter"


def test_from_magnitude_and_unit():
    q = ChemUnitQuantity(10, "ml")
    assert q.magnitude == 10


def test_from_pint_quantity():
    pq = ureg.Quantity(3, "ml")
    q = ChemUnitQuantity(pq)
    assert q.magnitude == 3


def test_parse_classmethod():
    q = ChemUnitQuantity.parse("3 ml")
    assert q.magnitude == 3


def test_parse_rejects_bare_number():
    with pytest.raises(ValueError):
        ChemUnitQuantity.parse(42)


def test_from_any_string():
    q = ChemUnitQuantity.from_any("5 ml")
    assert q.magnitude == 5


def test_from_any_number_with_default_unit():
    q = ChemUnitQuantity.from_any(5, default_unit="ml")
    assert q.magnitude == 5


def test_from_any_number_without_unit_raises():
    with pytest.raises(ValueError):
        ChemUnitQuantity.from_any(5)


def test_invalid_construction_raises():
    with pytest.raises(TypeError):
        ChemUnitQuantity(42)


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------


def test_add_same_unit():
    a = ChemUnitQuantity(1, "ml")
    b = ChemUnitQuantity(1, "ml")
    result = a + b
    assert isinstance(result, ChemUnitQuantity)
    assert result.magnitude == 2


def test_add_scalar_uses_self_unit():
    q = ChemUnitQuantity(5, "ml")
    result = q + 2
    assert result.magnitude == 7


def test_radd():
    q = ChemUnitQuantity(5, "ml")
    result = 2 + q
    assert result.magnitude == 7


def test_sub():
    a = ChemUnitQuantity(5, "ml")
    b = ChemUnitQuantity(3, "ml")
    result = a - b
    assert result.magnitude == 2


def test_mul_scalar():
    q = ChemUnitQuantity(5, "ml")
    result = q * 2
    assert result.magnitude == 10


def test_rmul_scalar():
    q = ChemUnitQuantity(5, "ml")
    result = 2 * q
    assert result.magnitude == 10


def test_div_scalar():
    q = ChemUnitQuantity(10, "ml")
    result = q / 2
    assert result.magnitude == 5


# ---------------------------------------------------------------------------
# degC offset handling (the known divergence fix)
# ---------------------------------------------------------------------------


def test_degc_from_string():
    q = ChemUnitQuantity("25 degC")
    assert q.magnitude == 25
    # pint normalises "degC" to "degree_Celsius" internally; verify via conversion
    assert abs(q.to("kelvin").magnitude - 298.15) < 0.01


def test_degree_sign_alias():
    q = ChemUnitQuantity("25 \N{DEGREE SIGN}C")
    assert abs(q.to("kelvin").magnitude - 298.15) < 0.01


def test_celsius_alias():
    q = ChemUnitQuantity("25 celsius")
    assert abs(q.to("kelvin").magnitude - 298.15) < 0.01


# ---------------------------------------------------------------------------
# units_for_dimension
# ---------------------------------------------------------------------------


def test_units_for_volume():
    dims = ureg.Quantity(1, "ml").dimensionality
    result = units_for_dimension(dims, ureg)
    assert "ml" in result
    assert "ul" in result


def test_units_for_temperature():
    dims = ureg.Quantity(1, "degC").dimensionality
    result = units_for_dimension(dims, ureg)
    assert "degC" in result


def test_units_for_none_returns_empty():
    assert units_for_dimension(None, ureg) == []


# ---------------------------------------------------------------------------
# repr
# ---------------------------------------------------------------------------


def test_repr():
    q = ChemUnitQuantity(5, "ml")
    assert "ChemUnitQuantity" in repr(q)
    assert "5" in repr(q)
