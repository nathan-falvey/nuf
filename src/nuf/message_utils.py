from colorama import just_fix_windows_console
import colorama
from colorama import Fore, Style


# Initialize colorama (safe to call multiple times, handles Windows ANSI translation)
colorama.init(autoreset=True)


# Pyrefly: ignore [missing-imports]
def make_info(message: str, prefix_label: str = "INFO") -> str:
    return f"[{Fore.BLUE}{prefix_label.upper()}{Style.RESET_ALL}] {message}"
    
# Pyrefly: ignore [missing-imports]
def make_warning(message: str, prefix_label: str = "WARNING") -> str:
    return f"[{Fore.YELLOW}{prefix_label.upper()}{Style.RESET_ALL}] {message}"

# Pyrefly: ignore [missing-imports]
def make_error(message: str, prefix_label: str = "ERROR") -> str:
    return f"[{Fore.RED}{prefix_label.upper()}{Style.RESET_ALL}] {message}"

# Pyrefly: ignore [missing-imports]
def make_success(message: str, prefix_label: str = "SUCCESS") -> str:
    return f"[{Fore.GREEN}{prefix_label.upper()}{Style.RESET_ALL}] {message}"

# Pyrefly: ignore [missing-imports]
def make_critical(message: str, prefix_label: str = "CRITICAL") -> str:
    return f"[{Fore.RED}{prefix_label.upper()}{Style.BRIGHT}{Style.RESET_ALL}] {message}"

# Pyrefly: ignore [missing-imports]
def make_debug(message: str, prefix_label: str = "DEBUG") -> str:
    return f"[{Style.DIM}{prefix_label.upper()}{Style.RESET_ALL}] {message}"
    