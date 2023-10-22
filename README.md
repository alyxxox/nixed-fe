# Pyrex5 System Manager.
## Built with the intention of simplifying package distribution across all Linux distributions. 

# Goals:
- [x] integration with Distrobox (in progress)
- [ ] Search all 'repositories' give user prompt to choose where from
- [ ] Proper config and installation method
## Current Version: 5.2.1

## Dependencies:
- Python3 <=
- distrobox
- docker
- nix 
- flatpak
- yay & pacman

## Installation: 
### Install prerequisites:
- Install docker and distrobox
  - Arch: `yay -S docker distrobox`
  - Debian: `apt install docker distrobox`
  - Nix: `nix-env -i docker distrobox`
- Enable docker daemon:
  - `systemctl enable dockerd`
- Create shell environments:
  - `distrobox create -r --image archlinux -n arch-template`
  - `distrobox create -r --image debian -n debian-template`
  - `distrobox create -r --image fedora -n fedora-template`
- Move python script to bin directory to be executed:
  - `mv nvv.py /usr/local/bin/nvv`

#### Potential issues:
- If a permission denied error is given after moving /usr/bin/ then execution permissions need to be granted to the file. Executing the command below will grant said permissions.
  - `chmod +x /usr/bin/nvv`

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
