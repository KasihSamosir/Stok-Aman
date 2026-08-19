import pandas as pd

from forecasting import forecast_sales


def main():

    print("=" * 60)
    print("TEST FORECASTING SEMUA PRODUK")
    print("=" * 60)

    df = pd.read_csv(
        "data/processed_sales.csv"
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    for product_id in sorted(
        df["product_id"].unique()
    ):

        history = (
            df[
                df["product_id"] == product_id
            ]
            .sort_values("date")
            .tail(30)
            .copy()
        )

        result = forecast_sales(
            product_id=product_id,
            history=history
        )

        print(
            f"\n{product_id}"
        )

        print(
            f"Total forecast 7 hari: "
            f"{result['total_forecast']} unit"
        )

        for item in result["forecast"]:

            print(
                f"  {item['date']} -> "
                f"{item['predicted_units']} unit"
            )

    print("\n" + "=" * 60)
    print("SEMUA PRODUK BERHASIL DITES")
    print("=" * 60)


if __name__ == "__main__":
    main()


def test_invalid_input():

    print("\n")
    print("=" * 60)
    print("TEST ERROR HANDLING")
    print("=" * 60)

    # Data histori terlalu sedikit
    invalid_history = pd.DataFrame({
        "date": pd.date_range(
            "2026-07-20",
            periods=5
        ),
        "product_id": ["P01"] * 5,
        "units_sold": [20, 21, 19, 22, 20]
    })

    try:

        forecast_sales(
            product_id="P01",
            history=invalid_history
        )

        print(
            "ERROR: data invalid "
            "tidak ditolak."
        )

    except ValueError as error:

        print(
            "PASS: input tidak valid "
            "berhasil ditolak."
        )

        print(
            f"Pesan: {error}"
        )


if __name__ == "__main__":

    main()

    test_invalid_input()