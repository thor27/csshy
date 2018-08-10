import math
TOOLKIT = None

try:
    import wx
    TOOLKIT = "wx"
except ImportError:
    pass

if not TOOLKIT:
    try:
        import tkinter as tk
        TOOLKIT = "tk"
    except ImportError:
        pass

if not TOOLKIT:
    try:
        import gtk
        TOOLKIT = "gtk"
    except ImportError:
        pass


def get_screen_size():
    w, h = 1920, 1080

    if TOOLKIT == "wx":
        app = wx.App(False)
        w, h = wx.GetDisplaySize()
        app.Destroy()
    elif TOOLKIT == "tk":
        app = tk.Tk()
        w = app.winfo_screenwidth()
        h = app.winfo_screenheight()
        app.destroy()
    elif TOOLKIT == "gtk":
        w = gtk.gdk.screen_width()
        h = gtk.gdk.screen_height()

    return w, h


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
