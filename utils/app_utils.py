# Purpose: A Module Containing Application Utilities
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - initial coding
#   03/15/2023 (htu) - tested out:


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
        shiny: : runApp(appPath, **shinyArgs)



