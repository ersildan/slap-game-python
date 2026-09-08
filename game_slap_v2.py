import random


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

            if choice == 'exit'.upper():
                print('Выход из игры')
                exit()

            if not choice:
                return None
            
            choice = choice[0]
            
            if choice in valid_keys:
                return choice
                   
            else:
                print(f"\nИспользуй только [ A ] или [ D ]!")

    @staticmethod
    def human_choose_defense():
        """Выбор защиты с валидацией"""
        
        valid_keys = ['A', 'D', 'Q']
        q_flag = False
        
        while True:
            raw_input = input('Юнит, защищайся!\n[ A ] - защита слева, [ D ] - защита справа '
                                      '[ Q ] - Бабл Паладина, если не использовал: \n').upper()

            if raw_input == 'exit'.upper():
                print('Выход из игры')
                exit()

            if not raw_input:
                return None
            
            choice = raw_input[0]
            
            if choice == 'Q':
                if q_flag:
                    print("ЭЙ! Q уже использован в этом ходу! \nВыбери A или D для защиты!")
                    continue
                    
                print("[magenta]Бросок кубика на бабл Паладина![/magenta]")
        
                while True:
                    user_input = input("Нажмите [ пробел ] для броска. Сложность <15>:")

                    if user_input == 'exit'.upper():
                        print('Выход из игры')
                        exit()

                    if user_input == " ":
                        break
                    else:
                        print("[bright_red]Нажмите именно [ пробел ]![/bright_red]")
                
                n = GameLogic.roll_dice()
                
                print(f"На кубике < {n} >")

                if n > 15:
                    print('[yellow]Бабл активирован! Урона нет![/yellow]')
                    return True
                else:
                    q_flag = True
                    print('[yellow]Бабл не активирован! Выбери защиту вручную.\n[/yellow]')
                    continue
                    
            elif choice in ['A', 'D']:
                return choice
            else:
                print(f"[bright_red]Используй только => {', '.join(valid_keys)}![/bright_red]")

    @staticmethod
    def computer_choose():
        return random.choice(['A', 'D'])
    
    @staticmethod
    def check_hit(attack_side, defense_side):
        return attack_side != defense_side


class GameController:
    def __init__(self):
        self.computer = Unit("Компьютер")
        self.player = Unit()
        
    
    def game_loop(self):
        """Фаза 1: Определение инициативы"""

        print("[magenta]Бросок кубика на инициативу![/magenta]")
        
        while True:
            user_input = input("Нажмите для броска кубика [ пробел ] после нажмите [ Enter ]\n")

            if user_input == 'exit'.upper():
                print('Выход из игры')
                exit()

            if user_input[0] == " ":
                break
            else:
                print("[bright_red]Чтобы бросить кубик нажмите на [ пробел ][/bright_red]")
        
        player_roll = GameLogic.roll_dice()
        computer_roll = GameLogic.roll_dice()
            
        print(f"[magenta]Ты выкинул < {player_roll} > vs Компьютер < {computer_roll} >[/magenta]")
        
        if player_roll >= computer_roll:
            print("[cyan]Юнит атакует первым![/cyan]\n")
            self.player_attacks_first()
        else:
            print("[red]Компьютер атакует первым![/red]\n")
            self.computer_attacks_first()
    
    def player_attacks_first(self):
        """Ветка событий: Юнит атакует первым"""

        round_number = 1
        while self.player.is_alive() and self.computer.is_alive():
            print(f"====== РАУНД {round_number} ======")

            result = self.player_attack_phase()
            if result == 'Победил Юнит!':
                print(("ЮНИТ ПОБЕДИЛ!"))
                return

            if self.computer.is_alive():
                result = self.computer_attack_phase()
                if result == 'Победил Компьютер!':
                    print(("GAME OVER КОМПЬЮТЕР ПОБЕДИЛ!"))
                    return

            round_number += 1
    
    def computer_attacks_first(self):
        """Ветка событий: Компьютер атакует первым"""

        round_number = 1
        while self.player.is_alive() and self.computer.is_alive():
            print((f"====== РАУНД {round_number} ======" ))

            result = self.computer_attack_phase()
            if result == 'ПобеКомпьютер!':
                print(("GAME OVER КОМПЬЮТЕР ПОБЕДИЛ!"))
                return

            if self.player.is_alive():
                result = self.player_attack_phase()
                if result == 'Победил Юнит!':
                    print(("ЮНИТ ПОБЕДИЛ!"))
                    return

            round_number += 1

    def player_attack_phase(self):
        """Атака Юнита - Компьютер защищается"""

        action1 = GameLogic.human_choose_attack()
        action2 = GameLogic.computer_choose()

        n = GameLogic.roll_dice()

        print("[magenta]Компьютер бросает кубик на бабл паладина[/magenta]")
        print(f"[magenta]Проверка на активацию Сложность <15>, выпало: {n}[/magenta]")

        if n >= 15:
            print("[yellow]Компьютер активирует бабл паладина и не получает урон![/yellow]\n")
            return True
        else:
            if GameLogic.check_hit(action1, action2):
                print('[yellow]Бабл не активирован! Компьютер делает выбор на защиту...[/yellow]')
                print('[bright_red]Юнит наносит 3 очка урона, точно в цель![/bright_red]')
                self.computer.take_damage(3)
            else:
                print('[yellow]Компьютер не использует бабл и делает выбор на защиту...[/yellow]')
                print('[orange3]И он защищает нужную сторону и получает всего 1 урон![/orange3]')
                self.computer.take_damage(1)
            
            print(self.computer.get_status())
        
        if not self.computer.is_alive():
            return 'Победил Юнит!'
        elif not self.player.is_alive():
            return 'Победил Компьютер!'
        else:
            return True
    
    def computer_attack_phase(self):
        """Атака Компьютера - Юнит защищается"""
        
        computer_attack = GameLogic.computer_choose()
        player_defense = GameLogic.human_choose_defense()
        
        # Если игрок использовал Q и вернул True - нет урона
        if player_defense is True:
            print("[green]Бабл сработал! Урона нет![/green]")
            return
        
        # Сравниваем атаку компьютера и защиту игрока
        if GameLogic.check_hit(computer_attack, player_defense):
            print('[bright_red]Компьютер наносит 3 урона![/bright_red]')
            self.player.take_damage(3)
        else:
            print('[orange3]Юнит блокирует удар и получает 1 урона![/orange3]')
            self.player.take_damage(1)
        
        print(self.player.get_status())

        if not self.player.is_alive():
            return 'Победил Компьютер!'
        elif not self.computer.is_alive():
            return 'Победил Юнит!'
        return True


if __name__ == "__main__":
    game = GameController()
    game.game_loop()
