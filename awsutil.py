
""" Utility code for invoking AWS CLI commands from scripts.

    Hugh Fisher, Canberra Australia, Nov 2026
    Released under MIT license.
"""

import json, subprocess, sys, time

def run(*subcommand):
    """Run aws with subcommand and options, return output or raise exception"""
    cli = ["aws"]
    cli.extend(subcommand)
    print("> " + " ".join(cli))
    cp = subprocess.run(cli, capture_output=True)
    try:
        cp.check_returncode()
    except (subprocess.CalledProcessError,) as e:
        # Convenience for caller
        print(e.stderr.decode('utf-8', 'backslashreplace'), file=sys.stderr)
        raise
    return cp.stdout.decode('utf-8', 'backslashreplace')

def whoAmI():
    """Return dict with user, region"""
    result = {}
    out = json.loads(run("sts", "get-caller-identity"))
    result["user"] = out["Arn"]
    out = run("configure", "list")
    for line in out.splitlines():
        fields = [s.strip() for s in line.split(':')]
        for k in ("profile", "region"):
            if fields[0] == k:
                result[k] = fields[1]
    return result

def allowCancel(prompt="Execute in", wait=5):
    """Give me time to change my mind and Ctrl-C"""
    print(prompt, end="", flush=True)
    while wait > 0:
        print(" {}".format(wait), end="", flush=True)
        time.sleep(1)
        wait -= 1
    print()


##  Utilities for startup

def confirmCLI():
    """Check that we have CLI"""
    out = run("--version")
    print(out.split(' ')[0])

def confirmID():
    """Initial check that logged in"""
    out = run("sts", "get-caller-identity")
    user = json.loads(out)
    print("Run as", user["Arn"])

config = {}

def start():
    """My common code"""
    global config
    #
    confirmCLI()
    confirmID()
    config = whoAmI()
