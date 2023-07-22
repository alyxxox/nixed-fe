#!/usr/bin/env python3
import os 
import argparse
import threading
parser = argparse.ArgumentParser(
    description='Pyrex2 package manager/wrapper. Built with the intention of simplifying package distribution via declarative initialisation of nix, pacman, flatpak, and npm in one function.', 
    epilog='Use nix.[unit], aur.[unit], flatpak.[unit], or npm.[unit] to specify source.\nexample: pyrex --station aur.firefox')
parser.add_argument('-s', '--station', dest='install', action='store_true', help='Install units')
parser.add_argument('-t', '--trash', dest='remove', action='store_true', help='Remove units')
parser.add_argument('-o', '--overhaul', dest='update', action='store_true', help='Update system')
parser.add_argument('-f', '--find', dest='find', action='store_true', help='find units')
parser.add_argument('-rr', '--rebase', dest='source', action='store_true', help='Build and install unit from source (Nix only for now)')
parser.add_argument('-gc', '--garbage-collector', dest='collectGarbage', action='store_true', help='Collect unused units/paths (nix only for now)')
parser.add_argument('-c', '--compactor', dest='compactor', action='store_true', help='Consolidate shared dependencies to save storage and optimize file paths at the expense of less reproducibility. (Set to true per install by default)')
parser.add_argument('--shell', dest='shell', action='store_true', help='Install unit in non-persistent shell environment. (nix only for now)')
parser.add_argument(dest='stdinn', action='append', nargs='?')

# user configs #
class configs():
    autoCompactor = True
    autoCollectGarbage = False
    autoRebase = False

args = parser.parse_args()
class cliParser():
    initarg = '%s' % (args.stdinn)
    noLbracket = initarg.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    specin = noQuotes
# add custom maintained installed units list >>
def compactor():
    os.system('nix-store --optimise --log-format bar-with-logs')
if args.install == True:
    if args.shell == True:
        if 'nix.' in cliParser.specin:
            unit = cliParser.specin.replace('nix.', '')
            os.system('nix-shell -p --log-format bar-with-logs %s' % (unit))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system('nix-shell -p --log-format bar-with-logs %s' % (cliParser.specin))
            exit()
    else:
        if 'nix.' in cliParser.specin:
            unit = cliParser.specin.replace('nix.', '')
            os.system('nix-env -iA --log-format bar-with-logs nixpkgs.%s' % (unit))
            if configs.autoRebase == True:
                os.system('nix-build "<nixpkgs>" -A %s --check' % (unit))
            if configs.autoCompactor == True:
                compactor()
            exit()
        elif 'aur.' in cliParser.specin:
            unit = cliParser.specin.replace('aur.', '')
            os.system('yay -S %s' % (unit))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system("nix-env -f '<nixpkgs>' -iA --log-format bar-with-logs %s" % (cliParser.specin))
            os.system('nix-store --optimize --log-format bar-with-logs')
            exit()
        elif 'flatpak.' in cliParser.specin:
            unit = cliParser.specin.replace('flatpak.', '')
            os.system('flatpak install %s' % (unit))
            exit()
        elif 'npm.' in cliParser.specin:
            unit = cliParser.specin.replace('npm.', '')
            os.system('npm install %s' % (unit))
            exit()
if args.compactor == True:
    compactor()
    exit()
def collectGarbage():
    os.system('nix-collect-garbage -d --log-format bar-with-logs')
    #os.system('nix-collect-garbage')
if args.source == True:
    if args.shell == True:
        if 'nix.' in cliParser.specin:
            unit = cliParser.specin.replace('nix.', '')
            os.system('nix-shell -p --option substitute false --log-format bar-with-logs %s' % (unit))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system('nix-shell -p --option substitute false --log-format bar-with-logs %s' % (cliParser.specin))
            exit()
    else:
        if 'nix.' in cliParser.specin:
            unit = cliParser.specin.replace('nix.', '')
            os.system('nix-env -iA --option substitute false --log-format bar-with-logs nixpkgs.%s' % (unit))
            exit()
        elif 'nur.' in cliParser.specin:
            os.system("nix-env -f '<nixpkgs>' -iA --option substitute false --log-format bar-with-logs %s" % (cliParser.specin))
            exit()
if args.remove == True:
    if 'nix.' in cliParser.specin:
        unit = cliParser.specin.replace('nix.', '')
        os.system('nix-env -e --log-format bar-with-logs %s' % (unit))
        if configs.autoCollectGarbage == True:
            collectGarbage()
        exit()
    elif 'aur.' in cliParser.specin:
        unit = cliParser.specin.replace('aur.', '')
        os.system('yay -R %s' % (unit))
        exit()
    elif 'flatpak.' in cliParser.specin:
        unit = cliParser.specin.replace('flatpak.', '')
        os.system('flatpak remove %s' % (unit))
        exit()
    elif 'npm.' in cliParser.specin:
        unit = cliParser.specin.replace('npm.', '')
        os.system('npm remove %s' % (unit))
        exit()
class update():
    def nix():
        if args.source == True:
            os.system('nix-channel --update --log-format bar-with-logs')
            os.system('nix-env --upgrade --option substitute false --log-format bar-with-logs')
        else:
            os.system('nix-channel --update --log-format bar-with-logs')
            os.system('nix-env --upgrade --log-format bar-with-logs')
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
def nixFind():
    unit = cliParser.specin.replace('nix.', '')
    if '.installed' in cliParser.specin:
        if unit == 'installed':
            print('Installed nixpkgs:')
            os.system('nix-env -q --installed >> ~/.nix-installed.txt')
        else:
            noInstall = unit.replace('.installed', '')
            os.system('nix-env -q %s --installed >> ~/.nix-installed.txt' % (noInstall))
        os.system('cat ~/.nix-installed.txt')
        os.system('rm ~/.nix-installed.txt')
        exit()
    else:
        os.system('nix-env -q %s --available' % (unit)) #>> ~/.nix-search.txt' % (unit))
        # print('Available nixpkgs:')
        # os.system('cat ~/.nix-search.txt')
        # os.system('rm ~/.nix-search.txt')
        exit()
def aurFind():
    unit = cliParser.specin.replace('aur.', '')
    if '.installed' in cliParser.specin:
        os.system('yay -Ss')
        exit()
    else:
        print('Available AUR units:')
        os.system('yay -Ss %s' % (unit))
        exit()
def flatpakFind():
    unit = cliParser.specin.replace('flatpak.', '')
    if '.installed' in cliParser.specin:
        os.system('flatpak list')
        exit()
    else:
        print('Available Flatpak units:')
        os.system('flatpak search %s' % (unit))
        exit()
def npmFind():
    unit = cliParser.specin.replace('npm.', '')
    if '.installed' in cliParser.specin:
        os.system('npm list')
        exit()
    else:
        print('Available node.js units:')
        os.system('npm search %s' % (unit))
        exit()
nixSearch = threading.Thread(target=nixFind)
aurSearch = threading.Thread(target=aurFind)
flatpakSearch = threading.Thread(target=flatpakFind)
npmSearch = threading.Thread(target=npmFind)
if args.find == True:
    if 'nix.' in cliParser.specin:
        nixFind()
    elif 'aur.' in cliParser.specin:
        aurFind()
    elif 'flatpak.' in cliParser.specin:
        flatpakFind()
    elif 'npm.' in cliParser.specin:
        npmFind()
    elif cliParser.specin == 'installed':
        def listunits():
            print('To avoid flooding terminal with text, pacman units are retained to their own command. Use "pyrex -q aur.installed" to see those units.\n')
            os.system('echo "Nix units:" >> ~/.pkgs-installed.txt')
            os.system('nix-env -q --installed >> ~/.pkgs-installed.txt')
            #os.system('echo "\nFlatpaks:" >> ~/.pkgs-installed.txt')
            os.system('echo "\nnode.js units:" >> ~/.pkgs-installed.txt')
            os.system('npm list >> ~/.pkgs-installed.txt')
            os.system('cat ~/.pkgs-installed.txt')
            print('Flatpaks:')
            os.system('flatpak list') #>> ~/.pkgs-installed.txt')
            os.system('rm ~/.pkgs-installed.txt') 
        listunits()
        exit()
    else:
        nixSearch.start()
        #aurSearch.start()
        flatpakSearch.start()
        npmSearch.start()

if args.collectGarbage == True:
    collectGarbage()
    exit()

elif cliParser.specin == 'None':
    os.system('pyrex -h')