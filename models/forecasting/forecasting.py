import os
import joblib
import pandas as pd


MODEL_DIR = "models/forecasting/saved_models"
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


def load_model(product_id):
    """
    Memuat model Random Forest berdasarkan product_id.
    """

    model_path = os.path.join(
        MODEL_DIR,
        f"{product_id}.joblib"
    )

    if not os.path.exists(model_path):
        raise ValueError(
            f"Model untuk produk {product_id} tidak ditemukan."
        )

    return joblib.load(model_path)


def validate_history(history):
    """
    Memastikan data histori memiliki format yang benar.
    """

    required_columns = [
        "date",
        "product_id",
        "units_sold"
    ]

    for column in required_columns:

        if column not in history.columns:
            raise ValueError(
                f"Kolom '{column}' tidak ditemukan."
            )

    if history.empty:
        raise ValueError(
            "Data histori kosong."
        )

    if history["units_sold"].isnull().any():
        raise ValueError(
            "Terdapat units_sold yang kosong."
        )

    if (history["units_sold"] < 0).any():
        raise ValueError(
            "units_sold tidak boleh negatif."
        )


def forecast_sales(product_id, history):
    """
    Memprediksi penjualan 7 hari ke depan.

    Parameters
    ----------
    product_id : str
        ID produk.

    history : pandas.DataFrame
        Histori penjualan produk.

        Wajib memiliki:
        - date
        - product_id
        - units_sold

        Minimal 14 hari histori.

    Returns
    -------
    dict
        Hasil forecast 7 hari.
    """

    if not isinstance(history, pd.DataFrame):

        raise TypeError(
            "history harus berupa pandas.DataFrame."
        )

    # Validasi awal
    validate_history(history)

    data = history.copy()

    # Konversi tipe data
    data["date"] = pd.to_datetime(
        data["date"]
    )

    data["units_sold"] = pd.to_numeric(
        data["units_sold"]
    )

    # Ambil produk yang diminta
    data = data[
        data["product_id"] == product_id
    ].copy()

    if data.empty:

        raise ValueError(
            f"Histori produk {product_id} tidak ditemukan."
        )

    # Urutkan berdasarkan tanggal
    data = (
        data
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Minimal histori
    if len(data) < 14:

        raise ValueError(
            "Minimal diperlukan 14 hari histori."
        )

    # Load model produk
    model = load_model(
        product_id
    )

    # Histori penjualan
    history_values = (
        data["units_sold"]
        .astype(float)
        .tolist()
    )

    # Tanggal terakhir
    last_date = data[
        "date"
    ].iloc[-1]

    forecasts = []

    # Forecast 7 hari
    for day in range(
        1,
        FORECAST_HORIZON + 1
    ):

        future_date = (
            last_date
            + pd.Timedelta(days=day)
        )

        features = pd.DataFrame([{
            "lag_1": history_values[-1],
            "lag_2": history_values[-2],
            "lag_3": history_values[-3],
            "lag_7": history_values[-7],
            "lag_14": history_values[-14],
            "day_of_week": future_date.dayofweek,
            "month": future_date.month,
        }])

        prediction = model.predict(
            features[FEATURES]
        )[0]

        # Penjualan tidak boleh negatif
        prediction = max(
            0,
            float(prediction)
        )

        prediction = round(
            prediction,
            2
        )

        forecasts.append({
            "date": future_date.strftime(
                "%Y-%m-%d"
            ),
            "predicted_units": prediction
        })

        # Prediksi hari ini digunakan sebagai
        # histori untuk prediksi hari berikutnya.
        history_values.append(
            prediction
        )

    # Total prediksi 7 hari
    total_forecast = round(
        sum(
            item["predicted_units"]
            for item in forecasts
        ),
        2
    )

    return {
        "product_id": product_id,
        "forecast_horizon": 7,
        "forecast": forecasts,
        "total_forecast": total_forecast
    }