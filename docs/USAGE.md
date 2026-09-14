# Użycie

`python app.py file --file obraz.iso --algorithm sha256`
`python app.py generate --root dane --manifest manifest.json`
`python app.py verify --root dane --manifest manifest.json --output reports`
`python app.py compare --manifest przed.json --other po.json`

Manifest zapisuj poza katalogiem badanym; nie nadpisuje istniejącego manifestu.
Symlinki i junctions są pomijane. Brak dostępu przerywa tworzenie, zamiast udawać kompletny manifest.
Porównanie bazuje na zawartości, nie samej dacie. Nie odczytuje ścieżek spoza jawnie wskazanego root.
Manifest nie jest podpisany; jego autentyczność zależy od bezpiecznego przechowywania.

## Rozszerzenia 0.2.0

`python app.py compare-folders --root "C:/pierwszy" --other "C:/drugi" --algorithm sha256`
porównuje względne ścieżki i hashe, pokazując nowe, brakujące, zmienione i identyczne pliki.
Różnice zwracają kod 2. Operacja wyłącznie odczytuje oba katalogi.
