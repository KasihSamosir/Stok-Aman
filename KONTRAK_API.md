# Kontrak API StokAman

Dokumen ini berisi kesepakatan format data antara frontend, backend, model forecasting, model risk scoring, dan decision engine.

## 1. Alur Sistem

Frontend
↓
Backend
↓
Forecasting Model
↓
Risk Scoring Model
↓
Decision Engine
↓
Backend
↓
Frontend

## 2. Input Utama

Pengguna mengunggah 2 file:

### A. Sales Data

Berisi histori penjualan produk.

Kolom yang direncanakan:

- date
- product_id
- quantity

### B. Supplier Delivery Data

Berisi histori pengiriman supplier.

Kolom yang direncanakan:

- supplier_id
- order_date
- expected_delivery_date
- actual_delivery_date
- product_id

## 3. Output Forecasting

Forecasting menghasilkan prediksi kebutuhan produk.

Format awal:

- product_id
- forecast_quantity
- forecast_period

## 4. Output Risk Scoring

Risk scoring menghasilkan risiko keterlambatan supplier.

Format awal:

- supplier_id
- risk_score
- risk_level

Risk level:

- low
- medium
- high

## 5. Output Decision Engine

Decision engine menggabungkan hasil forecasting dan risk scoring.

Format awal:

- product_id
- forecast_quantity
- recommended_supplier
- risk_level
- recommendation

## 6. API Endpoint

Endpoint utama:

POST /predict

Input:
- sales CSV
- supplier delivery CSV

Output:
- forecast
- supplier risk
- recommendation

## 7. Catatan

Format di atas adalah rancangan awal dan dapat diperbarui setelah tim menyepakati dataset dan implementasi model.
