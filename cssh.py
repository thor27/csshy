import subprocess


def cssh_backend(login, cluster_nodes, cluster_name):
    args = ["cssh"]
    args += ["{}@{}".format(login, node) for node in cluster_nodes]
    subprocess.Popen(args)
