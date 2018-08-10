from csshy import update_config, load_config
from configobj import ConfigObj
import os


def load_old_config():
    home = os.path.expanduser("~")
    return ConfigObj(home + "/.csshnatorrc")


def main():
    print("Migrating cluster nodes from csshnator to csshy...")

    print("Loading config files")
    new_config = load_config()
    old_config = load_old_config()

    for cluster in old_config:
        print("Migrating", cluster)
        new_config['cluster_nodes'][cluster] = old_config[cluster].split(" ")

    print("Saving settings")
    update_config(new_config)

    print("Done")


if __name__ == '__main__':
    main()
