"""
Moduł wizualizacji klatek ze zbioru PKLot
Inspirowany kodem z pracy inżynierskiej (ParkClassifier / cv2 overlay)
Praca magisterska: "Analiza i porównanie metod służących do predykcji zajętości miejsc parkingowych"
AGH, Teleinformatyka
"""

import cv2
import numpy as np
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt


def render_parking_frame(
    xml_path: Path,
    show_ids: bool = True,
    scale: float = 1.0
) -> Tuple[np.ndarray, dict]:
    """
    Odczytuje zdjęcie JPG i odpowiadający mu plik XML ze zbioru PKLot,
    nanosi obrysy miejsc parkingowych (zielony = wolne, czerwony = zajęte)
    oraz rysuje panel informacyjny w stylu inżynierki.
    
    :param xml_path: Ścieżka do pliku XML klatki PKLot.
    :param show_ids: Czy wyświetlać numery ID miejsc parkingowych.
    :param scale: Współczynnik skalowania obrazu (np. 0.8 dla mniejszych ekranów).
    :return: (obraz_bgr, slownik_ze_statystykami)
    """
    jpg_path = xml_path.with_suffix(".jpg")
    if not jpg_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku obrazu: {jpg_path}")
        
    img = cv2.imread(str(jpg_path))
    if img is None:
        raise ValueError(f"Nie udało się załadować obrazu: {jpg_path}")
        
    tree = ET.parse(xml_path)
    root = tree.getroot()
    spaces = root.findall("space")
    total_spaces = len(spaces)
    
    occupied_count = 0
    empty_count = 0
    
    # Rysowanie obrysów miejsc parkingowych
    for s in spaces:
        spot_id = s.get("id", "")
        is_occupied = s.get("occupied") == "1"
        
        # Kolory w BGR: Zielony dla wolnych, Czerwony dla zajętych
        if is_occupied:
            occupied_count += 1
            color = (0, 0, 255)
        else:
            empty_count += 1
            color = (0, 255, 0)
            
        # Odczyt punktów wielokąta (konturu) z XML
        contour = s.find("contour")
        if contour is not None:
            pts = [[int(pt.get("x")), int(pt.get("y"))] for pt in contour.findall("point")]
            pts_arr = np.array(pts, dtype=np.int32)
            cv2.polylines(img, [pts_arr], isClosed=True, color=color, thickness=2)
            
            if show_ids and len(pts) > 0:
                cx = sum(p[0] for p in pts) // len(pts)
                cy = sum(p[1] for p in pts) // len(pts)
                cv2.putText(img, spot_id, (cx - 8, cy + 4), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Obliczenie statystyk
    occupancy_rate = (occupied_count / total_spaces * 100.0) if total_spaces > 0 else 0.0
    parking_name = root.get("id", xml_path.parent.parent.parent.name).upper()
    timestamp_str = xml_path.stem.replace("_", " ", 1).replace("_", ":")

    # Panel informacyjny w stylu inżynierki (półprzezroczyste tło w lewym górnym rogu)
    overlay = img.copy()
    cv2.rectangle(overlay, (25, 20), (330, 115), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.75, img, 0.25, 0, img)
    cv2.rectangle(img, (25, 20), (330, 115), (120, 120, 120), 1)

    # Teksty w panelu
    cv2.putText(img, f"{parking_name} | {timestamp_str}", (35, 45), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, f"Wolne (Free): {empty_count} / {total_spaces}", (35, 75), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    cv2.putText(img, f"Zajetosc: {occupancy_rate:.1f}% ({occupied_count} aut)", (35, 102), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 1)

    if scale != 1.0:
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        
    stats = {
        "timestamp": timestamp_str,
        "parking_lot": parking_name,
        "total": total_spaces,
        "occupied": occupied_count,
        "empty": empty_count,
        "occupancy_rate": occupancy_rate
    }
    return img, stats


def show_in_notebook(img_bgr: np.ndarray, figsize: Tuple[int, int] = (12, 8)):
    """Wyświetla obraz BGR bezpośrednio wewnątrz komórki Jupyter Notebook za pomocą Matplotlib."""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=figsize)
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def show_in_window(img_bgr: np.ndarray, window_name: str = "Podglad PKLot"):
    """Wyświetla obraz w natywnym oknie OpenCV z możliwością zamknięcia klawiszem 'q' lub ESC."""
    cv2.imshow(window_name, img_bgr)
    print("Naciśnij dowolny klawisz (lub 'q') w oknie z obrazem, aby je zamknąć...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Testowe wywołanie dla przykładowej klatki
    base_dir = Path(__file__).resolve().parent.parent
    sample_xml = base_dir / "data" / "raw" / "PKLot" / "PKLot" / "PKLot" / "PUCPR" / "Sunny" / "2012-09-11" / "2012-09-11_15_16_58.xml"
    
    if sample_xml.exists():
        rendered_img, stats = render_parking_frame(sample_xml, show_ids=True)
        print("Statystyki klatki:", stats)
        output_preview = base_dir / "data" / "processed" / "sample_annotated_frame.jpg"
        cv2.imwrite(str(output_preview), rendered_img)
        print(f"Zapisano wygenerowany podgląd do: {output_preview}")
    else:
        print(f"Nie znaleziono przykładowego pliku: {sample_xml}")
