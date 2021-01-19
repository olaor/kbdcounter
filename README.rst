kdbcounter - a program for counting keyboard activity
-----------------------------------------------------

This program will count the number of keypresses you make on your
keyboard and mouse, on any X Window System environment, for example
Linux. 

The results, divided by hour, are stored in a commaseparated file, by
default ~/.kbdcounter.csv. For hours where there's no activity, no
line is added to the file. 

It will also mute you microphones on the first registered keyboard
click , then unmute after 0.75 seconds of keyboard inactivity. Very
handy when attending Teams, Zoom, appear.in or other online meetings.


Installation
------------

Install the *python-xlib* package via apt, yum, pip or whatever means necessary.

Run *src/kbdcounter.py*. After 5 minutes, verify that it's working by
inspecting ~/.kbdcounter.csv.

The program should be started automatically when your desktop session
is started. 

Is this a silly program?
------------------------

Yes. I wrote it because I was curious on how many keystrokes I was
making on a regular working day.

And no. After adding the mute functionality it is very useful during
meetings.

The original author did a damn fine job making this program, silly or not.

Known bugs
----------

* The program will not save the last 5 minutes of stats if it's
  killed. Killing it with Ctrl-C will however save state.

   



