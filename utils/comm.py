# Purpose: A Module Containing Common Utilities 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - initial coding
#   03/15/2023 (htu) - tested out: 
#

from shutil import rmtree
from pathlib import Path
from shutil import move
# import argparse
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
    g_lvl = os.getenv("g_lvl")      # message level
    d_lvl = os.getenv("d_lvl")      # debug level
    logfn = os.getenv("log_fn")     # log file name
    wrt2log = os.getenv("write2log")
    query_str = os.getenv("QUERY_STRING")
    http_host = os.getenv("HTTP_HOST")
    is_web = bool(query_str and http_host)

    g_lvl = int(g_lvl) if g_lvl else 1
    d_lvl = int(d_lvl) if d_lvl else 1
    ofn = fn if fn else logfn
    if not msg or msg is None:
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



def format_number(n, t=None):
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
