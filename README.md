# CSSHY - Alpha Version

Imporved ClusterSSH for modern terminals like terminator and tilix, to manage a cluster of nodes through ssh connections
launches multiple splits with ssh connections to each node

## TODO
* Add command line arguments to create/remove/modify cluster so there is no need to edit json files
* Improve `guess` terminal detection for other DE (KDE and XFCE at least)
* Add more backends
* Change this to a instalable python package and make it available on pypi
* Make it compatible with other platforms (OS X, Windows)
* Improve terminator code to use tempfile instead of creating a profile inside terminator

## Migrate from csshnator
If you are a previous csshnator user, you can migrate your old configuration with `migrate_settings_from_csshnator.py` script, just run it to get your cluster settings migrated

## Usage
To use it, just pass all hostnames as arguments on command line, like that:
```bash
csshy -l user host1 host2 host3
```

You can also create a config file with all the clusters listed in a json format, and also adjust your default terminal:
$HOME/.csshy.conf

```json
{
  "terminal": "guess",
  "cluster_nodes": {
      "cluster1": [
           "10.10.100.209",
           "10.10.100.210",
           "10.10.100.211"
      ],
      "cluster2": [
           "10.10.100.212",
           "10.10.100.213",
           "10.10.100.214"
      ]
  }
}

```
In `terminal` you can choose between `guess`, `terminator`, `tilix` and `cssh`. When you choose `guess` csshy will try it best to guess wich terminal to use.

To use the cluster you created just pass the `-c` argument

```bash
csshy -l <user> -c <clustername>
```

example:
```bash
csshy -l thor27 -c cluster1
```

For more usage information you can consult the help:

```
./csshy --help

usage: csshy.py [-h] [-l LOGIN] [-s] [-c CLUSTER_NAME] [-t TERMINAL]
                [cluster_nodes [cluster_nodes ...]]

Open ClusterSSH-like session on Terminator or Tilix

positional arguments:
  cluster_nodes         Hostnames or user@hostname to connect to, separated by
                        space

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN, --login LOGIN
                        Login username to pass to all hosts used.
  -s, --show            Show all clusters available.
  -c CLUSTER_NAME, --cluster-name CLUSTER_NAME
                        Cluster name is a collection of hosts available on
                        ~/.csshy.conf file
  -t TERMINAL, --terminal TERMINAL
                        Choose terminal to use (tilix, terminator, cssh)
```
