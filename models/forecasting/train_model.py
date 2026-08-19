import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


DATA_PATH = "data/processed_sales.csv"
MODEL_DIR = "models/forecasting/saved_models"

TEST_SIZE = 73
FORECAST_HORIZON = 7

FEATURES = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_7",
    "lag_14",
    "day_of_week",
    "month",
]


def create_model():
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )


def add_lag_features(data):
    data = data.sort_values("date").copy()

    data["lag_1"] = data["units_sold"].shift(1)
    data["lag_2"] = data["units_sold"].shift(2)
    data["lag_3"] = data["units_sold"].shift(3)
    data["lag_7"] = data["units_sold"].shift(7)
    data["lag_14"] = data["units_sold"].shift(14)

    return data


def evaluate_model(product_data):
    """
    Evaluasi Random Forest pada data testing.
    Digunakan sebagai pengecekan sebelum
    model final dilatih menggunakan seluruh data.
    """

    product_data = (
        product_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    train_data = product_data.iloc[:-TEST_SIZE]
    test_data = product_data.iloc[-TEST_SIZE:]

    train_features = add_lag_features(
        train_data
    ).dropna()

    X_train = train_features[FEATURES]
    y_train = train_features["units_sold"]

    model = create_model()

    model.fit(
        X_train,
        y_train
    )

    history = train_data[
        "units_sold"
    ].tolist()

    actual_all = []
    prediction_all = []

    for start in range(
        0,
        len(test_data),
        FORECAST_HORIZON
    ):

        test_block = test_data.iloc[
            start:start + FORECAST_HORIZON
        ]

        predictions = []

        for i in range(
            len(test_block)
        ):

            future_date = test_block[
                "date"
            ].iloc[i]

            features = pd.DataFrame([{
                "lag_1": history[-1],
                "lag_2": history[-2],
                "lag_3": history[-3],
                "lag_7": history[-7],
                "lag_14": history[-14],
                "day_of_week": future_date.dayofweek,
                "month": future_date.month,
            }])

            prediction = model.predict(
                features[FEATURES]
            )[0]

            prediction = max(
                0,
                float(prediction)
            )

            predictions.append(
                prediction
            )

            # Recursive forecasting
            history.append(
                prediction
            )

        actual = test_block[
            "units_sold"
        ].tolist()

        actual_all.extend(actual)
        prediction_all.extend(predictions)

        # Setelah blok 7 hari selesai,
        # gunakan aktual untuk blok berikutnya.
        history = (
            train_data["units_sold"].tolist()
            + test_data[
                "units_sold"
            ].iloc[
                :start + len(test_block)
            ].tolist()
        )

    return mean_absolute_error(
        actual_all,
        prediction_all
    )


def train_final_model(product_data):
    """
    Training model final menggunakan
    seluruh histori yang tersedia.
    """

    data = add_lag_features(
        product_data
    ).dropna()

    X = data[FEATURES]
    y = data["units_sold"]

    model = create_model()

    model.fit(
        X,
        y
    )

    return model


def main():

    print("=" * 60)
    print("FINAL TRAINING RANDOM FOREST")
    print("=" * 60)

    df = pd.read_csv(
        DATA_PATH
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    results = []

    for product_id in sorted(
        df["product_id"].unique()
    ):

        product_data = df[
            df["product_id"] == product_id
        ].copy()

        product_name = product_data[
            "product_name"
        ].iloc[0]

        # 1. Evaluasi
        mae = evaluate_model(
            product_data
        )

        # 2. Training final menggunakan
        # seluruh data
        final_model = train_final_model(
            product_data
        )

        # 3. Simpan model
        model_path = os.path.join(
            MODEL_DIR,
            f"{product_id}.joblib"
        )

        joblib.dump(
            final_model,
            model_path
        )

        results.append({
            "product_id": product_id,
            "product_name": product_name,
            "MAE": round(mae, 2),
            "model": model_path
        })

    results_df = pd.DataFrame(
        results
    )

    print("\nHasil Evaluasi:")

    print(
        results_df.to_string(
            index=False
        )
    )

    average_mae = results_df[
        "MAE"
    ].mean()

    print("\nRata-rata MAE:")
    print(
        round(
            average_mae,
            2
        )
    )

    print("\nModel tersimpan di:")

    print(
        MODEL_DIR
    )

    print("\n" + "=" * 60)
    print("FINAL TRAINING SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    main()