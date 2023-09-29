# Pyrex4 System Manager.
## Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak, and npm in one function.

## Current Version: 4.10

## Dependencies:
- Python3 <=
- nix (optional)
- flatpak (optional)
- yay/pacman (optional)
- npm (optional)

## Installation: 
- `mv pyrex /usr/local/bin/`

## Options:
```
  -h, --help                     show this help message and exit
  -p, --prep                    Install units
  -t, --trash                    Remove units
  -o, --overhaul            Update system
  -f, --find                       Find units
  -fs, --from-scratch  Build and install unit from source (Nix only for now)
  -cc, --contain            Install unit in non-persistent shell environment. (Nix only for now)
  --garbage-disposal
                                        Collect unused units/paths (Nix only for now)
  --compact                 Consolidate shared dependencies to save storage and optimize file paths at the expense of less
                                        reproducibility. (Set to true per install by default)
  -v, --version              Show version number
```
