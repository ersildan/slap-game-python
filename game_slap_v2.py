from rich.console import Console
from rich.panel import Panel
import random

console = Console()


class Unit:

    def __init__(self, name='Юнит', hp=10):
        self.name = name
        self.hp = hp

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp

    def is_alive(self):
        return self.hp > 0

    def get_status(self):
        return f"[green]{self.name}: {self.hp} здоровья[/green]\n"


class GameLogic:

    @staticmethod
    def roll_dice(sides=20):
        """Бросок кубика 1-20"""

        return random.randint(1, sides)

    @staticmethod
    def human_choose_attack():
        """Выбор действия с валидацией"""

        valid_keys = ['A', 'D']
        
        while True:
            print("Атака слева - [ A ] или [ D ] - Атака справа")
            choice = input('Выберите действие: ').upper()
            
            if not choice:
                return None
            
            choice = choice[0]
            
            if choice in valid_keys:
                return choice
                   
            else:
                console.print(f"\n[bright_red]Используй только [ A ] или [ D ]![/bright_red]")

    @staticmethod
    def human_choose_defense():
        """Выбор защиты с валидацией"""
        
        valid_keys = ['A', 'D', 'Q']
        q_flag = False
        
        while True:
            raw_input = console.input('[cyan]Юнит[/cyan], защищайся!\n[ A ] - защита слева, [ D ] - защита справа '
                                      '[ Q ] - Бабл Паладина, если не использовал: \n').upper()

            if not raw_input:
                return None
            
            choice = raw_input[0]
            
            if choice == 'Q':
                if q_flag:
                    console.print("[bright_red]ЭЙ! Q уже использован в этом ходу! \nВыбери A или D для защиты![/bright_red]")
                    continue
                    
                console.print("[magenta]Бросок кубика на бабл Паладина![/magenta]")
        
                while True:
                    user_input = console.input("[magenta]Нажмите [ пробел ] для броска. Сложность <15>: [/magenta]")
                    
                    if user_input == " ":
                        break
                    else:
                        console.print("[bright_red]Нажмите именно [ пробел ]![/bright_red]")
                
                n = GameLogic.roll_dice()
                
                print(f"На кубике < {n} >")

                if n > 15:
                    console.print('[yellow]Бабл активирован! Урона нет![/yellow]')
                    return True
                else:
                    q_flag = True
                    console.print('[yellow]Бабл не активирован! Выбери защиту вручную.\n[/yellow]')
                    continue
                    
            elif choice in ['A', 'D']:
                return choice
            else:
                console.print(f"[bright_red]Используй только => {', '.join(valid_keys)}![/bright_red]")

    @staticmethod
    def computer_choose():
        return random.choice(['A', 'D'])
    
    @staticmethod
    def check_hit(attack_side, defense_side):
        return attack_side != defense_side


class GameController:
    def __init__(self):
        self.computer = Unit("Хекс")
        self.player = Unit()
        self.console = Console()
    
    def game_loop(self):
        """Фаза 1: Определение инициативы"""

        console.print("[magenta]Бросок кубика на инициативу![/magenta]")
        
        while True:
            user_input = input("Нажмите для броска кубика [ пробел ] + [ Enter ]\n")
            
            if user_input[0] == " ":
                break
            else:
                console.print("[bright_red]Чтобы бросить кубик нажмите на [ пробел ][/bright_red]")
        
        player_roll = GameLogic.roll_dice()
        computer_roll = GameLogic.roll_dice()
            
        console.print(f"[magenta]Ты выкинул < {player_roll} > vs Хекс < {computer_roll} >[/magenta]")
        
        if player_roll >= computer_roll:
            console.print("[cyan]Юнит атакует первым![/cyan]\n")
            self.player_attacks_first()
        else:
            console.print("[red]Хекс атакует первым![/red]\n")
            self.computer_attacks_first()
    
    def player_attacks_first(self):
        """Ветка событий: Юнит атакует первым"""

        round_number = 1
        while self.player.is_alive() and self.computer.is_alive():
            self.console.print(Panel(f"====== РАУНД {round_number} ======", style="bold green"))

            result = self.player_attack_phase()
            if result == 'Победил Юнит!':
                console.print(Panel("ЮНИТ ПОБЕДИЛ!", style="bold green"))
                return

            if self.computer.is_alive():
                result = self.computer_attack_phase()
                if result == 'Победил Хекс!':
                    console.print(Panel("GAME OVER ХЕКС ПОБЕДИЛ!", style="bold red"))
                    return

            round_number += 1
    
    def computer_attacks_first(self):
        """Ветка событий: Хекс атакует первым"""

        round_number = 1
        while self.player.is_alive() and self.computer.is_alive():
            self.console.print(Panel(f"====== РАУНД {round_number} ======", style="bold green"))

            result = self.computer_attack_phase()
            if result == 'Победил Хекс!':
                console.print(Panel("GAME OVER ХЕКС ПОБЕДИЛ!", style="bold red"))
                return

            if self.player.is_alive():
                result = self.player_attack_phase()
                if result == 'Победил Юнит!':
                    console.print(Panel("ЮНИТ ПОБЕДИЛ!", style="bold green"))
                    return

            round_number += 1

    def player_attack_phase(self):
        """Атака Юнита - Хекс защищается"""

        action1 = GameLogic.human_choose_attack()
        action2 = GameLogic.computer_choose()

        n = GameLogic.roll_dice()

        console.print("[magenta]Хекс бросает кубик на бабл паладина[/magenta]")
        console.print(f"[magenta]Проверка на активацию Сложность <15>, выпало: {n}[/magenta]")

        if n >= 15:
            console.print("[yellow]Хекс активирует бабл паладина и не получает урон![/yellow]\n")
            return True
        else:
            if GameLogic.check_hit(action1, action2):
                console.print('[yellow]Бабл не активирован! Хекс делает выбор на защиту...[/yellow]')
                console.print('[bright_red]Юнит наносит 3 очка урона, точно в цель![/bright_red]')
                self.computer.take_damage(3)
            else:
                console.print('[yellow]Хекс не использует бабл и делает выбор на защиту...[/yellow]')
                console.print('[orange3]И он защищает нужную сторону и получает всего 1 урон![/orange3]')
                self.computer.take_damage(1)
            
            console.print(self.computer.get_status())
        
        if not self.computer.is_alive():
            return 'Победил Юнит!'
        elif not self.player.is_alive():
            return 'Победил Хекс!'
        else:
            return True
    
    def computer_attack_phase(self):
        """Атака Хекса - Юнит защищается"""
        
        computer_attack = GameLogic.computer_choose()
        player_defense = GameLogic.human_choose_defense()
        
        # Если игрок использовал Q и вернул True - нет урона
        if player_defense is True:
            console.print("[green]Бабл сработал! Урона нет![/green]")
            return
        
        # Сравниваем атаку компьютера и защиту игрока
        if GameLogic.check_hit(computer_attack, player_defense):
            console.print('[bright_red]Хекс наносит 3 урона![/bright_red]')
            self.player.take_damage(3)
        else:
            console.print('[orange3]Юнит блокирует удар и получает 1 урона![/orange3]')
            self.player.take_damage(1)
        
        console.print(self.player.get_status())

        if not self.player.is_alive():
            return 'Победил Хекс!'
        elif not self.computer.is_alive():
            return 'Победил Юнит!'
        return True


if __name__ == "__main__":
    game = GameController()
    game.game_loop()
