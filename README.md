# Pyrex4 System Manager.
## Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, and flatpak in one function.

# Goals:
- [x] integration with Distrobox (in progress)
- [ ] Search all 'repositories' give user prompt to choose where from
- [ ] Proper config and installation method
## Current Version: 4.12.02

## Dependencies:
- Python3 <=
- distrobox
- docker
- nix (optional)
- flatpak (optional)
- yay/pacman (optional)

## Installation: 
- `mv nv /usr/local/bin/`

## Options:
```
options:
  -h, --help            show this help message and exit
  -i, --install         Install packages
  -t, --trash           Remove packages
  -o, --overhaul        Update system
  -f, --find            Find packages
  -sh, --shell          Install unit in non-persistent shell environment. (Does not support Flatpak)
  -r, --run
  -gd, --garbage-disposal
                        Collect unused packages/paths (Nix function)
  -cc, --compact        Consolidate shared dependencies to save storage and optimize file paths at the expense of
                        less reproducibility. (Set to False per install by default)
  -v, --version         Show version number

```
