# MyAppNap
Suspend any one app when not in focus. Prints each app name in focus. On exit (ctrl-c), app will resume as normal.

## Usage:

Start desired app, then run script with:
python myAppNap.py [app name]
Ex. *python myAppNap.py Unity*

If no argument is given, will monitor apps in focus

Tested in Mac OS Sierra

## TODO:

    Disallow suspending parent app (eg Terminal, if launched from Terminal)
    DONE - do nothing if invalid name given
