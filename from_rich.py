from rich.console import Console
from rich. import 

console = Console(force_terminal=True)

print(("ФАЗА АТАКИ ЮНИТА", style="bold green"))
print("[cyan]Юнит[/cyan] атакует!")
print("[magenta]Хекс теряет 3 HP![/magenta]")
print("[bold red]Юнит наносит 3 очка урона, точно в цель![/bold red]")
print("[orange3]И он защищает нужную сторону и получает всего 1 урон![/orange3]")
print("[bold green]Бабл активирован! Урона нет![/bold green]")

from colorama import Fore, Back, Style, init
init(autoreset=True)

print(Fore.GREEN + "ФАЗА АТАКИ ЮНИТА")
print(Fore.CYAN + "Юнит" + Style.RESET_ALL + " атакует!")
print(Fore.MAGENTA + "Хекс теряет 3 HP!")
print(Fore.RED + "Юнит наносит 3 очка урона, точно в цель!")
print(Fore.YELLOW + "И он защищает нужную сторону и получает всего 1 урон!")
print(Fore.GREEN + "Бабл активирован! Урона нет!")