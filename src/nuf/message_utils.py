import colorama
from colorama import Fore, Style

# Initialize colorama (safe to call multiple times, handles Windows ANSI translation)
colorama.init(autoreset=True)


COLOUR_TABLE = {
    "default": Style.RESET_ALL,
    "info": Fore.BLUE,
    "success": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "critical": Fore.RED + Style.BRIGHT,
    "debug": Style.DIM,
}

def message_func() -> str:
    return "Hello from message_utils"


def bracketed_message_string(label: str, style: str = "default") -> str:
    return f"[{COLOUR_TABLE[style]}{label}{COLOUR_TABLE['default']}]"
    
def print_warning(message: str, prefix_label: str = "WARNING") -> None:
    print(f"{bracketed_message_string(prefix_label, 'warning')} {message}")

def print_error(message: str, prefix_label: str = "ERROR") -> None:
    print(f"{bracketed_message_string(prefix_label, 'error')} {message}")

def print_success(message: str, prefix_label: str = "SUCCESS") -> None:
    print(f"{bracketed_message_string(prefix_label, 'success')} {message}")

def print_info(message: str, prefix_label: str = "INFO") -> None:
    print(f"{bracketed_message_string(prefix_label, 'info')} {message}")

def print_debug(message: str, prefix_label: str = "DEBUG") -> None:
    print(f"{bracketed_message_string(prefix_label, 'debug')} {message}")

def print_critical(message: str, prefix_label: str = "CRITICAL") -> None:
    print(f"{bracketed_message_string(prefix_label, 'critical')} {message}")

