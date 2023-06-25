# Pyrex2 package manager
Pyrex2 package manager/wrapper. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman(yay), flatpak, and npm in one function. 
```
options:
  -s, --station         Install packages (nix., aur., flatpak., npm.,)
  -t, --trash           Remove packages (nix., aur., flatpak., npm.,)
  -o, --overhaul        Update system
  -f, --find            find packages (nix., aur., flatpak., npm.,)
  -bs, --build-source   Build and install package from source (Nix only for now)
  -rd, --remove-debris  Collect unused packages/paths (nix only for now)
  -c, --compactor       Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to true by default)
  --shell               Install package in non-persistent shell environment. (nix only for now)
```
