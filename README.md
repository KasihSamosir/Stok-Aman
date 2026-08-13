# StokAman

StokAman adalah sistem berbasis AI untuk membantu UMKM merencanakan kebutuhan stok dan memilih supplier berdasarkan risiko keterlambatan pengiriman.

## Problem

UMKM dapat mengalami dua masalah yang saling berkaitan:

1. Sulit memperkirakan kebutuhan stok pada periode berikutnya.
2. Sulit mengetahui supplier mana yang memiliki risiko keterlambatan lebih tinggi.

## Solution

StokAman menggabungkan dua komponen AI:

- **Forecasting** — memprediksi kebutuhan stok berdasarkan histori penjualan.
- **Risk Scoring** — menilai risiko keterlambatan supplier berdasarkan histori pengiriman.

Kedua hasil tersebut kemudian digunakan oleh decision engine untuk menghasilkan satu rekomendasi.

## System Flow

Sales Data + Supplier Delivery Data
↓
Forecasting + Risk Scoring
↓
Decision Engine
↓
Stock & Supplier Recommendation

## Project Structure

```text
Stok-Aman/
├── backend/
├── data/
├── frontend/
├── models/
│   ├── forecasting/
│   └── risk_scoring/
├── KONTRAK_API.md
└── README.md
