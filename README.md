# Pyrex2 package manager
Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak,
and npm in one function.
```
options:
  -h, --help            show this help message and exit
  -s, --station         Install units
  -t, --trash           Remove units
  -o, --overhaul        Update system
  -f, --find            find units
  -bs, --build-source   Build and install unit from source (Nix only for now)
  -rd, --remove-debris  Collect unused units/paths (nix only for now)
  -c, --compactor       Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to true
                        by default)
  --shell               Install unit in non-persistent shell environment. (nix only for now)

Use nix.[unit], aur.[unit], flatpak.[unit], or npm.[unit] to specify source. example: pyrex --order aur.firefox

```
