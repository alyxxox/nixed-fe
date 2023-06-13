#!/usr/bin/env python3
import os
import argparse

syscall = os.system

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--install', dest='install', action='store_true', help='Install queried package.')
parser.add_argument('-r', '--remove', dest='remove', action='store_true', help='Remove queried package')
parser.add_argument('-cd', '--collect-garbage', dest='garbageCollection', action='store_true', help='Clean up unused directory paths from old packages and shells')
parser.add_argument('-u', '--update', dest='update', action='store_true', help='Update channels and installed packages.')
parser.add_argument('-tt', '--test', dest='shell', action='store_true', help='Leverage `nix-shell` to test out queried package in a non-persistent shell environment prior to installation')
parser.add_argument('-q', '--query', dest='query', action='store_true', help='Search store for queried package')
parser.add_argument('-ls', '--list-installed', dest='listInstalled', action='store_true', help='Modification flag for --query. Specifies searching from installed packages rather than from store.')
parser.add_argument('--debug', dest='debug', action='store_true')
parser.add_argument(dest='positionalArgument', action='append', nargs='?', help="Recommended to avoid requesting multiple packages in one command but if you do, put them quotes like so: nixed -i 'chromium firefox lynx'")

args = parser.parse_args()
class positParser():
    positInput = '%s' % (args.positionalArgument)
    noLbracket = positInput.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    positOut = noQuotes

class install():
    def nur():
        print('Nix user repo support is coming soon')
    def now():
        syscall('nix-env -iA nixpkgs.%s' % (positParser.positOut))
        install.createLauncher()
    def createLauncher():
        syscall('echo "[Desktop Entry]\nVersion=1.0\nType=Application\nName=%s\nComment=\nExec=%s\nIcon=%s\nPath=\nTerminal=false\nStartupNotify=false" >> ~/.local/share/applications/%s.desktop' % (positParser.positOut.capitalize(), positParser.positOut, positParser.positOut, positParser.positOut.capitalize()))
        exit()
class remove():
    def now():
        syscall('nix-env -e %s' % (positParser.positOut))
        remove.removeLauncher()
        remove.garbageCollection()

    def removeLauncher():
        syscall('rm ~/.local/share/applications/%s.desktop' % (positParser.positOut.capitalize()))

    def garbageCollection():
        syscall('nix-collect-garbage')
        syscall('nix-collect-garbage -d')

class shell():
    def now():
        syscall('nix-shell -p %s' % (positParser.positOut))

class update():
    def now():
        update.channelUpdate()
        update.pkgUpdate()

    def pkgUpdate():
        syscall('nix-env -u')

    def channelUpdate():
        syscall('nix-channel --update')

if args.install == True:
    install.now()
elif args.shell == True:
    shell.now()
elif args.remove == True:
    remove.now()
if args.update == True:
    update.now()
if args.garbageCollection == True:
    remove.garbageCollection()
if args.debug == True:
    install.createLauncher()