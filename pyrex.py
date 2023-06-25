#!/usr/bin/env python3
import os 
import argparse
parser = argparse.ArgumentParser(
    description='Pyrex2 package manager/wrapper. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak, and npm in one function.', 
    epilog='Use nix.[package], aur.[package], flatpak.[package], or npm.[package] to specify source.\nexample: pyrex --order aur.firefox')
parser.add_argument('-s', '--station', dest='install', action='store_true', help='Install packages (nix., aur., flatpak., npm.,)')
parser.add_argument('-t', '--trash', dest='remove', action='store_true', help='Remove packages (nix., aur., flatpak., npm.,)')
parser.add_argument('-o', '--overhaul', dest='update', action='store_true', help='Update system')
parser.add_argument('-f', '--find', dest='find', action='store_true', help='find packages (nix., aur., flatpak., npm.,)')
parser.add_argument('-bs', '--build-source', dest='source', action='store_true', help='Build and install package from source (Nix only for now)')
parser.add_argument('-rd', '--remove-debris', dest='collectGarbage', action='store_true', help='Collect unused packages/paths (nix only for now)')
parser.add_argument('-c', '--compactor', dest='compactor', action='store_true', help='Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to true by default)')
parser.add_argument('--shell', dest='shell', action='store_true', help='Install package in non-persistent shell environment. (nix only for now)')
parser.add_argument(dest='stdinn', action='append', nargs='?')

args = parser.parse_args()
class cliParser():
    initarg = '%s' % (args.stdinn)
    noLbracket = initarg.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    specin = noQuotes
if args.install == True:
    if args.shell == True:
        if 'nix.' in cliParser.specin:
            package = cliParser.specin.replace('nix.', '')
            os.system('nix-shell -p --log-format bar-with-logs %s' % (package))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system('nix-shell -p --log-format bar-with-logs %s' % (cliParser.specin))
            exit()
    else:
        if 'nix.' in cliParser.specin:
            package = cliParser.specin.replace('nix.', '')
            os.system('nix-env -iA --log-format bar-with-logs nixpkgs.%s' % (package))
            os.system('nix-store --optimize --log-format bar-with-logs')
            exit()
        elif 'aur.' in cliParser.specin:
            package = cliParser.specin.replace('aur.', '')
            os.system('yay -S %s' % (package))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system("nix-env -f '<nixpkgs>' -iA --log-format bar-with-logs %s" % (cliParser.specin))
            exit()
        elif 'flatpak.' in cliParser.specin:
            package = cliParser.specin.replace('flatpak.', '')
            os.system('flatpak install %s' % (package))
            exit()
        elif 'npm.' in cliParser.specin:
            package = cliParser.specin.replace('npm.', '')
            os.system('npm install %s' % (package))
            exit()
if args.compactor == True:
    os.system('nix-store --optimise --log-format bar-with-logs')
    exit()
def collectGarbage():
    os.system('nix-collect-garbage -d --log-format bar-with-logs')
    #os.system('nix-collect-garbage')
if args.source == True:
    if args.shell == True:
        if 'nix.' in cliParser.specin:
            package = cliParser.specin.replace('nix.', '')
            os.system('nix-shell -p --option substitute false --log-format bar-with-logs %s' % (package))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system('nix-shell -p --option substitute false --log-format bar-with-logs %s' % (cliParser.specin))
            exit()
    else:
        if 'nix.' in cliParser.specin:
            package = cliParser.specin.replace('nix.', '')
            os.system('nix-env -iA --option substitute false --log-format bar-with-logs nixpkgs.%s' % (package))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system("nix-env -f '<nixpkgs>' -iA --option substitute false --log-format bar-with-logs %s" % (cliParser.specin))
            exit()
if args.remove == True:
    if 'nix.' in cliParser.specin:
        package = cliParser.specin.replace('nix.', '')
        os.system('nix-env -e --log-format bar-with-logs %s' % (package))
        #collectGarbage()
        exit()
    elif 'aur.' in cliParser.specin:
        package = cliParser.specin.replace('aur.', '')
        os.system('yay -R %s' % (package))
        exit()
    elif 'flatpak.' in cliParser.specin:
        package = cliParser.specin.replace('flatpak.', '')
        os.system('flatpak remove %s' % (package))
        exit()
    elif 'npm.' in cliParser.specin:
        package = cliParser.specin.replace('npm.', '')
        os.system('npm remove %s' % (package))
        exit()
class update():
    def nix():
        os.system('nix-channel --update --log-format bar-with-logs')
        os.system('nix-env --upgrade --option substitute false --log-format bar-with-logs')
    def aur():
        os.system('yay')
    def flatpak():
        os.system('flatpak update')
    def npm():
        os.system('npm update')
if args.update == True:
    if cliParser.specin == 'None':
        update.nix()
        update.aur()
        update.flatpak()
        update.npm()
        exit()
    elif cliParser.specin == 'nix':
        update.nix()
        exit()
    elif cliParser.specin == 'aur':
        update.aur()
        exit()
    elif cliParser.specin == 'flatpak':
        update.flatpak()
        exit()
    elif cliParser.specin == 'npm':
        update.npm()
        exit()
if args.find == True:
    if 'nix.' in cliParser.specin:
        package = cliParser.specin.replace('nix.', '')
        if '.installed' in cliParser.specin:
            os.system('echo "Nix packages:" >> ~/.nix-installed.txt')
            os.system('nix-env -q --installed >> ~/.nix-installed.txt')
            os.system('cat ~/.nix-installed.txt')
            os.system('rm ~/.nix-installed.txt')
            exit()
        else:
            os.system('nix-env -q %s --available' % (package))
            exit()
    elif 'aur.' in cliParser.specin:
        package = cliParser.specin.replace('aur.', '')
        if '.installed' in cliParser.specin:
            os.system('yay -Ss')
            exit()
        else:
            os.system('yay -Ss %s' % (package))
            exit()
    elif 'flatpak.' in cliParser.specin:
        package = cliParser.specin.replace('flatpak.', '')
        if '.installed' in cliParser.specin:
            os.system('flatpak list')
            exit()
        else:
            os.system('flatpak search %s' % (package))
            exit()
    elif 'npm.' in cliParser.specin:
        package = cliParser.specin.replace('npm.', '')
        if '.installed' in cliParser.specin:
            os.system('npm list')
            exit()
        else:
            os.system('npm search %s' % (package))
            exit()
    elif cliParser.specin == 'installed':
        def listpackages():
            print('To avoid flooding terminal with text, pacman packages are retained to their own command. Use "pyrex -q aur.installed" to see those packages.\n')
            os.system('echo "Nix packages:" >> ~/.pkgs-installed.txt')
            os.system('nix-env -q --installed >> ~/.pkgs-installed.txt')
            #os.system('echo "\nFlatpaks:" >> ~/.pkgs-installed.txt')
            os.system('echo "\nnode.js packages:" >> ~/.pkgs-installed.txt')
            os.system('npm list >> ~/.pkgs-installed.txt')
            os.system('cat ~/.pkgs-installed.txt')
            print('Flatpaks:')
            os.system('flatpak list') #>> ~/.pkgs-installed.txt')
            os.system('rm ~/.pkgs-installed.txt')
        listpackages()
        exit()

if args.collectGarbage == True:
    collectGarbage()
    exit()

elif cliParser.specin == 'None':
    os.system('pyrex -h')