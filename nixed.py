#!/usr/bin/env python3
import os
import argparse

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

class positParser():
    positInput = '%s' % (args.positionalArgument)
    noLbracket = positInput.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    positOut = noQuotes

class install():
    def nur():
        print('Nix user repo support is coming soon')
    def main():
        os.system('nix-env -iA %s' % (positParser.positOut))
        install.createLauncher()
    def createLauncher():
        os.system('echo "[Desktop Entry]\nVersion=1.0\nType=Application\nName=%s\nComment=\nExec=%s\nIcon=%s\nPath=\nTerminal=false\nStartupNotify=false" >> ~/.local/share/applications/%s.desktop' % (positParser.positOut.capitalize(), positParser.positOut, positParser.positOut, positParser.positOut.capitalize()))
        exit()
if args.install == True:
    if args.shell != True:
        install.main()
        exit()
class shell():
    def launch():
        os.system('nix-shell')
    def install():
        if args.install == True:
            if positParser.positOut == 'None':
                print("Please select a package to test or drop the --install (`nixed --shell`) to invoke from shell.nix file")
                exit()
            else:
                os.system('nix-shell -p %s' % (positParser.positOut))
if args.shell == True:
    if args.install == True:
        shell.install()
        exit()
    elif args.install != True:
        shell.launch()
        exit()
class remove():
    def main():
        os.system('nix-env -e %s' % (positParser.positOut))
        remove.removeLauncher()
        remove.garbageCollection()
    def removeLauncher():
        os.system('rm ~/.local/share/applications/%s.desktop' % (positParser.positOut.capitalize()))
    def garbageCollection():
        os.system('nix-collect-garbage')
        os.system('nix-collect-garbage -d')
if args.remove == True:
    if args.install != True:
        remove.main()
        exit()
if args.garbageCollection == True:
    if args.remove != True:
        remove.garbageCollection()
        exit()
if args.removeLauncher == True:
    if args.remove != True:
        remove.removeLauncher()
        exit()
class update():
    def main():
        update.channelUpdate()
        update.pkgUpdate()
    def pkgUpdate():
        os.system('nix-env -u')
    def channelUpdate():
        os.system('nix-channel --update')
if args.update == True:
    update.main()
    exit()
class query():
    def listInstalled():
        if positParser.positOut == 'None':
            os.system('nix-env -q --installed')
        elif positParser.positOut != 'None':
            os.system('nix-env -q %s --installed' % (positParser.positOut))
    def listAvailable():
        os.system('nix-env -q %s --available' % (positParser.positOut))
if args.query == True:
    if args.listInstalled == True:
        query.listInstalled()
        exit()
    else:
        query.listAvailable()
        exit()
else:
    print("Unknown command '%s'\nType 'nixed -h' to view available options" % (positParser.positOut))
class debug():
    def editLauncher():
        os.system('nano ~/.local/share/applications/%s.desktop' % (positParser.positOut.capitalize()))
    def renameLauncher():
        os.system('mv ~/.local/share/applications/%s.desktop ~/.local/share/applications/%s.desktop')
if args.debug == True:
    if positParser.positOut == 'None':
        print('Please specify a package launcher you wish to correct')
        exit()
    if positParser.positOut != 'None':
        debug.editLauncher()
        exit()






