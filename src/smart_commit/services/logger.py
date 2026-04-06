import sys
from colorama import Fore, Style, init


init(autoreset=True)


class Logger:
    @staticmethod
    def info(msg: str):
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")

    @staticmethod
    def success(msg: str):
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")

    @staticmethod
    def warning(msg: str):
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}")

    @staticmethod
    def error(msg: str):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}", file=sys.stderr)


logger = Logger()
