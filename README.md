# Pyrex5 System Manager.
## Built with the intention of simplifying package distribution across all Linux distributions. 

# Goals:
- [x] integration with Distrobox (in progress)
- [ ] Search all 'repositories' give user prompt to choose where from
- [ ] **Proper config and installation method**
  - *There is honestly nothing really stopping me from writing a quick install.py script or something (or even figuring out how to enter into distro repos) but ive been finding working on this or other stuff more fun then making it usable for the public. Sorry as this is a mostly personal project currently, I will get to that eventually though!*
## Current Version: 5.3

## Dependencies:
- Python3 <=
- distrobox
- docker
- nix 
- flatpak
- yay & pacman
- neofetch

## Installation: 
### Prerequisites:
- Install depends: 
  - Arch: `yay -S docker distrobox neofetch`
  - Debian: `apt install docker distrobox neofetch`
  - Nix: `nix-env -i docker distrobox neofetch`
- Enable docker daemon:
  - `systemctl enable dockerd`
- Create shell environments:
  - `distrobox create -r --image archlinux -n arch-template`
  - `distrobox create -r --image debian -n debian-template`
  - `distrobox create -r --image fedora -n fedora-template`
### "Install"
- Move python script to bin directory to be executed:
  - `mv nvv.py /usr/bin/nvv`
- Create configs dir
  - `mkdir -p /etc/pyrex/nvv/`
- Move version.conf file to etc dir:
  - `mv pyrexVersion.conf /etc/pyrex/nvv/`

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
