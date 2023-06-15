#!/usr/bin/env python3
import os
import argparse

syscall = os.system

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--install', dest='install', action='store_true', help='Install queried package.')
parser.add_argument('-sh', '--shell', dest='shell', action='store_true', help='Leverage `nix-shell` to test out queried package in a non-persistent shell environment')

parser.add_argument('-r', '--remove', dest='remove', action='store_true', help='Remove queried package')
parser.add_argument('-rl', '--remove-launcher', dest='removeLauncher', action='store_true', help='Manually delete launcher entry from ~/.local/share/applications/')
parser.add_argument('-cd', '--collect-garbage', dest='garbageCollection', action='store_true', help='Clean up unused directory paths from old packages and shells')

parser.add_argument('-u', '--update', dest='update', action='store_true', help='Update channels and installed packages.')

parser.add_argument('-q', '--query', dest='query', action='store_true', help='Search store for queried package')
parser.add_argument('-ls', '--list-installed', dest='listInstalled', action='store_true', help='Modification flag for --query. Specifies searching from installed packages rather than from store.')

parser.add_argument('--debug', dest='debug', action='store_true', help='Manually edit launcher entry')

parser.add_argument(dest='positionalArgument', action='append', nargs='?', help="Recommended to avoid requesting multiple packages in one command but if you do, put them quotes like so: nixed -i 'chromium firefox lynx'")

args = parser.parse_args()


positInput = '%s' % (args.positionalArgument)
noLbracket = positInput.replace('[', '')
noRbracket = noLbracket.replace(']', '')
noQuotes = noRbracket.replace("'", "")
positOut = noQuotes


def nur():
    print('Nix user repo support is coming soon')
def installMain():
    syscall('nix-env -iA %s' % (positOut))
    createLauncher()
def createLauncher():
    syscall('echo "[Desktop Entry]\nVersion=1.0\nType=Application\nName=%s\nComment=\nExec=%s\nIcon=%s\nPath=\nTerminal=false\nStartupNotify=false" >> ~/.local/share/applications/%s.desktop' % (positOut.capitalize(), positOut, positOut, positOut.capitalize()))
    exit()

def shellLaunch():
    syscall('nix-shell')
def shellInstall():
    if args.install == True:
        if positOut == 'None':
            print("Please select a package to test or drop the --install (`nixed --shell`) to invoke from shell.nix file")
            exit()
        else:
            syscall('nix-shell -p %s' % (positOut))

def removeMain():
    syscall('nix-env -e %s' % (positOut))
    removeLauncher()
    garbageCollection()

def removeLauncher():
    syscall('rm ~/.local/share/applications/%s.desktop' % (positOut.capitalize()))

def garbageCollection():
    syscall('nix-collect-garbage')
    syscall('nix-collect-garbage -d')

def updateMain():
    channelUpdate()
    pkgUpdate()

def pkgUpdate():
    syscall('nix-env -u')

def channelUpdate():
    syscall('nix-channel --update')


def listInstalled():
    if positOut == 'None':
        syscall('nix-env -q --installed')
    elif positOut != 'None':
        syscall('nix-env -q %s --installed' % (positOut))

def listAvailable():
    syscall('nix-env -q %s --available' % (positOut))

def editLauncher():
    syscall('nano ~/.local/share/applications/%s.desktop' % (positOut.capitalize()))
def renameLauncher():
    syscall('mv ~/.local/share/applications/%s.desktop ~/.local/share/applications/%s.desktop')

if args.shell == True:
    if args.install == True:
        shellInstall()
        exit()
    elif args.install != True:
        shellLaunch()
        exit()
if args.install == True:
    if args.shell != True:
        installMain()
        exit()
if args.remove == True:
    if args.install != True:
        removeMain()
        exit()
if args.update == True:
    updateMain()
    exit()
if args.garbageCollection == True:
    garbageCollection()
    exit()
if args.debug == True:
    if positOut == 'None':
        print('Please specify a package launcher you wish to correct')
        exit()
    if positOut != 'None':
        editLauncher()
        exit()
if args.removeLauncher == True:
    removeLauncher()
    exit()
if args.query == True:
    if args.listInstalled == True:
        listInstalled()
        exit()
    else:
        listAvailable()
        exit()
else:
    print("Unknown command '%s'\nType 'nixed -h' to view available options" % (positOut))