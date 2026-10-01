"""PyInstaller entry point (the package uses relative imports, so it can't be the entry itself)."""
import multiprocessing

from mucify.main import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
