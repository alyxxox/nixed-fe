#!/usr/bin/env python3

import subprocess
import argparse
import threading
import time
import os

home_dir = os.path.expanduser('~')
config_dir = '/etc/pyrex/nvv/'
version_config = config_dir+'pyrexVersion.config'

parser = argparse.ArgumentParser(description='Pyrex4 System Manager. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak in one function.', add_help=False)
parser.add_argument('-h', '--help', action='store_true')
parser.add_argument('-i', '--install', dest='install', action='store_true', help='Install packages')
parser.add_argument('-t', '--trash', dest='remove', action='store_true', help='Remove packages')
parser.add_argument('-o', '--overhaul', dest='update', action='store_true', help='Update system')
parser.add_argument('-f', '--find', dest='find', action='store_true', help='Find packages')
#parser.add_argument('--verbose', dest='verbose', action='store_true', help='Require user confirmation before any command is processed. (Currently only implemented with AUR)')
#parser.add_argument('-fs', '--from-scratch', dest='source', action='store_true', help='Build and install package from source (Nix only for now)')
parser.add_argument('-sh', '--shell', dest='shell', action='store_true', help='Install package in non-persistent shell environment. (Does not support Flatpak)')
parser.add_argument('-r', '--run', dest='run', action='store_true', help='Run a package installed in a shell environment (or run any shell to make customisations to the template)')
parser.add_argument('-gd', '--garbage-disposal', dest='collectGarbage', action='store_true', help='Collect unused packages/paths (Nix function)')
parser.add_argument('-cc', '--compact', dest='compactor', action='store_true', help='Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to False per install by default)')
parser.add_argument('--generate-templates', dest='generate_templates', action='store_true', help='Generate shell templates automatically.')
parser.add_argument('--refresh-templates', dest='refresh_templates', action='store_true', help='Remove shell templates and replace with using fresh images in case they get too full or configs are messed up')
parser.add_argument('-v', '--version', dest='version', action='store_true', help='Show version number')
parser.add_argument('-dbd', '--debug', dest='debug', action='store_true', help="Prints the raw output of the input parser. For debugging purposes and shouldn't be included in final release")
parser.add_argument(dest='package', action='append', nargs='?', help='must be the last argument presented')
args = parser.parse_args()
cmm = subprocess.call
class CliParser:
    def __init__(self, package):
        self.package = package
    def clean_input(self):
        cleaned_input = str(self.package).strip('[]\'')
        return cleaned_input
cli_parser = CliParser(args.package)
specin = cli_parser.clean_input()
if specin != 'None':
    repo = specin.split(':')[0]
    package = specin.split(':')[1]
    updateRepo = repo
else:
    repo = 'None'
    package = 'None'
if repo == 'aur':
    container = 'arch-template'
elif repo == 'apt':
    container = 'debian-template'
elif repo == 'dnf':
    container = 'fedora-template'
else:
    _class = 'None'
    container = 'None'
shellName = repo+'0'+package
class arch_commands():
    install = ['yay', '-S', '{}'.format(package)]
    shellInstall = ['distrobox', 'enter', '{}'.format(shellName), '-r', '-e', 'yay', '-S', '--noconfirm', '{}'.format(package)]
    remove = ['yay', '-R', '{}'.format(package)]
    update = ['yay', '--noconfirm']
    shellUpdate = ['distrobox', 'enter', 'arch-template', '-r', '-e', 'yay', '--noconfirm']
    find = ['yay', '-Ss', '{}'.format(package)]
    run = ['distrobox', 'enter', 'arch-template', '-r', '-e', '{}'.format(package)]
    shell = ['distrobox', 'enter', 'arch-template', '-r', '-e', 'yay', '-S', '{}'.format(package)]
    createShell = ['distrobox', 'create', '-r', '--image', 'archlinux', '-n', 'arch-template', '-a', '--volume="$HOME/.Xauthority:/root/.Xauthority:rw"']
    removeShell = ['distrobox', 'rm', '-Y', '-r', 'arch-template']
class flatpak_commands():
    install = ['sudo', 'flatpak', 'install', '{}'.format(package)]
    remove = ['sudo', 'flatpak', 'remove', '{}'.format(package)]
    update = ['sudo', 'flatpak', 'update', '--assumeyes', '--noninteractive']
    find = ['sudo', 'flatpak', 'search', '{}'.format(package)]
    run = ['sudo', 'flatpak', 'run', '{}'.format(package)]
class fedora_commands():
    install = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'dnf', 'install', '{}'.format(package)]
    shellInstall = ['distrobox', 'enter', '{}'.format(shellName), '-r', '-e', 'sudo', 'dnf', 'install', '{}'.format(package)]
    remove = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'dnf', 'remove', '{}'.format(package)]
    update = ['distrobox', 'enter', 'fedora-template', '-r', '-e', 'sudo', 'dnf', 'update', '-y']
    find = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'dnf', 'search', '{}'.format(package)]
    run = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', '{}'.format(package)]
    createShell = ['distrobox', 'create', '-r', '--image', 'fedora', '-n', 'fedora-template', '-a', '--volume="$HOME/.Xauthority:/root/.Xauthority:rw"']
    removeShell = ['distrobox', 'rm', '-Y', '-r', 'fedora-template']
class debian_commands():
    install = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'apt', 'install', '{}'.format(package)]
    shellInstall = ['distrobox', 'enter', '{}'.format(shellName), '-r', '-e', 'sudo', 'apt', 'install', '{}'.format(package)]
    remove = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'apt', 'remove', '{}'.format(package)]
    update = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'update', '-y']
    upgrade = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'apt', 'upgrade', '-y']
    find = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', 'sudo', 'apt', 'search', '{}'.format(package)]
    run = ['distrobox', 'enter', '{}'.format(container), '-r', '-e', '{}'.format(package)]
    createShell = ['distrobox', 'create', '-r', '--image', 'debian', '-n', 'debian-template', '-a', '--volume="$HOME/.Xauthority:/root/.Xauthority:rw"']
    removeShell = ['distrobox', 'rm', '-Y', '-r', 'debian-template']
def stopBox():
    if args.shell == True:
        cmm(['distrobox', 'stop', '-Y', '-r', '{}'.format(shellName)])
    else:
        cmm(['distrobox', 'stop', '-Y', '-r', '{}'.format(container)])
class nix_commands():
    install = ['nix-env', '-iA', '--log-format', 'bar-with-logs', 'nixpkgs.{}'.format(package)]
    shell = ['nix-shell', '-p', '{}'.format(package)]
    remove = ['nix-env', '-e', '--log-format', 'bar-with-logs', '{}'.format(package)]
    collectGarbage = ['nix-collect-garbage', '-d', '--log-format', 'bar-with-logs']
    optimise = ['nix-store', '--optimise', '--log-format', 'bar-with-logs']
    channelUpdate = ['nix-channel', '--update', '--log-format', 'bar-with-logs']
    envUpdate = ['nix-env', '--upgrade', '--log-format', 'bar-with-logs']
    channelUpdate_root = ['sudo', 'nix-channel', '--update', '--log-format', 'bar-with-logs']
    envUpdate_root = ['sudo', 'nix-env', '--upgrade', '--log-format', 'bar-with-logs']
    find = ['firefox', '--private-window', 'https://search.nixos.org/packages?type=packages&query={}'.format(package)]
if repo == 'apt':
    _class = debian_commands
elif repo == 'dnf':
    _class = fedora_commands
elif repo == 'aur':
    _class = arch_commands
elif repo == 'nix':
    _class = nix_commands
elif repo == 'flatpak':
    _class = flatpak_commands
else:
    repo = 'nix'
    updateRepo = 'all'
    _class = nix_commands
def gainPrivs():
    cmm(['sudo', 'echo', 'Changing user privileges ->'])

if args.help == True:
    print('''
usage: nvv [-h] [-i] [-t] [-o] [-f] [-sh] [-r] [-gd] [-cc] [--generate-templates] [--refresh-templates] [-v] [-dbd]

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

Syntax:
nvv [command] [repo]:[package]
    Example:

        `nvv -i aur:firefox`

        This is going to install firefox using the Pacman package manager.
        
Nix is set to be the default package manager so if the repo is left blank then it will pull from there
    Example:

        `nvv -i :firefox`

        This is going to install firefox using the Nix package manager.
    
Inspired by Nix's shell environments allowing you try a 
package without permanently installing or touching system directories, 
I integrated distrobox for just this function. 
    
    Using the `--shell` arugment, a distrobox template will be duplicated, 
    afterwards, the package requested will be installed in that new container. 
    Upon exiting this container, it will be shut down and promptly deleted from 
    your system leaving no traces.
    (except anything that may have touched the home dir. )
    Example:

        `nvv -sh apt:firefox`

        This will duplicate the docker image 'debian-template' using distrobox,
        and then run the command 'sudo apt install firefox' within the container.
        Once you exit the container, it will be stopped, and deleted.

Updates are performed system wide.
    When a command like `nvv -o` is issued, 
    packages from pacman, nix (under both standard and root user), flatpak, apt, and dnf
    will be updated. 
    
    If you wish to update a single repo at a time, you can always specify.
    Example:

        `nvv -o aur:`

        This will update the base system using pacman (yay) and also the arch-template container.
    ''')
    exit()
if args.version:
    def getVersion():
        cmm(['neofetch', '--config', '/etc/pyrex/nvv/pyrexVersion.conf'.format(home_dir)])
    getVersion()
    exit()
elif args.debug == True:
    print('specin:', specin)
    print('shellName', shellName)
    print('repo:', repo)
    print('updateRepo:', updateRepo)
    print('package:', package)
    print('_class:', _class)
    print('container:', container)
    print(home_dir)
    print(config_dir)
    print(version_config)
    exit()
elif args.find == True:
    cmm(_class.find)
    exit()
elif args.install == True:
    gainPrivs()
    cmm(_class.install)
    if repo == 'apt' or repo == 'dnf':
        stopBox()
    exit()
elif args.shell == True:
    gainPrivs()
    if repo == 'nix':
        cmm(nix.shell)
    else:
        def shellWrapper():
            distrobox_create = ['distrobox', 'create', '-r', '-c', '{}'.format(container), '-n', '{}'.format(shellName), '-a', '--volume="$HOME/.Xauthority:/root/.Xauthority:rw"']
            distrobox_enter = ['distrobox', 'enter', '-r', '{}'.format(shellName)]
            distrobox_remove = ['distrobox', 'rm', '-Y', '-r', '{}'.format(shellName)]

            cmm(distrobox_create)
            cmm(_class.shellInstall)
            cmm(distrobox_enter)
            stopBox()
            cmm(distrobox_remove)
            
        shellWrapper()
    exit()
elif args.remove == True:
    gainPrivs()
    cmm(_class.remove)
    if repo == 'apt' or repo == 'dnf':
        stopBox()
    exit()
elif args.collectGarbage == True:
    cmm(nix_commands.collectGarbage)
    exit()
elif args.compactor == True:
    cmm(nix_commands.optimise)
    exit()
elif args.update == True:
    gainPrivs()
    def archUpdate():
        print('--------------------------------------\nSYSTEM:: Updating packages\n-----------------------------')
        cmm(arch_commands.update)
        print('--------------------------------------\nARCH-SHELL:: Updating packages\n-----------------------------')
        cmm(arch_commands.shellUpdate)
        return()
    def nixUpdate():
        print('--------------------------------------\nNIX-USER:: Updating repo\n-----------------------------')
        cmm(nix_commands.channelUpdate)
        print('--------------------------------------\nNIX-ROOT:: Updating repo\n-----------------------------')
        cmm(nix_commands.channelUpdate_root)
        time.sleep(15)
        print('--------------------------------------\nNIX-USER:: Updating packages\n-----------------------------')
        cmm(nix_commands.envUpdate)
        print('--------------------------------------\nNIX-ROOT:: Updating packages\n-----------------------------')
        cmm(nix_commands.envUpdate_root)
        return()
    def flatpakUpdate():
        print('--------------------------------------\nFLATPAK:: Updating packages\n-----------------------------')
        flatpakUpdate_proc = cmm(flatpak_commands.update)
        return()
    def debianUpdate():
        container = 'debian-template'
        print('--------------------------------------\nDEBIAN-SHELL:: Updating packages\n-----------------------------')
        debianUpdate_proc = cmm(debian_commands.update)
        print('--------------------------------------\nDEBIAN-SHELL:: Updating packages\n-----------------------------')
        debianUpgrade_proc = cmm(debian_commands.upgrade)
        return()
    def fedoraUpdate():
        container = 'fedora-template'
        print('--------------------------------------\nFEDORA-SHELL:: Updating packages\n-----------------------------')
        fedoraUpdate_proc = cmm(fedora_commands.update)
        return()
    archUpdateThread = threading.Thread(target=archUpdate)
    nixUpdateThread = threading.Thread(target=nixUpdate)
    flatpakUpdateThread = threading.Thread(target=flatpakUpdate)
    if updateRepo == 'all':
        archUpdateThread.start()
        time.sleep(1)
        nixUpdateThread.start()
        time.sleep(1)
        flatpakUpdateThread.start()
        debianUpdate()
        fedoraUpdate()
        stopBox
    elif updateRepo == 'nix':
        nixUpdate()
    else:
        cmm(_class.update)
        if updateRepo == 'aur':
            cmm(arch_commands.shellUpdate)
        if repo == 'apt' or repo == 'dnf':
            stopBox()
    exit()
if args.generate_templates == True:
    gainPrivs()
    print('Creating templates...')
    cmm(arch_commands.createShell)
    cmm(fedora_commands.createShell)
    cmm(debian_commands.createShell)
    #print('Preparing templates...')
if args.refresh_templates == True:
    gainPrivs()
    def debian_run():
        cmm(debian.run)
    def arch_run():
        cmm(arch.run)
    def fedora_run():
        cmm(fedora.run)
    def refresh_templates():
        print('Removing templates...')
        cmm(arch_commands.removeShell)
        cmm(fedora_commands.removeShell)
        cmm(debian_commands.removeShell)
        print('Creating templates...')
        cmm(arch_commands.createShell)
        cmm(fedora_commands.createShell)
        cmm(debian_commands.createShell)
        print('Preparing templates...')
        # debian_runThread = threading.Thread(target=debian_run)
        # fedora_runThread = threading.Thread(target=fedora_run)
        # arch_runThread = threading.Thread(target=arch_run)
        # debian_runThread.start()
        # arch_runThread.start()
        # fedora_runThread.start()
    refresh_templates()
elif args.run == True:
    gainPrivs()
    cmm(_class.run)
    stopBox()
    exit()
else:
    print('Use `nvv --help` for function details')