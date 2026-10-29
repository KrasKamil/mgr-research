# Przegląd Literatury – Praca Magisterska

**Tytuł:** Analiza i porównanie metod służących do predykcji zajętości miejsc parkingowych  
**Uczelnia:** Akademia Górniczo-Hutnicza w Krakowie (AGH)  
**Kierunek:** Teleinformatyka  

---

## Wykaz publikacji bazowych i źródeł danych

1. **Kim et al. (2025)**  
   *Real-Time Parking Space Management System Based on a Low-Power Embedded Platform*  
   Sensors, MDPI  
   Link: [https://www.mdpi.com/1424-8220/25/22/7009](https://www.mdpi.com/1424-8220/25/22/7009)  
   *Kluczowy wkład:* Projektowanie systemów czasu rzeczywistego, architektury embedded, ocena kosztu obliczeniowego i ograniczeń sprzętowych.

2. **Awan et al. (2020)**  
   *A Comparative Analysis of Machine/Deep Learning Models for Parking Space Availability Prediction*  
   Sensors, MDPI  
   Link: [https://www.mdpi.com/1424-8220/20/1/3223](https://www.mdpi.com/1424-8220/20/1/3223)  
   *Kluczowy wkład:* Porównanie modeli klasycznych ML z architekturami głębokimi (Deep Learning), metryki błędu (MAE, RMSE), wnioski dotyczące horyzontów predykcji.

3. **Avşar et al. (2022)**  
   *Parking lot occupancy prediction using long short-term memory and statistical methods*  
   Marmara Journal of Pure and Applied Sciences  
   Link: [https://dergipark.org.tr/en/pub/mjen/article/986631](https://dergipark.org.tr/en/pub/mjen/article/986631)  
   *Kluczowy wkład:* Bezpośrednie zestawienie metod statystycznych (ARIMA / SARIMA) z sieciami LSTM na danych parkingowych.

4. **Dahiya et al. (2025)**  
   *Hybrid parking space prediction model: integrating ARIMA, LSTM, and BPNN for smart city development*  
   PMC / PeerJ / Springer Nature  
   Link: [https://pmc.ncbi.nlm.nih.gov/articles/PMC11784715/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11784715/)  
   *Kluczowy wkład:* Modele hybrydowe, dekompozycja składowych liniowych (ARIMA) i nieliniowych (sieci neuronowe).

5. **Zeng et al. (2022)**  
   *Parking Occupancy Prediction Method Based on Multi Factors and Stacked GRU-LSTM*  
   IEEE Access  
   Link: [https://doi.org/10.1109/ACCESS.2022.31713306](https://doi.org/10.1109/ACCESS.2022.31713306)  
   *Kluczowy wkład:* Wykorzystanie architektur rekurencyjnych GRU i LSTM, wpływ czynników zewnętrznych (pogoda, pory dnia).

6. **Arjona et al. (2020)**  
   *Improving Parking Availability Information Using Deep Learning Techniques*  
   Transportation Research Procedia  
   Link: [https://doi.org/10.1016/j.trpro.2020.03.1137](https://doi.org/10.1016/j.trpro.2020.03.1137)  
   *Kluczowy wkład:* Praktyczne wdrożenia predykcji dostępności miejsc w systemach inteligentnego transportu (ITS).

7. **Mendeley Data (Dataset & Benchmark)**  
   *Time Series Decomposition + GRU (TSD-GRU)*  
   Mendeley Data  
   Link: [https://data.mendeley.com/datasets/nh2358f5mf/4](https://data.mendeley.com/datasets/nh2358f5mf/4)  
   *Kluczowy wkład:* Referencyjny zbiór szeregów czasowych zajętości parkingowej oraz kody benchmarkowe z dekompozycją szeregów.

8. **Zhao & Zhang (2024)**  
   *Enhancing Predictive Models for On-Street Parking Occupancy: Integrating Adaptive GCN and GRU*  
   Mathematics, MDPI  
   Link: [https://doi.org/10.3390/math12182823](https://doi.org/10.3390/math12182823)  
   *Kluczowy wkład:* Porównanie modeli GRU z grafowymi sieciami splotowymi w predykcji zajętości przestrzennej i czasowej.

---

## Zbiór danych: PKLot (Plan B)
- **Autorzy:** Almeida et al. (Federal University of Paraná & Pontifical Catholic University of Paraná, Brazylia)
- **Charakterystyka:** ~12 400 ujęć z kamer monitoringu trzech parkingów: PUCPR, UFPR04, UFPR05 w różnych warunkach pogodowych (Sunny, Cloudy, Rainy).
- **Zastosowanie w pracy:** Agregacja etykiet XML (stan poszczególnych miejsc parkingowych) w ciągły szereg czasowy zajętości procentowej.
