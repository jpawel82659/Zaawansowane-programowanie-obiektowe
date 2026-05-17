import asyncio
import random
from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, List

class IHealable(ABC):
    @abstractmethod
    def heal(self, amount: int):
        pass


class GameEventManager:
    on_death_callbacks: List[Callable[[str], None]] = []

    @staticmethod
    def trigger_death(character_name: str):
        for callback in GameEventManager.on_death_callbacks:
            callback(character_name)

class Character:
    total_characters_created = 0

    def __init__(self, name: str, hp: int, armor: int):
        self.name = name
        self._hp = hp
        self.max_hp = hp
        self.armor = armor
        self.is_alive = True
        Character.total_characters_created += 1

    @staticmethod
    def get_game_rules():
        return """
        === ZASADY GRY ===
        1. Nie zgiń!
        2. Walka turowa: Masz 1 akcję w turze, potem wpisz !end.
        3. Bilbo automatycznie atakuje, gdy inny członek drużyny zaatakuje!
        4. Zabij Smauga!
        5. Komenda !a{nazwa postaci} atakuje fizycznie.
        6. Komenda !fireball - Gandalf rzuca potężną kulę ognia!
        7. 10 Armora to -1 przyjętych obrażeń.
        """

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, value)
        if self._hp == 0 and self.is_alive:
            self.is_alive = False
            GameEventManager.trigger_death(self.name)

    def take_damage(self, amount: int) -> int:
        dmg_reduction = self.armor // 10
        final_dmg = max(0, amount - dmg_reduction)
        self.hp -= final_dmg
        return final_dmg

    async def perform_action(self, target):
        pass



class Hobbit(Character, IHealable):
    def __init__(self, name: str, hp: int, armor: int):
        super().__init__(name, hp, armor)

    async def perform_action(self, target: Character):
        dmg = random.randint(0, 10)
        dealt = target.take_damage(dmg)
        print(f" {self.name} dźga Żądełkiem! {target.name} traci {dealt} HP.")
        await asyncio.sleep(0.5)

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} zjada lembas i leczy {amount} HP! (Obecnie: {self.hp} HP)")



class Krasnolud(Character, IHealable):
    def __init__(self, name: str, hp: int, armor: int):
        super().__init__(name, hp, armor)

    async def perform_action(self, target: Character):
        dmg = random.randint(20, 40)
        dealt = target.take_damage(dmg)
        print(f"{self.name} uderza toporem! {target.name} traci {dealt} HP.")
        await asyncio.sleep(0.5)

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} pije piwo i leczy {amount} HP! (Obecnie: {self.hp} HP)")



class Mag(Character):
    def __init__(self, name: str, hp: int, armor: int, mana: int):
        super().__init__(name, hp, armor)
        self.mana = mana

    async def perform_action(self, target: Character):
        dmg = random.randint(20, 35)
        dealt = target.take_damage(dmg)
        print(f"{self.name} atakuje kosturem i {target.name} traci {dealt} HP.")
        await asyncio.sleep(0.5)

    async def cast_fireball(self, target: Character):
        if self.mana >= 115:
            self.mana -= 115
            dealt = target.take_damage(200)
            print(f"{self.name} rzuca KULĘ OGNIA! {target.name} traci potężne {dealt} HP!")
            await asyncio.sleep(0.5)
            return True
        return False



class Dragon(Character):
    def __init__(self, name: str, hp: int, armor: int):
        super().__init__(name, hp, armor)

    #target na druzyne pierscienia
    async def perform_action(self, party):
        alive_members = [m for m in party.members if m.is_alive]
        if not alive_members:
            return

        attack_type = random.choice(["pazur", "zioniecie"])

        if attack_type == "pazur":
            target = random.choice(alive_members)
            dealt = target.take_damage(30)
            print(f"{self.name} uderza payurem w {target.name} zadając {dealt} obrażeń!")
        else:
            print(f"{self.name} zieje ogniem na całą drużynę!")
            for target in alive_members:
                dealt = target.take_damage(10)
                print(f"   -> {target.name} otrzymuje {dealt} obrażeń.")
        await asyncio.sleep(1)




T = TypeVar('T', bound=Character)


class Party(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self.members: List[T] = []

    def __add__(self, character: T):
        self.members.append(character)
        return self

    def __getitem__(self, index: int) -> T:
        return self.members[index]

    def has_alive_members(self) -> bool:
        return any(m.is_alive for m in self.members)

    def print_status(self):
        print(f"\n--- Status drużyny: {self.name} ---")
        for m in self.members:
            status = f"HP: {m.hp}/{m.max_hp}" if m.is_alive else "MARTWY"
            mana_str = f" | Mana: {m.mana}" if isinstance(m, Mag) else ""
            print(f"[{m.name}] {status}{mana_str}")
        print("---------------------------------------")

    def analyze_team(self):
        print("\n--- Refleksja: Analiza drużyny ---")
        for m in self.members:
            klasa = type(m).__name__
            czy_leczy = issubclass(type(m), IHealable)
            print(f"{m.name} to {klasa}. Posiada leczenie? {'Tak' if czy_leczy else 'Nie'}")
        print("-------------------------------------\n")


#gra
async def main():
    print(Character.get_game_rules())

    GameEventManager.on_death_callbacks.append(
        lambda name: print(f"\n {name} poległ na polu bitwy! \n")
    )

    bilbo = Hobbit("Bilbo", hp=100, armor=20)
    gimli = Krasnolud("Gimli", hp=120, armor=50)
    gandalf = Mag("Gandalf", hp=100, armor=0, mana=100)
    smaug = Dragon("Smaug", hp=300, armor=70)


    my_party = Party[Character]("Drużyna Pierścienia")
    my_party = my_party + bilbo + gimli + gandalf


    my_party.analyze_team()

    tura = 1

    while smaug.is_alive and my_party.has_alive_members():
        print(f"\n=========== TURA {tura} ===========")
        my_party.print_status()
        print(f"[Smaug] HP: {smaug.hp}/300 | Pancerz: 70")


        if gandalf.is_alive:
            gandalf.mana += 5

        action_used = False


        while True:

            cmd = await asyncio.to_thread(input, "Wpisz komendę: ")
            cmd = cmd.strip().lower()

            if cmd == "!end":
                if not action_used:
                    print("Pominąłeś akcję w tej turze.")
                break

            elif cmd == "!mana":
                if gandalf.is_alive:
                    print(f"Gandalf posiada {gandalf.mana} punktów many.")
                else:
                    print("Gandalf nie żyje...")

            elif not action_used:

                attack_performed = False

                if cmd == "!abilbo" and bilbo.is_alive:
                    await bilbo.perform_action(smaug)
                    action_used = True


                elif cmd == "!agimli" and gimli.is_alive:
                    await gimli.perform_action(smaug)
                    action_used = True
                    attack_performed = True

                elif cmd == "!agandalf" and gandalf.is_alive:
                    await gandalf.perform_action(smaug)
                    action_used = True
                    attack_performed = True

                elif cmd == "!fireball" and gandalf.is_alive:
                    if gandalf.mana >= 115:
                        sukces = await gandalf.cast_fireball(smaug)
                        if sukces:
                            action_used = True
                            attack_performed = True
                    else:
                        print(f"Brakuje many! (Jest {gandalf.mana}, Potrzeba 115)")

                elif cmd == "!hbilbo" and bilbo.is_alive:
                    bilbo.heal(30)
                    action_used = True

                elif cmd == "!hgimli" and gimli.is_alive:
                    gimli.heal(30)
                    action_used = True

                else:
                    print("Niewłaściwa komenda, postać nie żyje, lub komenda nie istnieje.")

                if attack_performed and bilbo.is_alive:
                    print(f"[Pasywka] {bilbo.name} wykorzystuje zamieszanie i poprawia cios!")
                    await bilbo.perform_action(smaug)

                if action_used:
                    print("Akcja wykonana! Wpisz !end aby przejść do tury Smauga.")

            else:
                print("Wykorzystałeś już akcję w tej turze! Wpisz !end")

        if smaug.is_alive:
            print("\n--- TURA PRZECIWNIKA ---")
            await smaug.perform_action(my_party)

        tura += 1
    #ending
    print("\n==================================")
    if not smaug.is_alive:
        print("ZWYCIĘSTWO! Smaug został pokonany!")
    else:
        print("PORAŻKA! Drużyna Pierścienia uległa Smaugowi...")
    print("==================================")

#run app
if __name__ == "__main__":
    asyncio.run(main())