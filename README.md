# Autor: Paweł Jurek 82659

# Drużyna Pierścienia vs Smaug - Terminal RPG

Konsolowa gra RPG napisana w języku Python. Gracz przejmuje kontrolę nad Drużyną Pierścienia i staje do turowej walki z potężnym smokiem Smaugiem. 

Projekt powstał w celach edukacyjnych jako praktyczna demonstracja zaawansowanych mechanizmów programowania obiektowego (OOP) oraz programowania asynchronicznego.

---

## Zasady Gry
1. **Cel:** Pokonaj Smauga, zanim on pokona Twoją drużynę.
2. **System Turowy:** W swojej turze możesz wykonać tylko **jedną akcję** (atak lub leczenie). Po wykonaniu akcji należy wpisać `!end`, aby oddać turę przeciwnikowi.
3. **Pancerz (Armor):** Każde 10 punktów pancerza redukuje otrzymywane obrażenia o 1 punkt.
4. **Zdolność Pasywna Hobbita:** Za każdym razem, gdy dowolny inny członek drużyny wykona atak, Bilbo automatycznie wykonuje darmowy, dodatkowy cios.
5. **Mana:** Gandalf regeneruje 5 punktów many co turę. Potężne zaklęcia wymagają zgromadzenia odpowiedniej ilości many.

---

## Dostępne Komendy
Podczas tury gracza, system oczekuje na wpisanie jednej z poniższych komend:

* `!abilbo` - Atak fizyczny Bilba (Żądełko).
* `!agimli` - Atak fizyczny Gimliego (Topór).
* `!agandalf` - Atak fizyczny Gandalfa (Kostur).
* `!hbilbo` - Leczenie Bilba (zjada lembas, odnawia 30 HP).
* `!hgimli` - Leczenie Gimliego (pije piwo, odnawia 30 HP).
* `!mana` - Wyświetla aktualny stan many Gandalfa (nie zużywa akcji).
* `!fireball` - Gandalf rzuca Kulę Ognia zadającą potężne obrażenia (zużywa 115 many).
* `!end` - Kończy turę gracza i inicjuje losowy atak Smauga.

---

## Zaimplementowane Mechanizmy (Wymagania Projektowe)

Kod źródłowy gry zawiera implementację 12 kluczowych zagadnień z zakresu programowania:

1. **Klasy:** Struktura oparta na klasach (m.in. `Character`, `Hobbit`, `Dragon`, `Party`).
2. **Konstruktory:** Inicjalizacja atrybutów postaci (HP, Armor) w metodach `__init__`.
3. **Właściwości / Indeksatory:** Kontrola przypisywania punktów życia poprzez dekoratory `@property` i `@hp.setter`. Dostęp do członków drużyny zrealizowany metodą `__getitem__`.
4. **Elementy Statyczne:** Zmienna klasowa `total_characters_created` zliczająca instancje oraz metoda statyczna `get_game_rules()`.
5. **Dziedziczenie:** Hierarchia klas postaci dziedziczących po bazowej klasie `Character`.
6. **Polimorfizm:** Różne zachowania postaci wywoływane tą samą metodą `perform_action()`.
7. **Interfejsy / Abstrakcja:** Klasa abstrakcyjna `IHealable` wymuszająca implementację metody `heal()`.
8. **Typy ogólne / Kolekcje:** Bezpieczna typologicznie kolekcja postaci zrealizowana przez `Generic[T]` i `TypeVar`.
9. **Delegacje / Zdarzenia:** Mechanizm `GameEventManager` wyzwalający odpowiednie funkcje (wzorzec Obserwator) w momencie śmierci postaci.
10. **Przeciążanie operatorów:** Możliwość dodawania postaci do drużyny za pomocą operatora `+` (metoda `__add__`).
11. **Programowanie asynchroniczne:** Pętla gry i ataki działające w sposób nieblokujący z wykorzystaniem biblioteki `asyncio` (`async`/`await`).
12. **Refleksja:** Dynamiczna analiza zdolności klas w trakcie działania programu (sprawdzanie obecności interfejsu leczącego) zrealizowana w metodzie `analyze_team()`.

Dodatkowo na ocenę **BDB**:
13. **Enkapsulacja**: Zastosowanie `_hp`
14. **Wyrażenia listowe**: W klasie `Dragon` podczas losowania celu ataku: `alive_members = [m for m in party.members if m.is_alive]`.
15. **Adnotacje typów**: Zastosowanie statyczne typowanie, zadeklarowane zmienne, które nie są wymagane w Pythonie (np. `hp: int`).
---

## Jak uruchomić projekt?

Do uruchomienia gry wymagany jest zainstalowany interpreter **Python w wersji 3.7 lub nowszej** (biblioteka 'asyncio').

Aby uruchomić grę w swoim środowisku wykonaj następujące kroki:

1. Otwórz aplikację **Command Prompt** (cmd) lub **PowerShell**.
2. Przejdź do katalogu, w którym znajduje się plik z kodem (używając polecenia `cd`).
3. Wpisz poniższą komendę i zatwierdź klawiszem Enter:

```bash
python main.py