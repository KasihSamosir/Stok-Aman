from .features import create_supplier_features


def calculate_risk_score(late_rate, average_delay_days):
    """
    Menghitung risk score supplier dalam rentang 0 sampai 1.

    late_rate:
        Persentase pengiriman yang terlambat, 0 sampai 1.

    average_delay_days:
        Rata-rata jumlah hari keterlambatan.
    """

    # Normalisasi rata-rata keterlambatan.
    # 5 hari atau lebih dianggap sebagai tingkat keterlambatan maksimum.
    delay_score = min(average_delay_days / 5, 1)

    # Bobot:
    # 70% berdasarkan frekuensi terlambat
    # 30% berdasarkan lama keterlambatan
    risk_score = (
        (late_rate * 0.7)
        + (delay_score * 0.3)
    )

    return round(risk_score, 2)


def get_risk_level(risk_score):
    """
    Mengubah risk score menjadi kategori risiko.
    """

    if risk_score < 0.30:
        return "low"

    elif risk_score < 0.60:
        return "medium"

    else:
        return "high"


def get_recommendation(risk_level):
    """
    Memberikan rekomendasi berdasarkan risk level.
    """

    if risk_level == "low":
        return "Supplier memiliki tingkat risiko keterlambatan rendah."

    elif risk_level == "medium":
        return "Pertimbangkan supplier alternatif dan pantau kinerja supplier."

    else:
        return "Pertimbangkan supplier alternatif karena tingkat keterlambatan cukup tinggi."


def calculate_supplier_risk():
    features = create_supplier_features()

    results = []

    for _, supplier in features.iterrows():

        risk_score = calculate_risk_score(
            supplier["late_rate"],
            supplier["average_delay_days"]
        )

        risk_level = get_risk_level(risk_score)

        recommendation = get_recommendation(risk_level)

        results.append({
            "supplier_id": supplier["supplier_id"],
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation
        })

    return results


if __name__ == "__main__":
    results = calculate_supplier_risk()

    print("=== RISK SCORING ===")

    for result in results:
        print(result)