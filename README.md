# xabbo.py

## Features
* Anti-idle: Prevents idling after 5 minutes of doing nothing.
* Anti-typing bubble: Prevents showing the speech bubble when typing.
* Anti-bobba: yes.
* Anti-look: Prevents turning when clicking on other users.
* Turn commands: Allows turning in any direction without clicking on another user. North is in the diagonal up-right direction on the screen.
* Moodlight commands: Toggle the moodlight or open settings with a command.

## How to use
### Windows
Open `run.bat` and enter the G-Earth extension port, or just press enter to use the default port.

## Commands
* `/idle` Toggle anti-idle
* `/type` Toggle anti-typing bubble
* `/bobba` Toggle anti-bobba
* `/bobba [off|local|full]`
  * `off` - Disabled
  * `local` - Localized (only applied to text between square brackets `[]`)
  * `full` - Applied to full text
* `/look` - Toggle anti-look (don't turn when clicking users)
* `/turn [n|ne|e|se|s|sw|w|nw]` - Turn to face the specified direction
* `/mood` - Toggle the moodlight
* `/mood settings` - Open the moodlight settings
