#!/usr/bin/env python3
import sys
from pathlib import Path


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from termux_app_store.doctor import run

    run()


if __name__ == "__main__":
    main()
