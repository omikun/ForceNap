# ForceNap
Suspend any one or more apps when not in focus and resumes each app only when they come into focus.
This script runs every .5 second, but otherwise should introduce no additional lag. 
Suspend only stops the app from using CPU, so it is stopped but keeps its data in memory.
Prints each app name in focus. On exit (ctrl-c), app will resume as normal.

This differs from App Nap which throttles and potentially stops apps, but only if they are supported.

## Usage:
Download the pre-release [ForceNap](https://github.com/omikun/MyAppNap/releases), open and select the application(s) to force nap in the status bar (look for FN). ForceNap must be started after target applications have been started. This is not a stable product yet, so please do not use on 

## Compile 
You can also compile your own using [rumps](https://github.com/jaredks/rumps/blob/master/rumps/rumps.py) and py2app.

### Deprecated:
Start desired app, then run script with one or more app names as arguments:`python nap_my_app.py app_name(s)`

For example, to suspend Unity and Safari:
`python nap_my_app.py Unity Safari`

If no argument is given, all defocused apps (apps that get focus then lose it) are automatically suspended.

On exit, all suspended apps will be resumed.

Tested in Mac OS Sierra

## TODO:

    Done - Disallow suspending Terminal (useful if you're launching from Terminal)
    DONE - do nothing if invalid name given
    DONE - Integrate with rumps so this can be accessed from the status bar instead of terminal
    DONE - Select multiple apps to nap at the same time
    Refactor code
    Dynamically update menu
