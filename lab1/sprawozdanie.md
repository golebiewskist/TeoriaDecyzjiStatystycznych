# Laboratorium 1: Podstawy pracy z agentem

**Repozytorium:** https://github.com/golebiewskist/TeoriaDecyzjiStatystycznych 
**Środowisko:** Antigravity · Gemini 3.8 Flash (Medium)
**Końcowy raport:** project/results/exercise-summary.json

---

## 1. Zlecenie, granice i kryteria odbioru

Pracę rozpocząłem w katalogu projektu `C:\Users\goleb\OneDrive - Wojskowa Akademia Techniczna\TeoriaDecyzjiStatystycznych\lab1\project`. Na wstępie zleciłem agentowi przeanalizowanie pliku `README.md` oraz wyjaśnienie, czym zajmuje się skrypt `describe_data.py`. Ustaliłem, że celem jest wygenerowanie raportu podsumowującego dla danych ćwiczeniowych w pliku `results/exercise-summary.json`.

Określiłem wyraźne granice: w pierwszym etapie skupiliśmy się na weryfikacji środowiska i uruchomieniu bez wprowadzania jakichkolwiek modyfikacji w kodzie, danych czy testach. Dozwolona zmiana danych (edycja jednej etykiety w CSV) nastąpiła dopiero w etapie drugim.

Podczas odbioru zależało mi na weryfikacji rzeczywistego wykonania zadania, a nie tylko deklaracji modelu. Poprosiłem agenta o przedstawienie dowodów:
- użytego narzędzia i uruchomionej komendy w powłoce systemowej,
- zwróconego kodu błędu/sukcesu procesu oraz wyjścia konsoli,
- pełnej zawartości utworzonego pliku JSON z interpretacją liczb,
- wyniku uruchomienia gotowego testu jednostkowego z README.

---

## 2. Jak powstał raport i interpretacja liczebności

Raport powstał w wyniku fizycznego wywołania polecenia na moim lokalnym komputerze z systemem Windows (a nie w odciętym środowisku chmurowym). Agent wykorzystał swoje wbudowane narzędzie `run_command`, które przekazało komendy do lokalnego terminala PowerShell.

- **Środowisko:** Lokalny interpreter `Python 3.14.0` (ścieżka: `AppData\Local\Programs\Python\Python314\python3.14t.exe`).
- **Plik wejściowy:** `project/data/exercise.csv`
- **Wykonane polecenie:**
  ```powershell
  py -3 describe_data.py --data data/exercise.csv --out results/exercise-summary.json
  ```
- **Wynik procesu:** Kod zakończenia `0` (sukces), terminal wypisał informację o zapisie pliku oraz: `Messages: 8; labels: {'ham': 5, 'spam': 3}`.

W wygenerowanym raporcie ([link](project/results/exercise-summary.json)) znalazło się łącznie **8 wiadomości** (`total_messages`):
- `ham`: 5 (wiadomości pożądane),
- `spam`: 3 (niechciana poczta).

W rozmowie przeanalizowaliśmy też podgląd pojedynczej wiadomości `exercise-001`. Ustaliłem, że pole `text` może być wielowierszowe (dlatego skrypt korzysta z `csv.DictReader`, a nie prostego liczenia linii w pliku), a program nie klasyfikuje samemu treści ani nie trenuje modelu – jedynie odczytuje i zlicza istniejące etykiety z kolumny `label`.

---

## 3. Wyjaśnienie fragmentu kodu i mały przypadek (quiz)

W sesji poprosiłem agenta o szczegółowe wyjaśnienie 4 pierwszych linii funkcji `describe` w pliku `describe_data.py`:

```python
raw = input_path.read_bytes()
rows = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
if rows.fieldnames != ["message_id", "text", "label"]:
    raise ValueError("Expected columns: message_id,text,label.")
```

**Moje wyjaśnienie:**  
Zrozumiałem, że odczyt w postaci surowych bajtów (`read_bytes()`) jest potrzebny do obliczenia niezmiennego skrótu SHA-256 z pliku na dysku. Następnie bajty są dekodowane do tekstu UTF-8 i przekazywane przez wirtualny strumień w pamięci (`io.StringIO`) do `csv.DictReader` z flagą `newline=""`, co zapobiega zepsuciu podziałów wierszy wewnątrz wiadomości e-mail. Na koniec warunek `if` weryfikuje nagłówki – jeśli w CSV brakuje którejś kolumny, są dodatkowe pola lub kolejność jest inna, program natychmiast przerywa działanie zgłaszając `ValueError`.

**Mały przypadek sprawdzający:**  
Poprosiłem agenta o zagadkę dotyczącą działania pętli zliczającej. Agent podał mi miniaturowy zbiór CSV składający się z 3 wierszy (identyfikatory `msg-101`, `msg-102`, `msg-103` z etykietami kolejno: `ham`, `spam`, `ham`) i zapytał mnie o wynik.

- **Moje przewidywanie:** Wpisałem na czacie odpowiedź: `1: 3 2: spam: 1 ham: 2`.
- **Weryfikacja i wniosek:** Moje przewidywanie było w 100% trafne. Agent potwierdził to prześledzeniem pętli krok po kroku (dodawanie do `seen_ids` i inkrementacja słownika `counts`). Przeanalizowaliśmy też przypadek brzegowy: gdyby `msg-101` pojawił się drugi raz, program natychmiast wyrzuciłby wyjątek o duplikacie identyfikatora (`duplicate message_id`), nie tworząc raportu.

---

## 4. Wynik gotowego testu

W ramach weryfikacji agent uruchomił zestaw testów poleceniem z README:
```powershell
py -3 -m unittest discover -s tests -v
```

Test `test_cli_writes_expected_counts` w pliku `tests/test_report.py` zakończył się sukcesem:
```text
Ran 1 test in 0.334s
OK
```

W sesji wyjaśniliśmy działanie tego testu: test w ogóle **nie sprawdza naszego pliku `results/exercise-summary.json` ani zbioru `exercise.csv`**. Zamiast tego uruchamia `describe_data.py` na osobnym, syntetycznym pliku testowym `tests/fixtures/messages.csv` (zawierającym 3 spreparowane wiadomości) do tymczasowego folderu i sprawdza, czy skrypt generuje dokładnie `total: 3`, `ham: 2`, `spam: 1`. Test dowodzi jedynie, że mechanizm CLI i formatowanie JSON działają sprawnie.

---

## 5. Modyfikacja danych w Etapie 2

W drugim etapie poleciłem agentowi zmianę etykiety pierwszej wiadomości w `project/data/exercise.csv`:
- `message_id`: `exercise-001`
- Etykieta przed zmianą: `ham`
- Etykieta po zmianie: `spam`

Po wykonaniu tej edycji zapytałem agenta, czy dotychczasowy raport w `results/exercise-summary.json` nadal dobrze opisuje te dane. Ustaliliśmy wspólnie, że:
1. **Dotychczasowy raport stał się nieaktualny**, ponieważ jest jedynie statycznym zrzutem danych z momentu uruchomienia i nie aktualizuje się automatycznie.
2. Zmieniła się zawartość pliku, więc zmianie ulegnie również jego suma kontrolna `input_sha256`.
3. Aby uzyskać aktualny wynik, konieczne jest ponowne wywołanie komendy `describe_data.py` w terminalu i zweryfikowanie nowego pliku JSON oraz kodu wyjścia `0`.

**Porównanie liczebności:**
Zgodnie z przewidywaniem, po zamianie jednej wiadomości `ham` na `spam`:
- `ham` zmniejszyło się z 5 na **4**,
- `spam` zwiększyło się z 3 na **4**,
- łączna liczba wiadomości `total` pozostała bez zmian (**8**).