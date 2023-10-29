# Pyrex5 System Manager.
## Built with the intention of simplifying package distribution across all Linux distributions. 

# Goals:
- [x] integration with Distrobox (in progress)
- [ ] Search all 'repositories' give user prompt to choose where from
- [ ] **Proper config and installation method**
  - *There is honestly nothing really stopping me from writing a quick install.py script or something (or even figuring out how to enter into distro repos) but ive been finding working on this or other stuff more fun then making it usable for the public. Sorry as this is a mostly personal project currently, I will get to that eventually though!*
## Current Version: 5.3-4

## Dependencies:
- Python3 <=
- distrobox
- docker
- nix 
- flatpak
- yay & pacman
- neofetch

## Installation: 
### "Install" script and configs
- Move python script to bin directory to be executed:
  - `mv nvv.py /usr/bin/nvv`
- Create configs dir
  - `mkdir -p /etc/pyrex/nvv/`
- Move version.conf file to etc dir:
  - `mv help.conf /etc/pyrex/nvv/`
### Postrequisites:
- Install depends: 
  - Arch: `yay -S docker distrobox neofetch`
  
  **While the aim is to be distro agnostic, it is currently very focused on an arch based system with Nix package manager installed alongside. It is wholly untested on Debian, Fedora, or NixOS and can't currently operate with their package managers outside of passing commands through distrobox or using commands intended for nix-darwin. Although fixing this is exactly what I plan to work on next**
  - Debian: `apt install docker distrobox neofetch`
  - Nix: `nix-env -i docker distrobox neofetch`
- Enable docker daemon:
  - `systemctl enable dockerd`
- Generate the distrobox template containers:
  - Shell containers won't function without this (although the rest of the script should remain functional afaik, the interpreter may get confused at parts though, im unsure.)
  - `nvv --generate-templates`

#### Potential issues:
- If a permission denied error is given after moving /usr/bin/ then execution permissions need to be granted to the file. Executing the command below will grant said permissions.
  - `chmod +x /usr/bin/nvv`

## Options:
```
Repositories:
    [aur] - [Installs directly to system using pacman]
    [nix] - [Installs to user profile managed by Nix]
    [flatpak] - [Installs using flatpak]
    [apt] - [Creates a Debian container and installs package]
    [dnf] - [Creates a Fedora container and installs package]

options:
    -i    Install packages
    -t    Remove packages
    -o    Update system
    -f    Find packages
    -sh   Install package in non-persistent shell environment.
    -r    Run a package installed in a shell environment
    -gd   Collect unused packages/paths (Nix function)
    -cc   Consolidate shared dependencies to save storage and optimize file paths (Nix function)
    -v    Show version number

Long-form commands:
    --install
    --trash
    --overhaul
    --find
    --shell
    --run
    --garbage-disposal
    --compact
    --generate-templates
    --refresh-templates
    --version

```
