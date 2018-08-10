import subprocess


def cssh_backend(login, cluster_nodes, cluster_name):
    args = ["cssh"]
    args += ["{}@{}".format(login, node) for node in cluster_nodes]
    process = subprocess.Popen(args)
    process.wait()
    return process.returncode == 0
