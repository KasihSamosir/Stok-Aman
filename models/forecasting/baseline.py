import pandas as pd
from sklearn.metrics import mean_absolute_error


DATA_PATH = "data/processed_sales.csv"

TEST_SIZE = 73
FORECAST_HORIZON = 7
WINDOW_SIZE = 7


def evaluate_baseline(product_data):
    """
    Baseline forecasting dengan moving average 7 hari.

    Evaluasi dilakukan dengan horizon 7 hari:
    model memprediksi 7 hari sekaligus,
    kemudian dibandingkan dengan data aktual.
    """

    product_data = product_data.sort_values("date").copy()

    values = product_data["units_sold"].to_numpy()

    # Pisahkan data training dan testing berdasarkan waktu
    train = values[:-TEST_SIZE]
    test = values[-TEST_SIZE:]

    history = list(train)

    actual_all = []
    prediction_all = []

    # Evaluasi dalam blok 7 hari
    for start in range(0, len(test), FORECAST_HORIZON):

        actual_block = test[
            start:start + FORECAST_HORIZON
        ]

        if len(actual_block) == 0:
            break

        # Ambil 7 hari terakhir
        recent_values = history[-WINDOW_SIZE:]

        # Prediksi = rata-rata 7 hari terakhir
        prediction = sum(recent_values) / len(recent_values)

        # Prediksi yang sama untuk 7 hari
        predictions = [
            prediction
        ] * len(actual_block)

        actual_all.extend(actual_block)
        prediction_all.extend(predictions)

        # Setelah blok selesai,
        # data aktual baru dimasukkan ke history.
        history.extend(actual_block)

    mae = mean_absolute_error(
        actual_all,
        prediction_all
    )

    return mae


def main():

    print("=" * 60)
    print("BASELINE FORECASTING - HORIZON 7 HARI")
    print("=" * 60)

    # Membaca dataset
    df = pd.read_csv(DATA_PATH)

    df["date"] = pd.to_datetime(df["date"])

    results = []

    # Evaluasi setiap produk
    for product_id in df["product_id"].unique():

        product_data = df[
            df["product_id"] == product_id
        ].copy()

        product_name = product_data[
            "product_name"
        ].iloc[0]

        mae = evaluate_baseline(
            product_data
        )

        results.append({
            "product_id": product_id,
            "product_name": product_name,
            "MAE": round(mae, 2)
        })

    results_df = pd.DataFrame(results)

    print("\nHasil Baseline 7 Hari:")
    print(
        results_df.to_string(index=False)
    )

    print("\nRata-rata MAE:")

    print(
        round(
            results_df["MAE"].mean(),
            2
        )
    )

    print("\n" + "=" * 60)
    print("BASELINE SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    main()