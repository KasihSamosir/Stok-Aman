import pandas as pd


DATA_PATH = "data/sales_history_stokaman.csv"
OUTPUT_PATH = "data/processed_sales.csv"


def preprocess_data():
    print("=" * 50)
    print("PREPROCESSING DATA FORECASTING")
    print("=" * 50)

    # 1. Membaca dataset
    df = pd.read_csv(DATA_PATH)

    print(f"\nData awal: {len(df)} baris")

    # 2. Konversi tanggal
    df["date"] = pd.to_datetime(df["date"])

    # 3. Pastikan units_sold berupa angka
    df["units_sold"] = pd.to_numeric(
        df["units_sold"],
        errors="coerce"
    )

    # 4. Urutkan berdasarkan produk dan waktu
    df = df.sort_values(
        ["product_id", "date"]
    ).reset_index(drop=True)

    # 5. Cek nilai kosong setelah konversi
    print("\nMissing value:")
    print(df.isnull().sum())

    # 6. Cek tanggal untuk setiap produk
    print("\nPengecekan kontinuitas tanggal:")

    for product_id, group in df.groupby("product_id"):

        dates = group["date"].sort_values()

        expected_dates = pd.date_range(
            start=dates.min(),
            end=dates.max(),
            freq="D"
        )

        missing_dates = expected_dates.difference(dates)

        if len(missing_dates) == 0:
            print(
                f"{product_id}: "
                "tidak ada tanggal yang hilang"
            )
        else:
            print(
                f"{product_id}: "
                f"{len(missing_dates)} tanggal hilang"
            )

    # 7. Membuat fitur waktu
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_name"] = df["date"].dt.day_name()
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["month"] = df["date"].dt.month

    # 8. Menyimpan hasil
    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nData hasil preprocessing:")
    print(df.head())

    print("\nJumlah data akhir:")
    print(len(df))

    print(f"\nFile disimpan di:")
    print(OUTPUT_PATH)

    print("\n" + "=" * 50)
    print("PREPROCESSING SELESAI")
    print("=" * 50)

    return df


if __name__ == "__main__":
    preprocess_data()