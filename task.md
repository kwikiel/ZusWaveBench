Tak — benchmark powinien mieć **osobną warstwę “język polskiego urzędu”**, bo modele mylą nie tylko terminy, ale też **skutek prawny dokumentu**, **tryb zaskarżenia**, **relację obywatel–organ**, **formularze**, **skróty** i **lokalne idiomy kancelaryjno-podatkowe**.

Najważniejsza różnica: nie benchmarkuj tylko “czy model zna definicję słowa”, ale czy umie poprawnie rozwiązać **case urzędowy**.

## 1. Rdzeń pojęć administracyjnych — KPA / urząd / gmina / wojewoda

To jest najbardziej “polski urząd” core.

| Pojęcie                                   | Dlaczego trudne dla LLM                                                                                                       | Typowy test                                                         |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **decyzja administracyjna**               | Model musi wiedzieć, że rozstrzyga sprawę co do istoty albo kończy postępowanie; ma pouczenie, podstawę prawną, uzasadnienie. | “Czy od tego pisma przysługuje odwołanie?”                          |
| **postanowienie**                         | Często dotyczy kwestii proceduralnej, nie meritum; nie zawsze jest zaskarżalne.                                               | “Czy to kończy sprawę?”                                             |
| **zaświadczenie**                         | Nie jest decyzją; potwierdza stan faktyczny/prawny z danych organu. Modele często traktują je jak decyzję.                    | “Czy można zaskarżyć treść zaświadczenia jak decyzję?”              |
| **wezwanie**                              | Nie rozstrzyga sprawy, ale uruchamia obowiązek działania, np. uzupełnienia braków.                                            | “Co obywatel ma zrobić i jaki jest skutek braku reakcji?”           |
| **zawiadomienie**                         | Informuje o czynności/fakcie; nie zawsze tworzy obowiązek.                                                                    | “Czy trzeba składać odwołanie?”                                     |
| **odwołanie**                             | Środek od decyzji w toku instancji.                                                                                           | “Do kogo składa się odwołanie: organ I czy II instancji?”           |
| **zażalenie**                             | Środek typowo na postanowienia, ale tylko gdy przepis przewiduje.                                                             | “Czy na odmowę wydania zaświadczenia jest odwołanie czy zażalenie?” |
| **wniosek o ponowne rozpatrzenie sprawy** | Polski specyfik dla decyzji wydanych przez niektóre organy bez klasycznej II instancji.                                       | “Czy tu jest odwołanie, czy ponowne rozpatrzenie?”                  |
| **ostateczność decyzji**                  | Decyzja ostateczna ≠ prawomocna w sensie sądowym; modele mieszają.                                                            | “Czy ostateczna decyzja może być wzruszona?”                        |
| **rygor natychmiastowej wykonalności**    | Decyzja może być wykonywana mimo braku ostateczności.                                                                         | “Czy trzeba czekać na koniec odwołania?”                            |
| **bezczynność organu**                    | Brak załatwienia sprawy w terminie.                                                                                           | “Jakie pismo: ponaglenie, skarga, odwołanie?”                       |
| **przewlekłość postępowania**             | Organ działa, ale zbyt wolno/pozornie.                                                                                        | “Bezczynność czy przewlekłość?”                                     |
| **ponaglenie**                            | Kluczowy środek przed skargą na bezczynność/przewlekłość.                                                                     | “Co złożyć przed WSA?”                                              |
| **umorzenie postępowania**                | Postępowanie kończy się bez merytorycznego rozstrzygnięcia.                                                                   | “Czy organ odmówił, czy umorzył?”                                   |
| **odmowa wszczęcia postępowania**         | Inny skutek niż odmowa merytoryczna.                                                                                          | “Czy sprawa była badana co do meritum?”                             |
| **braki formalne**                        | Pismo może być poprawiane; brak uzupełnienia może zostawić sprawę bez rozpoznania.                                            | “Czy urząd powinien od razu odmówić?”                               |
| **strona postępowania**                   | Nie każdy zainteresowany jest stroną.                                                                                         | “Czy sąsiad ma interes prawny czy tylko faktyczny?”                 |
| **interes prawny vs interes faktyczny**   | Bardzo częsty fail modeli.                                                                                                    | “Czy osoba może żądać dopuszczenia do sprawy?”                      |
| **organ właściwy / niewłaściwy**          | Właściwość rzeczowa, miejscowa, instancyjna.                                                                                  | “Który urząd powinien rozpatrzyć sprawę?”                           |
| **milczące załatwienie sprawy**           | Nietypowy polski mechanizm: brak sprzeciwu organu może mieć skutek pozytywny.                                                 | “Czy brak odpowiedzi oznacza zgodę?”                                |

KPA jest dobrym źródłem kanonicznych pojęć: postępowanie administracyjne jest co do zasady dwuinstancyjne, a decyzje bez odwołania/ponownego rozpatrzenia stają się ostateczne; tekst KPA zawiera też klasyczne konstrukcje typu decyzja, postanowienie, odwołanie, zażalenie, ponaglenie i zaświadczenia. ([Isap][1])

## 2. Pojęcia “pismo urzędowe” — semantyka dokumentów

Tutaj benchmark powinien sprawdzać, czy model rozumie **typ dokumentu po jego treści**, nawet gdy nazwa jest myląca.

Przykłady klas:

| Dokument                                       | Co model musi rozpoznać                                            |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| **wezwanie do uzupełnienia braków formalnych** | To nie jest kara ani decyzja; trzeba uzupełnić konkretne elementy. |
| **wezwanie do złożenia wyjaśnień**             | Organ ma wątpliwości; odpowiedź powinna być rzeczowa, z dowodami.  |
| **informacja / zawiadomienie / obwieszczenie** | Często nie podlega odwołaniu.                                      |
| **decyzja odmowna**                            | Jest rozstrzygnięcie + pouczenie.                                  |
| **postanowienie o odmowie wszczęcia**          | Sprawa nie weszła w meritum.                                       |
| **postanowienie o zawieszeniu postępowania**   | Postępowanie nie jest zakończone.                                  |
| **zaświadczenie**                              | Potwierdzenie stanu; nie zastępuje decyzji.                        |
| **protokół**                                   | Utrwala czynność, nie rozstrzyga sam w sobie.                      |
| **urzędowe poświadczenie odbioru / UPO**       | Dowód doręczenia/złożenia, nie treść sprawy.                       |
| **pouczenie**                                  | Kluczowe: termin, tryb, organ, skutek zaniechania.                 |

Warto zrobić zadania typu: “Dostałem pismo. Zaklasyfikuj je jako decyzję/postanowienie/wezwanie/zaświadczenie/informację i powiedz, czy przysługuje odwołanie, zażalenie, ponaglenie, skarga do WSA albo nic.”

## 3. E-administracja: gov.pl, ePUAP, Profil Zaufany, e-Doręczenia, mObywatel

To jest bardzo polskie i bardzo benchmarkowalne.

| Pojęcie                                   | Typowy błąd modelu                                                  |
| ----------------------------------------- | ------------------------------------------------------------------- |
| **Profil Zaufany**                        | Model traktuje jak podpis kwalifikowany albo login bankowy.         |
| **ePUAP**                                 | Mieszanie skrzynki ePUAP z e-Doręczeniami.                          |
| **e-Doręczenia**                          | Mieszanie z e-mailem.                                               |
| **Mój GOV**                               | Mieszanie z mObywatel.                                              |
| **mObywatel**                             | Traktowanie jako pełny substytut dokumentu w każdej sytuacji.       |
| **podpis zaufany**                        | Mieszanie z podpisem osobistym i kwalifikowanym.                    |
| **podpis kwalifikowany**                  | Mieszanie z profilem zaufanym.                                      |
| **e-dowód**                               | Mieszanie dowodu osobistego jako dokumentu z warstwą elektroniczną. |
| **UPO**                                   | Model nie rozumie, że to dowód złożenia/doręczenia.                 |
| **ESP — elektroniczna skrzynka podawcza** | Rzadki skrót, dobry test lokalnej znajomości.                       |
| **skrzynka do doręczeń**                  | Inny reżim niż zwykła skrzynka mailowa.                             |

Przykład: usługi gov.pl dla PESEL/zameldowania prowadzą użytkownika przez Profil Zaufany i mogą generować zaświadczenie/dokument PDF; to jest bardzo dobry case, bo miesza dane rejestrowe, logowanie, skrzynkę i dokument urzędowy. ([Gov.pl][2])

## 4. Rejestry i identyfikatory państwowe

Tu modele często znają skrót, ale nie znają konsekwencji.

| Pojęcie                                                                | Test                                                                 |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **PESEL**                                                              | Czy identyfikuje osobę fizyczną, nie firmę?                          |
| **NIP**                                                                | Osoba/firma/podatnik; kiedy używany zamiast PESEL.                   |
| **REGON**                                                              | Statystyka publiczna, nie “numer podatkowy”.                         |
| **KRS**                                                                | Spółki, fundacje, stowarzyszenia, reprezentacja.                     |
| **CEIDG**                                                              | JDG, zawieszenie, wznowienie, pełnomocnik.                           |
| **BDO**                                                                | Odpady/opakowania; często mylone z bazą firm.                        |
| **CRBR**                                                               | Beneficjent rzeczywisty; ważne dla KYC/AML.                          |
| **EKRS / RDF**                                                         | Repozytorium dokumentów finansowych.                                 |
| **TERYT / SIMC / ULIC**                                                | Adresy administracyjne; rzadkie, ale używane w integracjach.         |
| **KW / księga wieczysta**                                              | Działy I–IV; hipoteka, właściciel, roszczenia.                       |
| **EGiB**                                                               | Ewidencja gruntów i budynków; działka, obręb, jednostka ewidencyjna. |
| **adres zameldowania vs adres zamieszkania vs adres korespondencyjny** | Bardzo częsty fail.                                                  |

Dobry benchmark: “Czy osoba prowadząca JDG ma KRS?” albo “Czy REGON wystarczy do zapłaty podatku?” albo “Czy adres zameldowania jest tym samym co rezydencja podatkowa?”

## 5. Podatki i urząd skarbowy — bardzo dobry benchmark lokalny

To jest chyba najłatwiejsze do wygenerowania z realnych pism.

| Pojęcie                                        | Dlaczego model się wyłoży                                                          |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| **PIT-28**                                     | Ryczałt; model myli z PIT-37.                                                      |
| **PIT-36 / PIT-36L / PIT-37 / PIT-38**         | Różne źródła dochodów.                                                             |
| **ryczałt od przychodów ewidencjonowanych**    | Podatek od przychodu, nie dochodu.                                                 |
| **zaliczka na podatek**                        | Modele mylą z podatkiem rocznym.                                                   |
| **wpłaty zaksięgowane na koncie podatnika**    | Klasyczne pismo US: “wykazane wpłaty niezgodne z kontem”.                          |
| **mikrorachunek podatkowy**                    | PIT/CIT/VAT zasadniczo na indywidualny rachunek.                                   |
| **symbol formularza płatności**                | Np. PIT-28, PIT-37, VAT-7 — istotne przy przelewie.                                |
| **okres rozliczeniowy**                        | Miesiąc/kwartał/rok; modele pomijają.                                              |
| **JPK_V7M / JPK_V7K**                          | Deklaracja + ewidencja VAT.                                                        |
| **KSeF**                                       | Faktury ustrukturyzowane, nie zwykły PDF.                                          |
| **czynny podatnik VAT / zwolniony z VAT**      | Modele mylą status z obowiązkiem wystawiania faktur.                               |
| **biała lista podatników VAT**                 | Rachunek bankowy kontrahenta, split payment.                                       |
| **mechanizm podzielonej płatności / MPP**      | VAT split, nie rabat.                                                              |
| **PCC**                                        | Czynności cywilnoprawne; mylone z VAT/PIT.                                         |
| **interpretacja indywidualna**                 | Nie jest “opinią urzędu” ogólną dla wszystkich.                                    |
| **czynny żal**                                 | Nie jest przeprosinami; ma warunki skuteczności.                                   |
| **zaległość podatkowa / nadpłata / odsetki**   | Modele mylą należność, wpłatę i zaksięgowanie.                                     |
| **wezwanie do wyjaśnień / korekta deklaracji** | Model powinien zaproponować korektę tylko jeśli błąd faktycznie jest w deklaracji. |

Ministerstwo Finansów wskazuje, że PIT, CIT i VAT opłaca się przez indywidualny rachunek podatkowy/mikrorachunek, a przy przelewie podatkowym ważne są m.in. kwota, okres i symbol formularza płatności. ([Podatki][3])

## 6. ZUS / ubezpieczenia społeczne

Bardzo dużo skrótów, świetne do “Polish bureaucratic reasoning”.

| Pojęcie                                           | Case                                            |
| ------------------------------------------------- | ----------------------------------------------- |
| **PUE ZUS / eZUS**                                | Konto i korespondencja z ZUS.                   |
| **ZUS DRA**                                       | Deklaracja rozliczeniowa.                       |
| **ZUS RCA / RSA / RPA**                           | Raporty imienne; modele często halucynują.      |
| **kod tytułu ubezpieczenia**                      | 05 10, 05 70 itd.; lokalna ezoteryka.           |
| **ulga na start**                                 | Bez składek społecznych, ale zdrowotna zostaje. |
| **preferencyjny ZUS**                             | Inny etap niż ulga na start.                    |
| **Mały ZUS Plus**                                 | Limit/przychód/dochód; modele upraszczają.      |
| **składka zdrowotna**                             | Zależna od formy opodatkowania.                 |
| **dobrowolne chorobowe**                          | Istotne dla zasiłku.                            |
| **zasiłek chorobowy / macierzyński / opiekuńczy** | Modele mieszają warunki.                        |
| **zaświadczenie A1**                              | Delegowanie/praca transgraniczna.               |
| **ZUS ZUA / ZZA / ZWUA**                          | Zgłoszenie/wyrejestrowanie.                     |

## 7. Praca, legalizacja pobytu, urząd wojewódzki

Jeśli benchmark ma sprawdzać LLM-y w polskich firmach, HR i compliance, to ten obszar jest złoty.

| Pojęcie                                                   | Test                                          |
| --------------------------------------------------------- | --------------------------------------------- |
| **zezwolenie na pracę typ A/B/C/D/E/S**                   | Czy model rozróżnia typy?                     |
| **oświadczenie o powierzeniu pracy cudzoziemcowi**        | Nie to samo co zezwolenie.                    |
| **powiadomienie o powierzeniu pracy obywatelowi Ukrainy** | Specjalny reżim.                              |
| **karta pobytu**                                          | Dokument pobytowy, nie “wiza”.                |
| **pobyt czasowy / stały / rezydent długoterminowy UE**    | Różne tryby.                                  |
| **stempel w paszporcie**                                  | Potwierdzenie złożenia wniosku, nie karta.    |
| **wojewoda / urząd wojewódzki**                           | Organ właściwy w wielu sprawach cudzoziemców. |
| **starosta / powiatowy urząd pracy**                      | Test właściwości organu.                      |
| **profil pomocy / status bezrobotnego**                   | Urzędowa kategoria, nie potoczne “bez pracy”. |

## 8. Samorząd, meldunek, USC, obywatel

| Pojęcie                                                | Case                                                                        |
| ------------------------------------------------------ | --------------------------------------------------------------------------- |
| **meldunek na pobyt stały / czasowy**                  | Nie jest własnością lokalu ani zgodą na najem.                              |
| **wymeldowanie administracyjne**                       | Postępowanie administracyjne, często dowodowe.                              |
| **akt urodzenia / małżeństwa / zgonu**                 | USC, odpis skrócony/zupełny/wielojęzyczny.                                  |
| **odpis aktu stanu cywilnego**                         | Nie “kopia dokumentu”.                                                      |
| **dowód osobisty / paszport**                          | Różne organy i tryby.                                                       |
| **zamieszkanie vs zameldowanie**                       | Jeden z najważniejszych testów.                                             |
| **opłata skarbowa**                                    | Płatna za czynność/pełnomocnictwo/zaświadczenie, nie każda opłata urzędowa. |
| **pełnomocnictwo szczególne / ogólne / PPS-1 / UPL-1** | Lokalne formularze, trudne dla LLM.                                         |
| **wniosek / zgłoszenie / deklaracja**                  | Różne skutki prawne.                                                        |

## 9. Budownictwo, nieruchomości, geodezja

To świetny “hard mode”, bo wymaga rozróżniania podobnych procedur.

| Pojęcie                                            | Typowy fail                                         |
| -------------------------------------------------- | --------------------------------------------------- |
| **pozwolenie na budowę**                           | Decyzja administracyjna.                            |
| **zgłoszenie robót budowlanych**                   | Nie to samo co pozwolenie; możliwy sprzeciw organu. |
| **brak sprzeciwu**                                 | Może pozwalać na rozpoczęcie robót.                 |
| **milcząca zgoda**                                 | Model myli z “urząd zapomniał”.                     |
| **WZ — warunki zabudowy**                          | Nie jest pozwoleniem na budowę.                     |
| **MPZP**                                           | Akt prawa miejscowego.                              |
| **EGiB**                                           | Rejestr danych gruntów/budynków.                    |
| **wypis i wyrys z rejestru gruntów**               | Dokument geodezyjny, nie akt własności.             |
| **podział nieruchomości**                          | Procedura administracyjna/geodezyjna.               |
| **użytkowanie wieczyste**                          | Polski relikt prawny, modele często nie ogarniają.  |
| **służebność przesyłu / gruntowa / osobista**      | Wysoka wartość dla benchmarku.                      |
| **księga wieczysta: dział I-O, I-Sp, II, III, IV** | Test głębokiego lokalnego rozumienia.               |

## 10. Zamówienia publiczne / BIP / JST

Jeżeli benchmark ma dotyczyć urzędów jako instytucji, dodaj:

| Pojęcie                                                                     | Case                                        |
| --------------------------------------------------------------------------- | ------------------------------------------- |
| **BIP**                                                                     | Oficjalny publikator informacji publicznej. |
| **informacja publiczna**                                                    | Nie wszystko jest informacją publiczną.     |
| **wniosek o dostęp do informacji publicznej**                               | Nie wymaga interesu prawnego.               |
| **JST**                                                                     | Gmina, powiat, województwo.                 |
| **rada gminy / wójt / burmistrz / prezydent miasta / starosta / marszałek** | Modele mylą kompetencje.                    |
| **uchwała / zarządzenie**                                                   | Organ kolegialny vs wykonawczy.             |
| **RIO**                                                                     | Regionalna izba obrachunkowa.               |
| **NIK**                                                                     | Kontrola państwowa.                         |
| **SIWZ / SWZ**                                                              | Stara/nowa terminologia w zamówieniach.     |
| **BZP / TED**                                                               | Publikatory zamówień.                       |
| **postępowanie krajowe / unijne**                                           | Progi i tryby.                              |
| **odwołanie do KIO**                                                        | Specjalny środek w zamówieniach.            |

## 11. Kategorie benchmarkowe, które bym zrobił

Nie rób jednego benchmarku “Polish bureaucracy”. Zrób **8 task families**:

### A. Document classification

Input: fragment pisma.
Output: typ dokumentu + skutek + następny krok.

Przykład:

> “Wzywa się Pana do uzupełnienia braków formalnych w terminie 7 dni pod rygorem pozostawienia podania bez rozpoznania.”

Model ma zwrócić:

```json
{
  "document_type": "wezwanie do uzupełnienia braków formalnych",
  "is_decision": false,
  "requires_action": true,
  "deadline_present": true,
  "likely_next_action": "uzupełnić wskazane braki w terminie",
  "appeal_applicable": "not normally; this is not a merits decision"
}
```

### B. Remedy selection

Input: obywatel opisuje sytuację.
Output: odwołanie / zażalenie / ponaglenie / skarga do WSA / korekta / wyjaśnienie / brak środka.

Przykłady:

| Case                                              | Poprawna klasa                                               |
| ------------------------------------------------- | ------------------------------------------------------------ |
| Decyzja odmowna z urzędu gminy                    | odwołanie                                                    |
| Postanowienie, na które przepis przewiduje środek | zażalenie                                                    |
| Urząd milczy po terminie                          | ponaglenie, potem skarga                                     |
| US prosi o wyjaśnienie wpłat                      | wyjaśnienie albo korekta, zależnie od stanu                  |
| Zaświadczenie ma inną treść niż oczekiwana        | nie klasyczne odwołanie od decyzji; trzeba znać tryb ochrony |

### C. Term disambiguation

Pary minimalne:

```text
zameldowanie ≠ zamieszkanie
zaświadczenie ≠ decyzja
odmowa wszczęcia ≠ odmowa merytoryczna
umorzenie ≠ oddalenie
ostateczna ≠ prawomocna
wniosek ≠ zgłoszenie ≠ deklaracja
PESEL ≠ NIP ≠ REGON
KRS ≠ CEIDG
Profil Zaufany ≠ podpis kwalifikowany
ePUAP ≠ e-Doręczenia
WZ ≠ pozwolenie na budowę
MPZP ≠ decyzja WZ
nadpłata ≠ zwrot ≠ zaliczka ≠ zaległość
```

### D. Form / symbol extraction

Model dostaje pismo albo opis i ma wyciągnąć:

```json
{
  "organ": "Naczelnik Urzędu Skarbowego ...",
  "case_reference": "...",
  "tax_form": "PIT-28",
  "tax_period": "2025",
  "amount_booked": "20109.00 PLN",
  "requested_action": "explain discrepancy or file correction",
  "deadline": "7 days",
  "risk": "possible mismatch between declared advance payments and tax account postings"
}
```

### E. Organ competence

Pytania typu:

| Sprawa               | Organ                                                            |
| -------------------- | ---------------------------------------------------------------- |
| dowód osobisty       | gmina                                                            |
| paszport             | wojewoda / punkt paszportowy                                     |
| karta pobytu         | wojewoda                                                         |
| PIT/VAT              | urząd skarbowy / KAS                                             |
| ZUS DRA              | ZUS                                                              |
| pozwolenie na budowę | starosta/prezydent miasta na prawach powiatu, zależnie od sprawy |
| WZ                   | wójt/burmistrz/prezydent miasta                                  |
| odpis aktu urodzenia | USC                                                              |

### F. Local abbreviation expansion

Hard benchmark skrótów:

```text
KPA, PPSA, KAS, US, UCS, IAS, ZUS, KRUS, NFZ, PUE, CEIDG, KRS, REGON, NIP,
PESEL, BDO, CRBR, UPO, UPP, ESP, ePUAP, PZ, eID, KSeF, JPK, MPP, WIS, WIA,
PIT, CIT, VAT, PCC, MDR, BIP, JST, RIO, SKO, WSA, NSA, KIO, SWZ, BZP, TED,
MPZP, WZ, EGiB, KW, ZRID, USC, TERYT, SIMC, ULIC
```

### G. Deadline reasoning

Modele często źle liczą terminy i nie rozumieją “dni robocze” vs “dni kalendarzowe”.

Testuj:

```text
7 dni od doręczenia
14 dni od dnia doręczenia decyzji
bez zbędnej zwłoki
nie później niż w terminie 7 dni
miesiąc / dwa miesiące w KPA
termin materialny vs procesowy
przywrócenie terminu
data nadania w placówce operatora
doręczenie elektroniczne / fikcja doręczenia
```

### H. Style transformation

Model ma przepisać pismo obywatela do urzędu:

* bez emocji,
* z faktami,
* z podstawą sprawy,
* z załącznikami,
* z żądaniem,
* bez halucynowania podstawy prawnej, jeśli jej nie zna.

To jest praktycznie bardzo wartościowe.

## 12. Proponowany zestaw “golden concepts” do pierwszej wersji benchmarku

Na MVP dałbym 120–200 pojęć, ale startowo top 50:

```text
decyzja administracyjna
postanowienie
zaświadczenie
wezwanie
zawiadomienie
obwieszczenie
odwołanie
zażalenie
ponaglenie
skarga do WSA
wniosek o ponowne rozpatrzenie sprawy
ostateczność decyzji
prawomocność
rygor natychmiastowej wykonalności
braki formalne
pozostawienie bez rozpoznania
umorzenie postępowania
odmowa wszczęcia postępowania
interes prawny
strona postępowania
pełnomocnik
opłata skarbowa
doręczenie
UPO
Profil Zaufany
ePUAP
e-Doręczenia
mObywatel
PESEL
NIP
REGON
KRS
CEIDG
BDO
CRBR
meldunek
adres zamieszkania
adres korespondencyjny
PIT-28
ryczałt
zaliczka na podatek
mikrorachunek podatkowy
JPK_V7
KSeF
czynny żal
nadpłata
zaległość podatkowa
ZUS DRA
kod tytułu ubezpieczenia
PUE ZUS
pozwolenie na budowę
zgłoszenie robót
WZ
MPZP
EGiB
księga wieczysta
```

## 13. Najlepszy format benchmarku

Nie rób tylko pytań typu “co to jest X?”. To będzie za łatwe i podatne na memorization.

Lepszy format:

```json
{
  "id": "PL-ADMIN-042",
  "domain": "tax",
  "task_type": "document_interpretation",
  "input": "Podczas weryfikacji PIT-28 za 2025 rok stwierdzono, że wykazane wpłaty zaliczek w poz. 236 są niezgodne z wpłatami na Pana koncie, zaksięgowane: 20109,00 zł. Proszę o analizę i wyjaśnienie...",
  "expected": {
    "document_type": "wezwanie do wyjaśnienia",
    "not_a_decision": true,
    "main_issue": "mismatch between declared advance payments and booked tax-account payments",
    "next_steps": [
      "compare PIT-28 declared amount with tax account postings",
      "verify transfer dates, symbols, tax period and microaccount",
      "file correction only if PIT value is wrong",
      "otherwise submit explanation with evidence"
    ],
    "wrong_answers": [
      "pay immediately without checking",
      "file appeal",
      "treat as tax decision",
      "assume debt exists solely because of the letter"
    ]
  }
}
```

## 14. Scoring

Najlepiej scoring hybrydowy:

```json
{
  "classification_accuracy": 0.25,
  "legal_effect_accuracy": 0.25,
  "next_action_accuracy": 0.25,
  "hallucination_penalty": 0.15,
  "terminology_precision": 0.10
}
```

Najważniejsze negatywne punkty:

* model wymyśla podstawę prawną,
* model mówi “odwołaj się”, gdy pismo nie jest decyzją,
* model myli zaświadczenie z decyzją,
* model każe zapłacić podatek, gdy pismo tylko prosi o wyjaśnienie,
* model nie rozpoznaje terminu,
* model nie odróżnia organu właściwego od niewłaściwego,
* model nie potrafi wskazać załączników/dowodów.

## 15. Krótka odpowiedź na Twoje pytanie: “specyficzne case’y czy ogólne case’y?”

Rób **oba**, ale w proporcji:

```text
70% specyficzne polskie case’y urzędowe
20% ogólne case’y administracyjne po polsku
10% adversarial/minimal pairs
```

Czyli nie “co to jest decyzja administracyjna?”, tylko:

> “Dostałem pismo z urzędu: ‘wzywa się do wyjaśnień’. Czy to znaczy, że mam zaległość podatkową, czy tylko urząd widzi niezgodność?”

Albo:

> “Urząd wydał zaświadczenie z inną treścią niż chciałem. Czy składam odwołanie od decyzji?”

Albo:

> “Mam adres zameldowania w Warszawie, ale mieszkam w Gdańsku. Który adres wpisuję jako adres zamieszkania?”

To są dokładnie te miejsca, gdzie model “zna polski”, ale nie zna **polskiej pragmatyki urzędowej**.

[1]: https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19600300168/U/D19600168Lj.pdf?utm_source=chatgpt.com "Kodeks postępowania administracyjnego - Akt prawny - Sejm"
[2]: https://www.gov.pl/web/gov/sprawdz-swoje-dane-w-rejestrze-pesel?utm_source=chatgpt.com "Sprawdź dane swoje lub swojego dziecka w rejestrze ..."
[3]: https://www.podatki.gov.pl/mikrorachunek-podatkowy/?utm_source=chatgpt.com "Mikrorachunek podatkowy"

