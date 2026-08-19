import json
import pandas as pd

from .risk_scoring import calculate_supplier_risk


def get_supplier_risk(supplier_id):
    """
    Mengambil risk scoring untuk satu supplier.
    """

    results = calculate_supplier_risk()

    for result in results:
        if result["supplier_id"] == supplier_id:
            return result

    return {
        "error": f"Supplier {supplier_id} tidak ditemukan."
    }


def get_all_supplier_risk():
    """
    Mengambil risk scoring seluruh supplier.
    """

    return calculate_supplier_risk()


def save_risk_results(output_path="data/supplier_risk_scores.csv"):
    """
    Menyimpan hasil risk scoring seluruh supplier ke CSV.
    """

    results = get_all_supplier_risk()

    if not results:
        return

    df = pd.DataFrame(results)

    df.to_csv(output_path, index=False)

    print(f"Hasil risk scoring disimpan ke: {output_path}")


if __name__ == "__main__":

    # Test satu supplier
    result = get_supplier_risk("SUP-002")

    print("=== SINGLE SUPPLIER ===")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # Test seluruh supplier
    results = get_all_supplier_risk()

    print("\n=== ALL SUPPLIERS ===")
    print(json.dumps(results, indent=4, ensure_ascii=False))

    # Simpan hasil ke CSV
    save_risk_results()