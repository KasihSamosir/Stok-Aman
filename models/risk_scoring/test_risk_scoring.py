from .predict import get_supplier_risk


def test_supplier_risk():
    result = get_supplier_risk("SUP-002")

    assert result["supplier_id"] == "SUP-002"
    assert result["risk_score"] == 0.65
    assert result["risk_level"] == "high"

    print("TEST SUP-002: PASSED")


def test_unknown_supplier():
    result = get_supplier_risk("SUP-999")

    assert "error" in result

    print("TEST SUP-999: PASSED")


if __name__ == "__main__":
    test_supplier_risk()
    test_unknown_supplier()

    print("\nSEMUA TEST BERHASIL.")