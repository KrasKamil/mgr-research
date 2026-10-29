# Analiza i porównanie metod służących do predykcji zajętości miejsc parkingowych

Projekt badawczy w ramach pracy magisterskiej (AGH, Teleinformatyka).

## Cel badań
Porównanie skuteczności, wydajności obliczeniowej (czas uczenia/inferencji, narzut zasobów) oraz trafności prognostycznej modeli:
1. **Naiwny Baseline** (Persistence / Last-Value / Historical Average)
2. **Model statystyczny** (ARIMA / SARIMA)
3. **Rekurencyjne sieci neuronowe** (Vanilla LSTM, Vanilla GRU)

na horyzontach predykcji: **15 min, 30 min, 60 min**.

## Struktura projektu
```text
mgr-research/
├── data/
│   ├── raw/             # Surowe dane (np. zbiór PKLot)
│   └── processed/       # Wygenerowane szeregi czasowe CSV
├── docs/
│   └── literature.md    # Zestawienie literatury naukowej i linków
├── models/              # Zapisane wagi wytrenowanych modeli
├── notebooks/           # Eksperymenty badawcze w Jupyter Notebook
├── src/                 # Kod źródłowy potoku (ETL, features, models)
├── requirements.txt     # Zależności biblioteczne
└── README.md
```

## Przegląd literatury
Szczegółowy wykaz publikacji bazowych i odnośników znajduje się w [docs/literature.md](docs/literature.md).
