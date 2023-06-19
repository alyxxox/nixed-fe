# nixed-fe
Nixed Frontend is a frontend/syntax wrapper for nix package manager (intended for Darwin builds.) Developed and tested on Arch Linux with Xfce4
```
shortform: nixed [-i] [-sh] [-r] [-u] [-q] [-ls]

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
```
