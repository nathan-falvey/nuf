import importlib
import pkgutil


__name__ = "nuf"
__version__ = "dev_testing"

# Dynamically import all python files (modules) in the current package directory
for _, module_name, _ in pkgutil.iter_modules(__path__):
    # Import the module dynamically
    module = importlib.import_module(f"{__name__}.{module_name}")
    # Expose the module in the package namespace
    globals()[module_name] = module



if __name__ == "__main__":
    import sys
    print("You are running the nuf package directly, which is not recommended. Please import this package in your own scripts instead.")
    sys.exit(1)