from shutil import rmtree
from pathlib import Path
from shutil import move
from comFuncs import echo_msg, get_abs_path
import argparse
import sys
import re
import os
import pandas as pd

def cvt_class2df(x, exc="^__", condition=False):
    var = []
    val = []
    for k, v in x.__dict__.items():
        if re.search(exc, k) and condition:
            continue
        var.append(k)
        val.append(v)
    df = pd.DataFrame({"variable": var, "value": val})
    return df


def echo_msg(prg, step, msg, lvl=0, fn=None):
    fmt = "%s: %.1f - %s\n"
    f1 = "<h2>%s</h2>"
    f2 = '<font color="%s">%s</font>'
    g_lvl = os.getenv("g_lvl")  # message level
    d_lvl = os.getenv("d_lvl")  # debug level
    logfn = os.getenv("log_fn")  # log file name
    wrt2log = os.getenv("write2log")
    query_str = os.getenv("QUERY_STRING")
    http_host = os.getenv("HTTP_HOST")
    is_web = bool(query_str and http_host)

    g_lvl = int(g_lvl) if g_lvl else 1
    d_lvl = int(d_lvl) if d_lvl else 1
    ofn = fn if fn else logfn
    if not msg:
        return

    # hide passwords
    msg = re.sub(r"(\w+)/(\w+)@(\w+)", r"\1/***@\3", msg)
    msg = re.sub(r"(password:)(\w+)", r"\1/***", msg, flags=re.IGNORECASE)

    if is_web:
        if re.search(r"^\s*\d+\.\s+\w+", msg):
            print(f1 % (fmt % (prg, step, msg)))
        if re.search(r"^ERR:", msg, re.IGNORECASE):
            print(f2 % ("red", fmt % (prg, step, msg)))
        if re.search(r"^WARN:", msg, re.IGNORECASE):
            print(f2 % ("orange", fmt % (prg, step, msg)))
        if re.search(r"^INFO:", msg, re.IGNORECASE):
            print(f2 % ("cyan", fmt % (prg, step, msg)))
        if re.search(r"^CMD:", msg, re.IGNORECASE):
            print(f2 % ("blue", fmt % (prg, step, msg)))
        if re.search(r"^\s*\d+\.\s+\w+:", msg):
            print("<br>")

    if lvl <= int(d_lvl) or lvl <= int(g_lvl):
        print(fmt % (prg, step, msg))
        if ofn and wrt2log:
            with open(ofn, "a") as f:
                f.write(fmt % (prg, step, msg))
                f.write("\n")


def get_abs_path(dir, relpath):
    abs_path = os.path.abspath(os.path.join(dir, relpath))
    if not os.path.exists(abs_path):
        return None
    abs_path = os.path.normpath(abs_path)
    dir = os.path.normpath(dir)
    if os.name == "nt":
        dir = dir.rstrip("/")
    if len(abs_path) <= len(dir) + 1:
        return None
    if abs_path[:len(dir)] != dir or abs_path[len(dir):len(dir) + 1] != "/":
        return None
    return abs_path


def is_empty(x):
    if x is None or x is float('nan') or x is '' or x == []:
        return True
    if isinstance(x, str) and x.isspace():
        return True
    return False


def start_app(app_name="showenv", n=1, pkg="comFuncs", pt=None, lb=None, ht="127.0.0.1", dm="normal", msg_lvl=None, loc='local'):
    prg = "start_app"
    echo_msg(prg, 0.0, 'Started', 1)
    if not loc == 'local':
        raise ValueError(
            "Unsupported location: {}. Only local location is supported.".format(loc))
    if not pkg in sys.modules:
        try:
            __import__(pkg)
        except ModuleNotFoundError:
            raise ValueError("Could not load package {}".format(pkg))
    if msg_lvl is None:
        os.environ["g_lvl"] = "0"
        os.environ["d_lvl"] = "0"
    else:
        os.environ["g_lvl"] = str(msg_lvl)
        os.environ["d_lvl"] = str(msg_lvl)
    echo_msg(prg, 0.1, "app_name = {}, n = {}, pkg = {}".format(
        app_name, n, pkg), 1)
    pks = {"genTS": "apps", "phuse": "examples",
           "podr": "apps", "orabkup": "apps", "comFuncs": "apps"}
    adr = pks.get(pkg, "apps")
    echo_msg(prg, 0.2, "adr = {}".format(adr), 1)
    appDir = os.path.join(os.path.dirname(__file__), adr)
    apps = os.listdir(appDir)
    app = apps[n-1] if app_name == "showenv" else app_name
    echo_msg(prg, 0.3, "appDir = {}, app = {}".format(appDir, app), 1)
    appPath = get_abs_path(appDir, app)
    echo_msg(prg, 0.4, "Resolved dir = {}".format(appPath), 1)
    if appPath is None:
        msg = "could not find a dir for {}".format(app)
        echo_msg(prg, 1.1, msg, 1)
        validApps = "\", \"".join(apps)
        raise ValueError("{} Valid apps are \"{}\"".format(msg, validApps))
    else:
        msg = "Start app from {}".format(appPath)
        echo_msg(prg, 1.2, msg, 1)
        shinyArgs = dict(port=pt, host=ht, launch_browser=lb, display_mode=dm)
        shiny: :runApp(appPath, **shinyArgs)


def format_number(self, n, t=None):
    # n - number
    # t - type: size or time

    if n == "":
        return ""

    t = 'size' if not t else t
    r, s = "", 0
    kb = 1024
    mb = 1024 * kb
    gb = 1024 * mb
    tb = 1024 * gb
    pb = 1024 * tb
    mi = 60
    hh = 60 * mi
    dd = 24 * hh

    if t.lower().startswith("s"):
        if n > pb:
            return f"{n / pb:.3f}PB"
        elif n > tb:
            return f"{n / tb:.3f}TB"
        elif n > gb:
            return f"{n / gb:.3f}GB"
        elif n > mb:
            return f"{n / mb:.3f}MB"
        elif n > kb:
            return f"{n / kb:.3f}KB"
        else:
            return f"{n} Bytes"
    else:
        s = abs(n)
        if s > dd:
            r = f"{s // dd}D"
            s = s % dd

        if s > hh:
            r += f"{s // hh:02}:"
            s = s % hh

        if s > mi:
            r += f"{s // mi:02}:"
            s = s % mi

        r += f"{s:02}"
        r = f"-{r}" if n < 0 else r

    return r


def cp_file(s, ifn, ofn, afn, fh_log):
    msg = ""
    if not os.path.isfile(ofn):
        s.mv_file(ifn, ofn, "NEW", fh_log)
        return

    a = os.stat(ifn)
    b = os.stat(ofn)
    if (a.st_size == b.st_size) and (a.st_mtime == b.st_mtime):
        os.unlink(ifn)
        msg = "  INFO: found with the same size and time in the target dir and\n"
        msg += f"        deleted source - {ifn}."
        s.echo_msg(msg, 0, fh_log)
    else:
        if os.path.isfile(afn):
            os.unlink(ifn)
            msg = f"  INFO: skipped cp and deleted source - {ifn}."
            s.echo_msg(msg, 0, fh_log)
        else:
            adr = os.path.dirname(afn)
            if not os.path.isdir(adr):
                s.mk_dir(adr, fh_log)
            s.mv_file(ifn, afn, "moved2", fh_log)


def mv_file(s, f1, f2, msg, fh):
    msg = f"  INFO: {msg} {f1} to {f2}."
    try:
        move(f1, f2)
    except Exception as e:
        msg = f"  ERR: move {f1} to {f2} failed: {e}"
    s.echo_msg(msg, 0, fh)
    if os.path.isfile(f1) and os.path.isfile(f2):
        os.unlink(f1)
    return


def mk_dir(s, dir, fh):
    msg = f"INFO: dir - {dir} exists."
    if os.path.isdir(dir):
        s.echo_msg(msg, 1, fh)
        return
    try:
        Path(dir).mkdir(parents=True)
    except Exception as e:
        msg = f"  ERR: could not mkdir - {dir}: {e}"
    else:
        msg = f"  INFO: ({os.strerror(os.errno.ENOENT)}) target dir - {dir} is created."
        if sys.platform != "win32":
            os.chmod(dir, 0o777)
    s.echo_msg(msg, 1, fh)
    if msg.startswith("  ERR:"):
        raise Exception(msg)
