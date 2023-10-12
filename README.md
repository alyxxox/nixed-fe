# Pyrex4 System Manager.
## Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, and flatpak in one function.

## Current Version: 4.10

## Dependencies:
- Python3 <=
- nix (optional)
- flatpak (optional)
- yay/pacman (optional)

## Installation: 
- `mv pyrex /usr/local/bin/`

## Options:
```
options:
  -h, --help            show this help message and exit
  -i, --install         Install packages
  -t, --trash           Remove packages
  -o, --overhaul        Update system
  -f, --find            Find packages1
  -gd, --garbage-disposal
                        Collect unused packages/paths (Nix only for now)
  -cc, --compact        Consolidate shared dependencies to save storage and optimize file paths at
                        the expense of less reproducibility. (Set to true per install by default)
  -v, --version         Show version number
  --debug-parser

```
