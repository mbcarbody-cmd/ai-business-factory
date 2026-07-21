# Ride Recorder Android MVP

Tikslas: ne demo, o lokaliai telefone veikiantis kelionės įrašymo produktas.

## Pirmo veikiančio leidimo kriterijai

- Android telefone prašo GPS leidimo;
- pradeda foreground GPS įrašymą;
- rodo esamą greitį;
- skaičiuoja atstumą ir kelionės laiką;
- rodo maksimalų greitį ir GPS taškų skaičių;
- sustabdžius išsaugo realų GPX failą;
- GPX galima pasidalinti / atidaryti kitoje žemėlapių programoje;
- veikia išjungus ekraną;
- jokio serverio ar registracijos.

## Toliau po patvirtinto MVP

1. Žemėlapis su realia maršruto linija.
2. Kelionių istorija telefone.
3. Pagreitėjimo ir stabdymo įvykiai.
4. Aukštis, vidutinis greitis, sustojimų laikas.
5. Vaizdo įrašymas ir telemetry overlay.
6. Mokamas Pro eksportas, pažangi statistika ir cloud backup.

## Build

Atidaryti `apps/ride-recorder-android` su Android Studio, palaukti Gradle sync ir paleisti fiziniame Android telefone. Emulatorius netinka realiam GPS važiavimo testui.
