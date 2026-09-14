# Użycie

`python app.py file --file obraz.iso --algorithm sha256`
`python app.py generate --root dane --manifest manifest.json`
`python app.py verify --root dane --manifest manifest.json --output reports`
`python app.py compare --manifest przed.json --other po.json`

Manifest zapisuj poza katalogiem badanym; nie nadpisuje istniejącego manifestu.
Symlinki i junctions są pomijane. Brak dostępu przerywa tworzenie, zamiast udawać kompletny manifest.
Porównanie bazuje na zawartości, nie samej dacie. Nie odczytuje ścieżek spoza jawnie wskazanego root.
Manifest nie jest podpisany; jego autentyczność zależy od bezpiecznego przechowywania.
