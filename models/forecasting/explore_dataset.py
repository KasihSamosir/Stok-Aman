import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "data/sales_history_stokaman.csv"


def main():
    # Membaca dataset
    df = pd.read_csv(DATA_PATH)

    # Mengubah tanggal menjadi format datetime
    df["date"] = pd.to_datetime(df["date"])

    # Mengurutkan data
    df = df.sort_values(["product_id", "date"])

    # ==========================================================
    # 1. GRAFIK HISTORI PENJUALAN SETIAP PRODUK
    # ==========================================================

    products = df["product_id"].unique()

    for product_id in products:
        product_data = df[df["product_id"] == product_id]

        product_name = product_data["product_name"].iloc[0]

        plt.figure(figsize=(12, 5))

        plt.plot(
            product_data["date"],
            product_data["units_sold"]
        )

        plt.title(
            f"Histori Penjualan - {product_id} ({product_name})"
        )

        plt.xlabel("Tanggal")
        plt.ylabel("Unit Terjual")

        plt.grid(True)

        plt.tight_layout()

        plt.show()

    # ==========================================================
    # 2. POLA PENJUALAN BERDASARKAN HARI
    # ==========================================================

    df["day_name"] = df["date"].dt.day_name()

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    daily_sales = (
        df.groupby("day_name")["units_sold"]
        .mean()
        .reindex(day_order)
    )

    plt.figure(figsize=(10, 5))

    daily_sales.plot(kind="bar")

    plt.title("Rata-rata Penjualan Berdasarkan Hari")

    plt.xlabel("Hari")

    plt.ylabel("Rata-rata Unit Terjual")

    plt.xticks(rotation=0)

    plt.grid(axis="y")

    plt.tight_layout()

    plt.show()

    # ==========================================================
    # 3. RATA-RATA PENJUALAN PER PRODUK
    # ==========================================================

    product_sales = (
        df.groupby("product_name")["units_sold"]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(10, 5))

    product_sales.plot(kind="bar")

    plt.title("Rata-rata Penjualan Setiap Produk")

    plt.xlabel("Produk")

    plt.ylabel("Rata-rata Unit Terjual")

    plt.xticks(rotation=45, ha="right")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()