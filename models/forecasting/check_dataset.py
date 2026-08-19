import pandas as pd

# Lokasi dataset
DATA_PATH = "data/sales_history_stokaman.csv"


def main():
    # Membaca dataset
    df = pd.read_csv(DATA_PATH)

    print("=" * 50)
    print("VALIDASI DATASET STOKAMAN - FORECASTING")
    print("=" * 50)

    # 1. Ukuran dataset
    print("\n[1] UKURAN DATASET")
    print(f"Jumlah baris : {len(df)}")
    print(f"Jumlah kolom : {len(df.columns)}")

    # 2. Nama kolom
    print("\n[2] KOLOM")
    print(list(df.columns))

    # 3. Informasi dasar
    print("\n[3] INFORMASI DATA")
    print(df.info())

    # 4. Format tanggal
    df["date"] = pd.to_datetime(df["date"])

    print("\n[4] PERIODE DATA")
    print(f"Tanggal awal : {df['date'].min().date()}")
    print(f"Tanggal akhir: {df['date'].max().date()}")

    # 5. Jumlah produk
    print("\n[5] PRODUK")
    print(f"Jumlah produk: {df['product_id'].nunique()}")

    print("\nDaftar produk:")
    products = df[["product_id", "product_name"]].drop_duplicates()
    print(products.to_string(index=False))

    # 6. Missing value
    print("\n[6] DATA KOSONG")
    missing = df.isnull().sum()
    print(missing)

    # 7. Duplikasi baris
    print("\n[7] DUPLIKASI BARIS")
    print(f"Jumlah duplikat: {df.duplicated().sum()}")

    # 8. Duplikasi tanggal + produk
    print("\n[8] DUPLIKASI TANGGAL + PRODUK")
    duplicate_keys = df.duplicated(
        subset=["date", "product_id"]
    ).sum()

    print(f"Jumlah duplikat: {duplicate_keys}")

    # 9. Nilai negatif
    print("\n[9] NILAI PENJUALAN NEGATIF")
    negative = (df["units_sold"] < 0).sum()
    print(f"Jumlah nilai negatif: {negative}")

    # 10. Statistik keseluruhan
    print("\n[10] STATISTIK UNITS SOLD")
    print(df["units_sold"].describe())

    # 11. Statistik setiap produk
    print("\n[11] STATISTIK PER PRODUK")

    product_stats = (
        df.groupby(["product_id", "product_name"])["units_sold"]
        .agg(
            jumlah_data="count",
            rata_rata="mean",
            minimum="min",
            maksimum="max",
            standar_deviasi="std",
        )
        .round(2)
    )

    print(product_stats)

    # 12. Pola berdasarkan hari
    print("\n[12] RATA-RATA PENJUALAN BERDASARKAN HARI")

    df["day_name"] = df["date"].dt.day_name()

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    daily_pattern = (
        df.groupby("day_name")["units_sold"]
        .mean()
        .reindex(day_order)
        .round(2)
    )

    print(daily_pattern)

    print("\n" + "=" * 50)
    print("VALIDASI SELESAI")
    print("=" * 50)


if __name__ == "__main__":
    main()