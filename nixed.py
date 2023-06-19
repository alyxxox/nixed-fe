#!/usr/bin/env python3
import os
import argparse
import threading

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', dest='help', action='store_true')
parser.add_argument('-i', '-install', dest='install', action='store_true', help='Install queried package.')
parser.add_argument('-sh', '-shell', dest='shell', action='store_true', help='Leverage `nix-shell` to test out queried package in a non-persistent shell environment')
parser.add_argument('-r', '-remove', dest='remove', action='store_true', help='Remove queried package')
parser.add_argument('-u', '-update', dest='update', action='store_true', help='Update channels and installed packages.')
parser.add_argument('-q', '-query', dest='query', action='store_true', help='Search store for queried package')
parser.add_argument('-ls', '-list.installed', dest='listInstalled', action='store_true', help='Modification flag for -query. Specifies searching from installed packages rather than from store.')
parser.add_argument('-nur', dest='nur', action='store_true', help='Use Nix User Repositories (nur.repos.*) rather than standard nixpkgs channel.')
parser.add_argument('-add.channel', dest='addChannel', action='store_true')
parser.add_argument('-remove.channel', dest='removeChannel', action='store_true')
parser.add_argument('-channel.list', dest='listChannels', action='store_true')
parser.add_argument('-cd', '-collect.garbage', dest='garbageCollection', action='store_true', help='Clean up unused directory paths from old packages and shells')
parser.add_argument('-remove.launcher', dest='removeLauncher', action='store_true', help='Manually delete launcher entry from paths.applications')
parser.add_argument('-first.time.setup', dest='firstTimeSetup', action='store_true')
parser.add_argument('-debug', dest='debug', action='store_true', help='Manually edit launcher entry')
parser.add_argument('-optimize.install.paths', dest='optimizeStore', action='store_true')
parser.add_argument('-test.paths',dest='testPaths',action='store_true',help='Debug option to test the directory pathing for .desktop files.')
parser.add_argument(dest='positionalArgument', action='append', nargs='?', help="Recommended to avoid requesting multiple packages in one command but if you do, put them quotes like so: nixed -i 'chromium firefox lynx'")
parser.add_argument(dest='positionalArgument2', action='append', nargs='?')
args = parser.parse_args()
class paths():
    applications = '~/.local/share/applications/'
    nixshell = '~/shell.nix'
class positParser():
    positInput = '%s' % (args.positionalArgument)
    noLbracket = positInput.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    positOut = noQuotes
class positParser2():
    positInput = '%s' % (args.positionalArgument2)
    noLbracket = positInput.replace('[', '')
    noRbracket = noLbracket.replace(']', '')
    noQuotes = noRbracket.replace("'", "")
    positOut2 = noQuotes
class install():
    # nur or nix user repositories is a community driven repo for various nixpkgs
    def nur():
        os.system("nix-env -f '<nixpkgs>' -iA nur.repos.%s" % (positParser.positOut))
    def main():
        os.system('nix-env -iA nixpkgs.%s' % (positParser.positOut))
        install.createLauncher()
    # nix doesn't like to create launcher file for integration with DE's        
    def createLauncher():
        os.system('echo "[Desktop Entry]\nVersion=1.0\nType=Application\nName=%s\nComment=\nExec=%s\nIcon=%s\nPath=\nTerminal=false\nStartupNotify=false" >> %s%s.desktop' % (positParser.positOut.capitalize(), positParser.positOut, positParser.positOut, paths.applications, positParser.positOut.capitalize()))
    class firstTimeSetup():
        def alert():
            print('support for doing a fully automated functional nix installation with minimal user input in the works.')
        def nixInstall():
            distro = input('Please choose distro:\n1. arch 2. debian 3. opensuse 4. alpine\n')
            if distro == 'arch':
                os.system('sudo pacman -S nix --noconfirm')
            elif distro == 'debian':
                os.system('sudo apt-get install nix')
        def nixChannelAdd():
            branch = input('Would you like the default nixpkgs channel (https://nixos.org/channels/nixpkgs-unstable\n) or use custom channel?\n1 for default; 2 for custom')
            if branch == '1':
                os.system('nix-channel --add https://nixos.org/channels/nixpkgs-unstable nixos')
                os.system('nix-channel --update')
            if branch == '2':
                os.system('nix-channel --add %s' % (positParser.positOut))
                os.system('nix-channel --update')
class shell():
    def launch():
        os.system('nix-shell')
    def nur():
        os.system('nix-shell -p nur.repos.%s' % (positParser.positOut))
    def install():
        if positParser.positOut == 'None':
            print("Please select a package to test or drop the --install (`nixed --shell`) to invoke from shell.nix file")
            exit()
        else:
            os.system('nix-shell -p %s' % (positParser.positOut))
class remove():
    def main():
        os.system('nix-env -e %s' % (positParser.positOut))
        remove.removeLauncher()
        remove.garbageCollection()
    def removeLauncher():
        os.system('rm %s%s.desktop' % (paths.applications, positParser.positOut.capitalize()))
    # clear up no longer used profile/dependency directories
    def garbageCollection():
        os.system('nix-collect-garbage')
        os.system('nix-collect-garbage -d')
class update():
    def main():
        update.channelUpdate()
        update.pkgUpdate()
    def pkgUpdate():
        os.system('nix-env -u')
    def channelUpdate():
        os.system('nix-channel --update')
class query():
    def available():
        if positParser.positOut == 'None':
            print('Please select a paposckage to query')
        else:
            os.system('nix-env -q %s --available' % (positParser.positOut))
    def listInstalled():
        if positParser.positOut == 'None':
            os.system('nix-env -q --installed')
        elif positParser.positOut != 'None':
            os.system('nix-env -q %s --installed' % (positParser.positOut))
class debug():
    def editLauncher():
        os.system('nano %s%s.desktop' % (paths.applications, positParser.positOut.capitalize()))
    def testPaths():
        print('%s%s' % (paths.applications, positParser.positOut))
    def optimizeStore():
        os.system('nix-store --optimize')
    def help():
        print(
'''
    shortform: nixed [-i] [-sh] [-r] [-u] [-q] [-ls]

    tip:
        Put multiple packages in quotes like so;
            nixed -i 'chromium lynx firefox'

    options:
        -install
            Install queried package. 
                nixed -i package_name
        -shell
            Leverage `nix-shell` to test out queried package in a non-persistent shell environment
                nixed -sh -i package_name
        -remove
            Remove queried package
                nixed -r package_name
        -update
            Update channels and installed packages.
                nixed -u
        -query
            Search store for queried package
                nixed -q package_name
        -list.installed
            Modification flag for --query. Specifies searching from installed packages rather than from store.
                nixed -ls
        -add.channel
            Add channel for nixpkgs to be queried from
                nixed -channel.add https://example.com/example-repo/ repo_name
        -remove.channel
            Remove channel from repo list
                nixed -channel.remove repo_name
        -channel.list
            List repo channels currently added to Nix package manager
                nixed -channel.list
        -collect.garbage
            Clean up unused directory paths from
        -first.time.setup
            old packages and shells
                nixed -cd
        -remove.launcher
            Manually delete launcher entry from paths.applications
                nixed -remove.launcher
'''
    )
class channel():
    def addChannel():
        print('nix-channel --add %s %s' % (positParser.positOut, positParser2.positOut2))
        #os.system('nix-channel --update')
    def removeChannel():
        os.system('nix-channel --remove %s' % (positParser.positOut))
    def listChannels():
        os.system('nix-channel --list')
if args.firstTimeSetup == True:
    install.firstTimeSetup.nixInstall()
    install.firstTimeSetup.nixChannelAdd()
    exit()
## logic for systemwide installation
if args.install == True:
    if args.remove != True:
        if args.shell != True:
            if args.nur == True:
                install.nur()
                exit()
            else:
                install.main()
                exit()
## logic for shell environments
if args.shell == True:
    if args.install == True:
        if args.nur == True:
            shell.nur()
            exit()
        else:
            shell.install()
            exit()
    if args.install != True:
        if args.debug == True:
            os.system('code %s' % (paths.nixshell))
            exit()
        if positParser.positOut != 'None':
            print('`nixed --shell` default behavior is to launch from shell.nix configuration.\nIf you wanted to try %s in a shell container use `nixed --shell --install %s`. :)' % (positParser.positOut, positParser.positOut))
            exit()
        else:
            shell.launch()
            exit()
## logic for package removal
if args.remove == True:
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
## logic for package updates
if args.update == True:
    update.main()
    exit()
## logic for package queries
if args.query == True:
    query.available()
    exit()
if args.listInstalled == True:
    query.listInstalled()
    exit()
if args.addChannel == True:
    channel.addChannel()
    exit()
if args.removeChannel == True:
    channel.removeChannel()
    exit()
if args.listChannels == True:
    channel.listChannels()
    exit()
## logic for debug functions
if args.debug == True:
    if positParser.positOut == 'None':
        print('Please specify a package launcher you wish to correct')
        exit()
    if positParser.positOut != 'None':
        if args.testPaths == True:
            debug.testPaths()
            exit()
        debug.editLauncher()
        exit()
## if all else fails
if args.help == True or positParser.positOut == 'help':
    debug.help()
    exit()
if args.optimizeStore == True:
    debug.optimizeStore()
    exit()
else:
    print("Unknown command '%s'\nType 'nixed --help' to view available options" % (positParser.positOut))
