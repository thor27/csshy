#!/usr/bin/env python
import sys
import argparse
import os
import json
from .backends import get_backend

SUCCESS, FAIL = 0, 1


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Open ClusterSSH-like session on Terminator or Tilix'
    )

    parser.add_argument(
        '-l',
        '--login',
        dest='login',
        type=str,
        default="",
        help='Login username to pass to all hosts used.'
    )

    parser.add_argument(
        '-s',
        '--show',
        dest='show',
        action='store_true',
        help='Show all clusters available.'
    )

    parser.add_argument(
        '-c',
        '--cluster-name',
        dest='cluster_name',
        type=str,
        default="tmp",
        help='Cluster name is a collection of hosts available on ~/.csshy.conf file'
    )

    parser.add_argument(
        '-t',
        '--terminal',
        dest='terminal',
        type=str,
        default="",
        help='Choose terminal to use (tilix, terminator, cssh)'
    )

    parser.add_argument(
        'cluster_nodes',
        nargs='*',
        default=None,
        help='Hostnames or user@hostname to connect to, separated by space'
    )

    return parser.parse_args(argv)


def print_servers(cluster_nodes):
    max_size = max([len(k) for k in cluster_nodes]) + 2
    formater = "{:<" + str(max_size) + "}"
    for key, value in cluster_nodes.items():
        print(formater.format(key), " ".join(value))


def get_config_filename():
    return os.path.join(
        os.path.expanduser("~"),
        ".csshy.conf"
    )


def update_config(config):
    config_file = get_config_filename()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


def load_config():
    default_settings = {
        'terminal': 'guess',
        'cluster_nodes': {}
    }

    config_file = get_config_filename()

    try:
        with open(config_file) as f:
            config = json.load(f)
    except FileNotFoundError:
        config = default_settings
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

    return config


def main():
    args = parse_args(sys.argv[1:])
    cssh_config = load_config()

    if args.show:
        print_servers(cssh_config['cluster_nodes'])
        return SUCCESS

    # width = gtk.gdk.screen_width()
    # height = gtk.gdk.screen_height()

    cluster_nodes = cssh_config['cluster_nodes'].get(args.cluster_name, args.cluster_nodes)
    if not cluster_nodes:
        print("No hosts to connect. Use --help for more info.")
        return FAIL

    backend = get_backend(cssh_config, args.terminal)

    if not backend:
        print("No valid terminal available. Please install tilix, terminator or cssh")

    result = backend(args.login, cluster_nodes, args.cluster_name)
    return SUCCESS if result else FAIL


if __name__ == "__main__":
    sys.exit(main())
