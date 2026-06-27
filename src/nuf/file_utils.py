from nuf.message_utils import print_success
import logging
import shutil
import os
from pathlib import Path
from typing import Union, List

# Set up logging
logger = logging.getLogger("nuf.file_utils")

# Custom Exception Hierarchy
class FileUtilsError(Exception):
    """Base exception for file_utils operations."""
    pass

class PathNotFoundError(FileUtilsError):
    """Raised when a file or directory is not found."""
    pass

class PermissionDeniedError(FileUtilsError):
    """Raised when permission is denied for a file or directory operation."""
    pass

class DirectoryNotEmptyError(FileUtilsError):
    """Raised when trying to delete a non-empty directory using a strict rmdir."""
    pass

class OperationFailedError(FileUtilsError):
    """Raised when an OS or file system operation fails."""
    pass

# Dummy function for linting
def file_func() -> str:
    return "Hello from file_utils"


def check_file_exists(path: Union[str, Path]) -> bool:
    """Checks if a file exists at the given path."""
    try:
        return Path(path).is_file()
    except Exception as e:
        logger.debug("Failed to check file existence for %s: %s", path, e)
        return False


def check_dir_exists(path: Union[str, Path]) -> bool:
    """Checks if a directory exists at the given path."""
    try:
        return Path(path).is_dir()
    except Exception as e:
        logger.debug("Failed to check directory existence for %s: %s", path, e)
        return False


def get_file_size(path: Union[str, Path]) -> int:
    """Returns the size of the file in bytes.
    
    Raises:
        PathNotFoundError: If the file does not exist.
        PermissionDeniedError: If access is denied.
        OperationFailedError: For other OS/filesystem errors.
    """
    p = Path(path)
    try:
        if not p.is_file():
            raise PathNotFoundError(f"File not found: {p}")
        return p.stat().st_size
    except PathNotFoundError:
        raise
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied accessing size of: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to get file size for: {p}. Original error: {e}")


def create_dir(path: Union[str, Path], parents: bool = True, exist_ok: bool = True) -> bool:
    """Creates a directory at the given path.
    
    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If creation fails due to other OS/file system errors.
    """
    p = Path(path)
    try:
        p.mkdir(parents=parents, exist_ok=exist_ok)
        return True
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied creating directory: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to create directory: {p}. Original error: {e}")


def delete_dir(path: Union[str, Path], recursive: bool = False) -> bool:
    """Deletes a directory. If recursive is True, deletes all its contents.
    
    Raises:
        PathNotFoundError: If the directory does not exist.
        PermissionDeniedError: If permission is denied.
        DirectoryNotEmptyError: If directory is not empty and recursive is False.
        OperationFailedError: If deletion fails.
    """
    p = Path(path)
    try:
        if not p.is_dir():
            raise PathNotFoundError(f"Directory not found: {p}")
        
        if recursive:
            shutil.rmtree(p)
        else:
            p.rmdir()
        return True
    except PathNotFoundError:
        raise
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied deleting directory: {p}. Original error: {e}")
    except OSError as e:
        import errno
        # Error code for Directory Not Empty is ENOTEMPTY or EEXIST
        if e.errno in (errno.ENOTEMPTY, errno.EEXIST):
            raise DirectoryNotEmptyError(f"Directory not empty: {p}. Set recursive=True to delete contents.")
        raise OperationFailedError(f"Failed to delete directory: {p}. Original error: {e}")


def create_file(path: Union[str, Path], exist_ok: bool = True) -> bool:
    """Creates an empty file at the given path.
    
    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If creation fails.
    """
    p = Path(path)
    try:
        if p.is_file() and not exist_ok:
            raise OperationFailedError(f"File already exists: {p}")
        p.touch(exist_ok=exist_ok)
        return True
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied creating file: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to create file: {p}. Original error: {e}")


def append_line_to_file(path: Union[str, Path], line: str, encoding: str = 'utf-8') -> bool:
    """Writes a line to a file (creates parent directories if needed).
    
    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If write operation fails.
    """
    p = Path(path)
    try:
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            
        with open(p, 'a', encoding=encoding) as file:
            file.write(line + '\n')
        return True
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied writing to file: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to write line to file: {p}. Original error: {e}")


def return_lines_from_file(path: Union[str, Path], encoding: str = 'utf-8') -> List[str]:
    """Returns a list of lines from a file.
    
    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.
    """
    p = Path(path)
    try:
        if not p.is_file():
            raise PathNotFoundError(f"File not found: {p}")
        with open(p, 'r', encoding=encoding) as file:
            return file.readlines()
    except PathNotFoundError:
        raise
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied reading file: {p}. Original error: {e}")
    except (OSError, UnicodeDecodeError) as e:
        raise OperationFailedError(f"Failed to read lines from file: {p}. Original error: {e}")


def stream_files(path: Union[str, Path], recursive: Union[True, False]) -> object:
    """ Streams a list of filenames from a file, paths are chosen by extension

    Args:
        path (Union[str, Path]): The path to the directory to stream files from.
        recursive (bool): Whether to stream files recursively.

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    Yields:
        Iterator[Path]: An iterator of paths to files.
    """
    
    p = Path(path)
    if not p.is_dir():
        raise PathNotFoundError(f"Directory not found: {p}")

    if recursive:
        files = p.glob("**/*")
    else:
        files = p.glob("*")

    for file in files:
        if file.is_file():
            yield file

def stream_files_by_extension(path: Union[str, Path], extensions: list, recursive: Union[True, False]) -> object:
    """ Streams a list of filenames from a file, paths are chosen by extension

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    
    p = Path(path)
    if not p.is_dir():
        raise PathNotFoundError(f"Directory not found: {p}")

    if recursive:
        files = p.glob("**/*")
    else:
        files = p.glob("*")

    for file in files:
        if file.is_file() and file.suffix in extensions:
            yield file


def list_files_by_extension(path: Union[str, Path], extensions: list, recursive: Union[True, False]) -> List[Path]:
    """ Returns a list of filenames from a file, paths are chosen by extension

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    
    p = Path(path)
    if not p.is_dir():
        raise PathNotFoundError(f"Directory not found: {p}")

    if recursive:
        files = p.glob("**/*")
    else:
        files = p.glob("*")

    return [file for file in files if file.is_file() and file.suffix in extensions]


def get_files_by_extension(path: Union[str, Path], extensions: list, recursive: Union[True, False]) -> List[Path]:
    """ Returns a list of filenames from a file, paths are chosen by extension

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    
    p = Path(path)
    if not p.is_dir():
        raise PathNotFoundError(f"Directory not found: {p}")

    if recursive:
        files = p.glob("**/*")
    else:
        files = p.glob("*")

    return [file for file in files if file.is_file() and file.suffix in extensions]

def sort_files_by_time(files: list, reverse: bool = False) -> List[Path]:
    """ Sorts a list of files by time 

    Args:
        files (list): List of files to sort
        reverse (bool, optional): Reverse the sort order. Defaults to False.

    Returns:
        List[Path]: Sorted list of files

    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=reverse)


def sort_files_by_size(files: list, reverse: bool = False) -> List[Path]:
    """ Sorts a list of files by size 

    Args:
        files (list): List of files to sort
        reverse (bool, optional): Reverse the sort order. Defaults to False.

    Returns:
        List[Path]: Sorted list of files

    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    return sorted(files, key=lambda x: x.stat().st_size, reverse=reverse)

def sort_files_by_name(files: list, reverse: bool = False) -> List[Path]:
    """ Sorts a list of files by name 

    Args:
        files (list): List of files to sort
        reverse (bool, optional): Reverse the sort order. Defaults to False.

    Returns:
        List[Path]: Sorted list of files

    Raises:
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    return sorted(files, key=lambda x: x.name, reverse=reverse)


def calculate_checksum_of_file(file_path: Union[str, Path], chunk_size: int = 8192) -> str:
    """ Calculates the checksum of a file 

    Args:
        file_path (Union[str, Path]): The path to the file to calculate the checksum of.
        chunk_size (int, optional): The chunk size to read the file in. Defaults to 8192.

    Returns:
        str: The checksum of the file.

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If read operation fails.

    """
    import hashlib
    p = Path(file_path)
    if not p.is_file():
        raise PathNotFoundError(f"File not found: {p}")
    checksum = hashlib.md5()
    with open(p, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            checksum.update(chunk)
    return checksum.hexdigest()

# File deletion functions

def delete_file(file_path: Union[str, Path]) -> None:
    """ Deletes a file 

    Args:
        file_path (Union[str, Path]): The path to the file to delete.

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If delete operation fails.

    """
    p = Path(file_path)
    if not p.is_file():
        raise PathNotFoundError(f"File not found: {p}")
    try:
        p.unlink()
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied deleting file: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to delete file: {p}. Original error: {e}")

def obfuscate_file_and_delete(file_path: Union[str, Path], debug: bool = False) -> None:
    """ Obfuscates a file by overwriting it with random data and then deleting it 

    Args:
        file_path (Union[str, Path]): The path to the file to obfuscate and delete.

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If obfuscate or delete operation fails.

    """
    p = Path(file_path)
    if not p.is_file():
        raise PathNotFoundError(f"File not found: {p}")

    size = p.stat().st_size

    try:
        with open(p, 'wb') as file:
            file.write(os.urandom(size))
            if debug:
                print_success(f"Obfuscated file: {p}")
        p.unlink(missing_ok=False)
        if debug:
            print_success(f"Deleted file: {p}")
    except PermissionError as e:
        raise PermissionDeniedError(f"Permission denied obfuscating or deleting file: {p}. Original error: {e}")
    except OSError as e:
        raise OperationFailedError(f"Failed to obfuscate or delete file: {p}. Original error: {e}")

def send_file_to_trash(file_path: Union[str, Path], debug: bool = False) -> None:
    """ Sends a file to the trash 

    Args:
        file_path (Union[str, Path]): The path to the file to send to the trash.

    Raises:
        PathNotFoundError: If file does not exist.
        PermissionDeniedError: If permission is denied.
        OperationFailedError: If send to trash operation fails.

    """
    import send2trash
    p = Path(file_path)
    if not p.is_file():
        raise PathNotFoundError(f"File not found: {p}")
    try:
        send2trash.send2trash(p)
        if debug:
            print_success(f"Sent file to trash: {p}")
    except Exception as e:
        raise OperationFailedError(f"Failed to send file to trash: {p}. Original error: {e}")
    