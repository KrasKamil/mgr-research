"""
Moduł ETL dla zbioru PKLot (Etap 1 potoku badawczego)
Praca magisterska: "Analiza i porównanie metod służących do predykcji zajętości miejsc parkingowych"
AGH, Teleinformatyka

Autor: Krask / Inicjalizacja potoku
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional


def parse_single_pklot_xml(xml_path: Path) -> Optional[Dict]:
    """
    Parsuje pojedynczy plik XML ze zbioru PKLot.
    
    Format ścieżki w PKLot:
    .../PKLot/<PARKING_LOT>/<WEATHER>/<DATE>/<YYYY-MM-DD_HH_MM_SS>.xml
    
    Zwraca słownik z metadanymi i obliczoną zajętością lub None w przypadku błędu.
    """
    try:
        # 1. Ekstrakcja znacznika czasu z nazwy pliku (np. '2012-09-12_06_05_16')
        timestamp = datetime.strptime(xml_path.stem, "%Y-%m-%d_%H_%M_%S")
        
        # 2. Odczyt metadanych ze struktury katalogów
        weather = xml_path.parent.parent.name      # Cloudy, Sunny, Rainy
        parking_lot = xml_path.parent.parent.parent.name  # PUCPR, UFPR04, UFPR05
        
        # 3. Parsowanie drzewa XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Każde miejsce parkingowe opisane jest węzłem <space id="..." occupied="0|1">
        spaces = root.findall("space")
        total_spaces = len(spaces)
        
        if total_spaces == 0:
            return None
            
        occupied_spaces = sum(1 for s in spaces if s.get("occupied") == "1")
        free_spaces = total_spaces - occupied_spaces
        occupancy_rate = (occupied_spaces / total_spaces) * 100.0  # w procentach [0-100%]
        
        return {
            "timestamp": timestamp,
            "parking_lot": parking_lot,
            "weather": weather,
            "total_spaces": total_spaces,
            "occupied_spaces": occupied_spaces,
            "free_spaces": free_spaces,
            "occupancy_rate": round(occupancy_rate, 2),
        }
    except Exception as e:
        print(f"[Ostrzeżenie] Błąd podczas parsowania pliku {xml_path.name}: {e}")
        return None


def extract_pklot_dataset(
    raw_data_dir: Path,
    parking_lots: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Przeszukuje katalog zbioru PKLot, parsuje pliki XML i tworzy uporządkowany DataFrame.
    
    :param raw_data_dir: Ścieżka bazowa do folderu PKLot (zawierającego podfoldery PUCPR, UFPR04, UFPR05).
    :param parking_lots: Opcjonalna lista parkingów do przetworzenia (np. ['PUCPR']). Jeśli None, parsuje wszystkie.
    :return: Posortowany chronologicznie DataFrame z ciągłymi szeregami czasowymi.
    """
    if parking_lots is None:
        target_dirs = [d for d in raw_data_dir.iterdir() if d.is_dir() and d.name in ["PUCPR", "UFPR04", "UFPR05"]]
    else:
        target_dirs = [raw_data_dir / lot for lot in parking_lots if (raw_data_dir / lot).is_dir()]
        
    records = []
    print(f"Rozpoczynam przeszukiwanie katalogów: {[d.name for d in target_dirs]}")
    
    for lot_dir in target_dirs:
        xml_files = list(lot_dir.glob("*/*/*.xml"))
        print(f" -> Parking {lot_dir.name}: Znaleziono {len(xml_files)} plików XML.")
        
        for file_path in xml_files:
            parsed = parse_single_pklot_xml(file_path)
            if parsed is not None:
                records.append(parsed)
                
    print(f"Łącznie poprawnie sparsowano {len(records)} klatek czasowych.")
    
    # Utworzenie DataFrame
    df = pd.DataFrame(records)
    
    # Sortowanie chronologiczne per parking
    df = df.sort_values(by=["parking_lot", "timestamp"]).reset_index(drop=True)
    
    return df


if __name__ == "__main__":
    # Domyślne ścieżki w repozytorium
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "PKLot" / "PKLot" / "PKLot"
    OUTPUT_CSV_PATH = BASE_DIR / "data" / "processed" / "pklot_occupancy_timeseries.csv"
    
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Katalog źródłowy: {RAW_DATA_PATH}")
    df_result = extract_pklot_dataset(RAW_DATA_PATH)
    
    # Zapis do CSV
    df_result.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Szereg czasowy zapisany pomyślnie w: {OUTPUT_CSV_PATH}")
    print("\nPierwsze 5 wierszy:")
    print(df_result.head())
