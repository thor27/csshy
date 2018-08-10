import math


def compute_geometry(nodes):
    nnodes = len(nodes)
    nrows = round(math.sqrt(nnodes))
    ncols = math.ceil(nnodes/nrows)
    nrows = int(nrows)
    ncols = int(ncols)
    nrows = max(nrows, 2)  # atlease 2 rows to make geometry easier
    ncols = max(ncols, 2)  # atlease 2 columns to make geometry easier
    return ncols, nrows


def get_start_script(login, node):
    command = "echo CSSHY started &&"
    command += "echo connecting to " + login + ("@" if login else "") + node + " &&"  # ssh command
    command += "ssh " + login + ("@" if login else "") + node  # ssh command
    return command
