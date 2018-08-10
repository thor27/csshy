import subprocess
import os
from .tilix import tilix_backend
from .terminator import terminator_backend
from .cssh import cssh_backend


# Terminals, by order of preference
terminal_names = (
    ("tilix", tilix_backend),
    ("terminator", terminator_backend),
    ("cssh", cssh_backend)
)


def execute(*args):
    exec = subprocess.Popen(args, stdout=subprocess.PIPE)
    exec.wait()
    return exec


def guess_from_text(text):
    for name, backend in terminal_names:
        if name in text.lower():
            return backend


def guess_default_terminal():
    active_desktop = os.environ.get("XDG_CURRENT_DESKTOP").lower()

    # Guess when running gnome
    if "gnome" in active_desktop or "unity" in active_desktop:
        exec = execute("gsettings", "get", "org.gnome.desktop.default-applications.terminal", "exec")
        guess = guess_from_text(exec.stdout.read().decode('utf-8'))
        if guess:
            return guess

    # TODO Guessing in other DEs

    # Guess default terminal set on system (Debian like only)
    exec = execute("update-alternatives", "--query", "x-terminal-emulator")
    if exec.returncode == 0:
        for line in exec.stdout:
            if line.startswith(b"Value:"):
                guess = guess_from_text(line.decode('utf-8'))
                if guess:
                    return guess
                break

    # Guess based on my personal preference
    for name, backend in terminal_names:
        if execute("which", name).returncode == 0:
            return backend

    # there is nothing to do now...
    return None


def get_backend(cssh_config, terminal_name=""):
    if not terminal_name:
        terminal_name = cssh_config["terminal"]

    if terminal_name == 'guess':
        return guess_default_terminal()

    return dict(terminal_names).get(terminal_name)
