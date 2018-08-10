from .utils import compute_geometry, get_start_script, get_screen_size
from configobj import ConfigObj
from shutil import copyfile
import subprocess
import os


def terminator_backend(login, cluster_nodes, cluster_name):
    home = os.path.expanduser("~")
    width, height = get_screen_size()
    config_path = home + "/.config/terminator/config_csshnator"
    copyfile(home + "/.config/terminator/config", config_path)
    terminator_config = ConfigObj(config_path)
    ncols, nrows = compute_geometry(cluster_nodes)
    nnodes = len(cluster_nodes)

    vpane_name = "vpane"
    hpane_name = "hpane"
    term_name = "term"
    window_name = "window"

    cssh_layout = {
        window_name + "0": {
            "type": "Window",
            "parent": "",
        }
    }

    # VPaned/ Horizontal splits
    paneparent = window_name + "0"
    for vpane in range(0, nrows - 1):
        panepos = height/nrows  # not used as far as I can tell
        paneratio = float(1.0/(nrows - vpane))  # 1/n ... 1/3,1/2
        panename = vpane_name + str(vpane)
        cssh_layout[panename] = {
                "type": "VPaned",
                "order": min(vpane, 1),  # first pane order 0, all others order 1
                "position": panepos,
                "ratio": paneratio,
                "parent": paneparent,
                }
        paneparent = panename

    # HPaned / Veritcal Split
    for row in range(0, nrows):
        # First split, parent is VPaned
        order = 0
        paneparent = vpane_name + str(row)
        if (row == (nrows - 1)):  # last row order is 1 last row parent is second to last
            order = 1
            paneparent = vpane_name + str(row - 1)
        panepos = width/ncols
        paneratio = float(1.0/(ncols))
        panename = hpane_name + str(row) + str(0)  # hpaned00 ~ hpanedn0
        cssh_layout[panename] = {
            "type": "HPaned",
            "position": panepos,
            "ratio": paneratio,
            "order": order,
            "parent": paneparent,
        }
        # Other panes parent is previous pane
        paneparent = panename
        for hpane in range(1, ncols - 1):
            panepos = width/ncols
            paneratio = float(1.0/(ncols - hpane))
            panename = hpane_name + str(row) + str(hpane)  # hpaned00 ~ hpanednn
            cssh_layout[panename] = {
                "type": "HPaned",
                "position": panepos,
                "ratio": paneratio,
                "order": 1,
                "parent": paneparent,
            }
            paneparent = panename

    # Child terminals parents are Hpanes
    node_ind = 0
    for row in range(0, nrows):
        for col in range(0, ncols):
            if (node_ind >= nnodes):
                command = "exit"  # exit the terminal if there is no node for this
            else:
                node = cluster_nodes[node_ind]  # get the node for this terminal
                node_ind += 1
                command = get_start_script(login, node)
                # command = "echo " + login + "@" + node  + " && bash "#for debugging

            order = 0
            termparent = hpane_name + str(row) + str(col)  # parent is hpane
            if (col == (ncols - 1)):  # last col order 1 and col-1 parent
                order = 1
                termparent = hpane_name + str(row) + str(col - 1)

            term = term_name + str(row) + str(col)
            cssh_layout[term] = {
                "command": command,
                "profile": "default",
                "type": "Terminal",
                "order": order,
                "parent": termparent,
            }

    # Write to config and launch terminator
    configname = "cssh_config_" + cluster_name
    terminator_config["layouts"][configname] = cssh_layout
    terminator_config["global_config"]["broadcast_default"] = "all"
    terminator_config.write()
    process = subprocess.Popen(
        [
            "terminator",
            "-u",
            "-g", config_path,
            "-l", configname,
            "--title", "CSSHY - {}".format(cluster_name)
        ]
    )
    process.wait()
    return process.returncode == 0
