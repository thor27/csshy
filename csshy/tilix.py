from .utils import compute_geometry, get_start_script
from tempfile import mkstemp
import json
import subprocess
import os


def generate_tree(content_array, dimension, next_dimension=None):
    if len(content_array) == 1:
        return content_array.pop()

    childs = {}
    if next_dimension and len(content_array) > 2:
        childs.update({
            "orientation": 1,
            "position": 50,
            "ratio": 1/dimension,
            "type": "Paned"
        })
        sub_child = lambda: generate_tree(content_array, next_dimension)
    else:
        childs.update({
            "orientation": 0,
            "position": 50,
            "ratio": 1/dimension,
            "type": "Paned"
        })
        sub_child = lambda: content_array.pop()

    childs['child1'] = sub_child()

    if dimension == 2:
        childs['child2'] = sub_child()
    elif dimension > 2:
        childs['child2'] = generate_tree(content_array, dimension-1, next_dimension)

    return childs


def tilix_backend(login, cluster_nodes, cluster_name):
    width, height = compute_geometry(cluster_nodes)
    nodes = []
    for node in cluster_nodes:
        command = get_start_script(login, node)
        nodes.append({
            "directory": "\/",
            "overrideCommand":  "/bin/sh -c \"{}\"".format(command),
            "profile": "",
            "readOnly": False,
            "synchronizedInput": True,
            "type": "Terminal",
            "uuid": "",
        })

    config = {
        "child": generate_tree(nodes, width, height),
        "name": "CSSHy",
        "synchronizedInput": True,
        "type": "Session",
        "uuid": "",
        "version": "1.0",
    }

    _, filename = mkstemp()
    try:
        with open(filename, 'w') as f:
            json.dump(config, f)
        process = subprocess.Popen(["tilix", "-s", f.name])
        process.wait()
    finally:
        os.unlink(filename)
    return process.returncode == 0
