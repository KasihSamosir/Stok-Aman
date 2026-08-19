from .preprocess import load_data


def create_supplier_features():
    df = load_data()

    supplier_features = (
        df.groupby("supplier_id")
        .agg(
            total_orders=("supplier_id", "count"),
            late_orders=("is_late", "sum"),
            average_delay_days=("delay_days", "mean")
        )
        .reset_index()
    )

    # Persentase pengiriman yang terlambat
    supplier_features["late_rate"] = (
        supplier_features["late_orders"]
        / supplier_features["total_orders"]
    )

    # Membulatkan angka agar lebih mudah dibaca
    supplier_features["average_delay_days"] = (
        supplier_features["average_delay_days"].round(2)
    )

    supplier_features["late_rate"] = (
        supplier_features["late_rate"].round(2)
    )

    return supplier_features


if __name__ == "__main__":
    features = create_supplier_features()

    print("=== SUPPLIER FEATURES ===")
    print(features.to_string(index=False))