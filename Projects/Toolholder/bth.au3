#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.1
 Author:         myName

 Script Function:
	Template AutoIt script.

#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here

Run("control bthprops.cpl", "C:/Windows/System32")
WinWait("Settings")
WinMove("Settings", "", 0, 0)
MouseClick("left", 380, 150)
Sleep(5000)
MouseClick("left", 380, 150)
WinClose("Settings")