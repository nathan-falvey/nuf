import importlib
import pkgutil


__name__ = "nuf"
__version__ = "0.1.0"

# Dynamically import all python files (modules) in the current package directory
for _, module_name, _ in pkgutil.iter_modules(__path__):
    # Import the module dynamically
    module = importlib.import_module(f"{__name__}.{module_name}")
    # Expose the module in the package namespace
    globals()[module_name] = module

