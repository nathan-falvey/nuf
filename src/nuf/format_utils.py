from typing import Union
from pathlib import Path



def format_func() -> str:
    return "Hello from format_utils"

def format_bytes(size_bytes: int, decimal_places: int = 2) -> str:
    """Converts a number of bytes to a human-readable string representation (e.g. KB, MB, GB)."""
    if size_bytes < 0:
        raise ValueError("Size in bytes cannot be negative")
    
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size_bytes)
    unit_idx = 0
    while size >= 1024.0 and unit_idx < len(units) - 1:
        size /= 1024.0
        unit_idx += 1
        
    return f"{size:.{decimal_places}f} {units[unit_idx]}"


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamps a value to a specified range."""
    return max(min_value, min(value, max_value))
    
def random_string(length: int = 10, include_special_characters: bool = False) -> str:
    """Generates a random string of the specified length."""
    import string
    import random

    if include_special_characters:
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    else:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



# Time Format Functions
def format_time_diff(seconds: float) -> str:
    """Converts a time difference in seconds to a human-readable string (e.g. 1h30m 12s)."""
    if seconds < 0:
        raise ValueError("Time difference cannot be negative")

    parts = []
    
    # Calculate hours
    hours, remainder = divmod(seconds, 3600)
    if hours > 0:
        parts.append(f"{int(hours)}h")
    
    # Calculate minutes
    minutes, seconds = divmod(remainder, 60)
    if minutes > 0:
        parts.append(f"{int(minutes)}m")
    
    # Calculate seconds (with milliseconds if needed)
    if seconds > 0 or not parts:
        if seconds >= 1:
            parts.append(f"{int(seconds)}s")
        else:
            parts.append(f"{seconds:.3f}s")
    
    return " ".join(parts)

def format_timestamp(timestamp: float, output_format: str = "%d-%m-%Y %H:%M:%S") -> str:
    """Formats a timestamp (seconds since epoch) into a human-readable date/time string."""
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime(output_format)



# File Age Functions
def get_file_age_in_seconds(file_path: Union[str, Path]) -> float:
    """Returns the age of the file in seconds."""
    p = Path(file_path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return p.stat().st_mtime

def get_file_age_in_minutes(file_path: Union[str, Path]) -> float:
    """Returns the age of the file in minutes."""
    return get_file_age_in_seconds(file_path) / 60

def get_file_age_in_hours(file_path: Union[str, Path]) -> float:
    """Returns the age of the file in hours."""
    return get_file_age_in_seconds(file_path) / 3600

def get_file_age_in_days(file_path: Union[str, Path]) -> float:
    """Returns the age of the file in days."""
    return get_file_age_in_seconds(file_path) / 86400