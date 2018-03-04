# MyAppNap
Suspend any one app when not in focus. Prints each app name in focus. On exit (ctrl-c), app will resume as normal.

## Usage:

Start desired app, then run script with:
python myAppNap.py [app name]
Ex. *python myAppNap.py Unity*

If no argument is given, will monitor apps in focus

Tested in Mac OS Sierra

## TODO:

    Done - Disallow suspending Terminal (useful if you're launching from Terminal)
    DONE - do nothing if invalid name given
    Integrate with rumps so this can be accessed from the status bar instead of terminal
    Select multiple apps to nap at the same time
