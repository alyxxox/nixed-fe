#!/usr/bin/env python3

import subprocess
import argparse
import threading
import time

parser = argparse.ArgumentParser(description='Pyrex4 System Manager. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak in one function.',)
parser.add_argument('-i', '--install', dest='install', action='store_true', help='Install packages')
parser.add_argument('-t', '--trash', dest='remove', action='store_true', help='Remove packages')
parser.add_argument('-o', '--overhaul', dest='update', action='store_true', help='Update system')
parser.add_argument('-f', '--find', dest='find', action='store_true', help='Find packages')
#parser.add_argument('--verbose', dest='verbose', action='store_true', help='Require user confirmation before any command is processed. (Currently only implemented with AUR)')
#parser.add_argument('-fs', '--from-scratch', dest='source', action='store_true', help='Build and install package from source (Nix only for now)')
parser.add_argument('-sh', '--shell', dest='shell', action='store_true', help='Install package in non-persistent shell environment. (Does not support Flatpak)')
parser.add_argument('-r', '--run', dest='run', action='store_true')
parser.add_argument('-gd', '--garbage-disposal', dest='collectGarbage', action='store_true', help='Collect unused packages/paths (Nix function)')
parser.add_argument('-cc', '--compact', dest='compactor', action='store_true', help='Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to False per install by default)')
parser.add_argument('-v', '--version', dest='version', action='store_true', help='Show version number')
parser.add_argument('--debug-parser', dest='debug', action='store_true', help="Prints the raw output of the input parser. For debugging purposes and shouldn't be included in final release")
parser.add_argument(dest='package', action='append', nargs='?', help='must be the last argument presented')
args = parser.parse_args()
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
class arch_commands():
    install = ['yay', '-S', '{}'.format(package)]
    remove = ['yay', '-R', '{}'.format(package)]
    update = ['yay', '--noconfirm']
    find = ['yay', '-Ss', '{}'.format(package)]
    run = ['distrobox', 'enter', 'arch-template', '-r', '-e', '{}'.format(package)]
    shell = ['distrobox', 'enter', 'arch-template', '-r', '-e', 'yay', '-S', '{}'.format(package)]
class flatpak_commands():
    install = ['flatpak', 'install', '{}'.format(package)]
    remove = ['flatpak', 'remove', '{}'.format(package)]
    update = ['flatpak', 'update', '--assumeyes', '--noninteractive']
    find = ['flatpak', 'search', '{}'.format(package)]
class fedora_commands():
    install = ['distrobox', 'enter', 'fedora-template', '-r', '-e', 'sudo', 'dnf', 'install', '{}'.format(package)]
    remove = ['distrobox', 'enter', 'fedora-template', '-r', '-e', 'sudo', 'dnf', 'remove', '{}'.format(package)]
    update = ['distrobox', 'enter', 'fedora-template', '-r', '-e', 'sudo', 'dnf', 'update', '-y']
    find = ['distrobox', 'enter', 'fedora-template', '-r', '-e', 'sudo', 'dnf', 'search', '{}'.format(package)]
    run = ['distrobox', 'enter', 'fedora-template', '-r', '-e', '{}'.format(package)]
class debian_commands():
    install = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'install', '{}'.format(package)]
    remove = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'remove', '{}'.format(package)]
    update = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'update', '-y']
    upgrade = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'upgrade', '-y']
    find = ['distrobox', 'enter', 'debian-template', '-r', '-e', 'sudo', 'apt', 'search', '{}'.format(package)]
    run = ['distrobox', 'enter', 'debian-template', '-r', '-e', '{}'.format(package)]
def stopBox():
    subprocess.call(['distrobox', 'stop', '-Y', '-r', '{}'.format(container)])
class nix_commands():
    install = ['nix-env', '-iA', '--log-format', 'bar-with-logs', '{}'.format(package)]
    shell = ['nix-shell', '-p', '{}'.format(package)]
    remove = ['nix-env', '-e', '--log-format', 'bar-with-logs', '{}'.format(package)]
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
def gainPrivs():
    subprocess.call(['sudo', 'echo', 'Changing user privileges ->'])
if args.version:
    print('Pyrex System Manager (nv) version 5.2.1')
    exit()
if args.debug == True:
    print('Specin:', specin)
    print('Repo:', repo)
    print('Package:', package)
    print('Class:', _class)
    print('Container:', container)
    exit()
    #print(class.install)
if args.find == True:
    subprocess.call(_class.find)
    exit
if args.install == True:
    gainPrivs()
    subprocess.call(_class.install)
    exit()
if args.shell == True:
    gainPrivs()
    subprocess.call(_class.shell)
    exit()
elif args.remove == True:
    gainPrivs()
    subprocess.call(_class.remove)
    #if repo == 'apt' or 'dnf':
    #    stopBox()
    exit()
elif args.update == True:
    gainPrivs()
    def archUpdate():
        subprocess.call(arch_commands.update)
        return()
    def nixUpdate():
        subprocess.Popen(nix_commands.channelUpdate)
        subprocess.call(nix_commands.channelUpdate_root)
        subprocess.Popen(nix_commands.envUpdate)
        subprocess.call(nix_commands.envUpdate_root)
        return()
    def flatpakUpdate():
        flatpakUpdate_proc = subprocess.call(flatpak_commands.update)
        #flatpakUpdate_proc.communicate()[0]
        return()
    def debianUpdate():
        container = 'debian-template'
        debianUpdate_proc = subprocess.call(debian_commands.update)
        debianUpgrade_proc = subprocess.call(debian_commands.upgrade)
        #debianUpdate_proc.communicate()[0]
        return()
        #stopBox()
    def fedoraUpdate():
        container = 'fedora-template'
        fedoraUpdate_proc = subprocess.call(fedora_commands.update)
        #fedoraUpdate_proc.communicate()[0]
        return()
        #stopBox()
    archUpdateThread = threading.Thread(target=archUpdate)
    nixUpdateThread = threading.Thread(target=nixUpdate)
    flatpakUpdateThread = threading.Thread(target=flatpakUpdate)
    #debianUpdateThread = threading.Thread(target=debianUpdate)
    #fedoraUpdateThread = threading.Thread(target=fedoraUpdate)
    if repo == 'None':
        archUpdateThread.start()
        nixUpdateThread.start()
        flatpakUpdateThread.start()
        debianUpdate()
        fedoraUpdate()
    elif repo == 'nix':
        nixUpdate()
    else:
        subprocess.call(_class.update)
    exit()
if args.run == True:
    gainPrivs()
    subprocess.call(_class.run)
    exit()
print('Use `nv --help` for function details')
