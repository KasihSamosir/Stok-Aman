import pandas as pd


DATA_PATH = "data/supplier_history.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)

    date_columns = [
        "order_date",
        "estimated_delivery_date",
        "actual_delivery_date"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    # Menghitung jumlah hari keterlambatan
    df["delay_days"] = (
        df["actual_delivery_date"]
        - df["estimated_delivery_date"]
    ).dt.days

    # 1 = terlambat, 0 = tidak terlambat
    df["is_late"] = (df["delay_days"] > 0).astype(int)

    return df


if __name__ == "__main__":
    df = load_data()

    print("=== DATA HASIL PREPROCESSING ===")
    print(df)

    print("\n=== RINGKASAN ===")
    print(f"Jumlah pengiriman : {len(df)}")
    print(f"Jumlah terlambat  : {df['is_late'].sum()}")
    