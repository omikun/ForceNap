# MyAppNap
Suspend any apps when not in focus. Prints each app name in focus. On exit (ctrl-c), app will resume as normal.

Usage:

Start desired app, then run script with:
python myAppNap.py [app name]
Ex. python myAppNap.py Unity

If no argument is given, defaults to Unity

Tested in Mac OS Sierra

TODO:
Disallow suspending parent app (eg Terminal, if launched from Terminal)
Wait until desired app is started before suspend (longer wait cycle? 5, 10s?)
