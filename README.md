# ForceNap
- Force one or more apps to stop when not in focus and resumes each app when they regain focus.
- This script runs every 0.5 second, but otherwise should introduce no additional lag. 
- Apps that are ForceNapped cannot be interacted with in the background (scroll with another app in focus).
- You may see spinning beachball over ForceNapped apps and they will show as "Not responding" in Activity Monitor. Click on the app or alt-tab back to it to resume the app.
- Suspend only stops the app from using CPU but keeps data in memory.

This differs from App Nap which throttles and potentially stops apps, but only if they are supported.

## Usage:
- Download the pre-release [ForceNap](https://github.com/omikun/MyAppNap/releases)
- Open and select the application(s) to force nap in the status bar (look for FN). 
- ForceNap must be started after target applications have been started. 
- This is not a stable product yet. 
- Not suited for mission critical applications.

![Screen shot](/ForceNap_screen_shot.png)
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

    - Done - Disallow suspending Terminal (useful if you're launching from Terminal)
    - DONE - do nothing if invalid name given
    - DONE - Integrate with rumps so this can be accessed from the status bar instead of terminal
    - DONE - Select multiple apps to nap at the same time
    - Refactor code
    - Dynamically update menu
