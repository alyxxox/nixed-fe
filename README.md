# Pyrex2 package manager
Nixed Frontend is a frontend/syntax wrapper for nix package manager (intended for Darwin builds.) Developed and tested on Arch Linux with Xfce4
```
usage: pyrex [-h] [-s] [-t] [-o] [-f] [-bs] [-rd] [-c] [--shell] [stdinn]

Pyrex2 package manager/wrapper. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak,
and npm in one function.

options:
  -h, --help            show this help message and exit
  -s, --station         Install packages (nix., aur., flatpak., npm.,)
  -t, --trash           Remove packages (nix., aur., flatpak., npm.,)
  -o, --overhaul        Update system
  -f, --find            find packages (nix., aur., flatpak., npm.,)
  -bs, --build-source   Build and install package from source (Nix only for now)
  -rd, --remove-debris  Collect unused packages/paths (nix only for now)
  -c, --compactor       Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to true
                        by default)
  --shell               Install package in non-persistent shell environment. (nix only for now)

Use nix.[package], aur.[package], flatpak.[package], or npm.[package] to specify source. example: pyrex --order aur.firefox
```
