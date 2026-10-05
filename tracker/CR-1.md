---
id: CR-1
type: change-request
title: "Personas koda pārbaude iesniegumā"
status: READY
priority: high
reporter: "Reģistrācijas nodaļa (izdomāts)"
owner: "@<github-lietotājvārds>"
contract: "docs/openapi.yaml · POST /submissions · personalCode"
depends_on: []
exported: "2026-09-30 · Ezermalas pieteikumu sistēma (simulācija)"
data_check: "Nav personas datu, iekšējo adrešu vai pielikumu"
---

# CR-1 · Personas koda pārbaude iesniegumā

> Noteikumi vienkāršoti mācību vajadzībām.

## Apraksts (description)

Iesniegumos bieži ir nepareizi personas kodi. Sistēmai jāpārbauda, vai personas kods ir derīgs, un nederīgi iesniegumi jānoraida.

## Pieņemšanas kritēriji (acceptance criteria)

| # | Ievade | Sagaidāmais rezultāts |
|---|---|---|
| 1 | `32000000001` (11 cipari, jaunais formāts) | 201 |
| 2 | `320000-00001` (11 cipari, defise pēc 6. cipara) | 201, saglabāts `32000000001` (bez defises) |
| 3 | ` 320000 00001 ` (11 cipari ar atstarpēm) | 201, saglabāts `32000000001` (bez atstarpēm) |
| 4 | `3200000000` (10 cipari) | 400, `INVALID_FORMAT` |
| 5 | `320000000011` (12 cipari) | 400, `INVALID_FORMAT` |
| 6 | `32OOOOOOOO1` (burts O cipara 0 vietā) | 400, `INVALID_FORMAT` |
| 7 | `""` (neaizpildīts) vai lauka `personalCode` nav | 400, `REQUIRED` |
| 8 | `010190-10001` (vecā formāta sintētisks kods: derīgs datums un kontrolcipars) | 201, saglabāts `01019010001` |
| 9 | `3200-0000001` (defise nav pēc 6. cipara) | 400, `INVALID_FORMAT` |
| 10 | `010190-10002` (vecais formāts, nepareizs kontrolcipars) | 400, `INVALID_FORMAT` |
| 11 | `310290-10006` (vecais formāts, neeksistējošs datums 31.02.) | 400, `INVALID_FORMAT` |
| 12 | `39999999999` (jaunais formāts, otrais cipars 9) | 201 |
| 13 | `30000000001` (otrais cipars 0 → vecais formāts, datums 30.00. neeksistē) | 400, `INVALID_FORMAT` |
| 14 | `"   "` vai `"-"` (tikai atstarpes vai defise) | 400, `INVALID_FORMAT` |
| 15 | Derīgs kods ar defisi vai atstarpēm (piem., `320000-00001`) | OMD reģistram nosūtīts normalizēts kods `32000000001` |

## Precizējumi (clarifications)

| Jautājums | Atbilde | Kas atbildēja, kad |
|---|---|---|
| Kur drīkst būt defise? | Tikai pēc 6. cipara | Linda, 2026-10-05 |
| Kur drīkst būt atstarpes? | Jebkurā vietā, tās izņem | Linda, 2026-10-05 |
| Ko pārbauda vecajam formātam (DDMMGG-XNNNN)? | Formātu, datumu un kontrolciparu | Linda, 2026-10-05 |
| Kā atšķirt jauno formātu no vecā? | Jaunajam pirmais cipars ir `3`, otrais `2`–`9` | Linda, 2026-10-05 |
| Vai kods, kurā ir tikai atstarpes vai defise, ir `REQUIRED` vai `INVALID_FORMAT`? | `INVALID_FORMAT` | Linda, 2026-10-05 |
| Vai normalizēto kodu (bez defises un atstarpēm) sūta arī OMD reģistram? | Jā | Linda, 2026-10-05 |


## Ārpus tvēruma (out of scope)

- Pārbaude, vai persona eksistē reģistrā
- Ārvalstnieku identifikatori

## Komentāri (comments)

- 2026-09-28 · Reģistrācijas nodaļa: "Vakar 12 iesniegumi ar nepareizu kodu. Visi jālabo ar roku."
