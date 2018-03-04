# NapMyApp
Suspend any one or more apps when not in focus and resumes each app only when they come into focus.
This script runs every .5 second, but otherwise should introduce no additional lag. 
Suspend only stops the app from using CPU, so it is stopped but keeps its data in memory.
Prints each app name in focus. On exit (ctrl-c), app will resume as normal.

This differs from App Nap which throttles and potentially stops apps, but only if they are supported.

## Usage:

Start desired app, then run script with one or more app names:
python NapMyApp.py [app name, ...]
For example, so suspend Unity and Safari:
*python NapMyApp.py Unity Safari*

If no argument is given, all defocused apps (apps that get focus then lose it) are automatically suspended.

On exit, all suspended apps will be resumed.

Tested in Mac OS Sierra

## TODO:

    Done - Disallow suspending Terminal (useful if you're launching from Terminal)
    DONE - do nothing if invalid name given
    Integrate with rumps so this can be accessed from the status bar instead of terminal
    Select multiple apps to nap at the same time
