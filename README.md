
# Requirements

* Python 2 or 3 (tested with v2.7.6 and v3.4.0)
* PyQt4 (tested with v4.10.4)
* pytz (tested with v2014.10)
* simplejson (optional; tested with v3.6.5)


# Usage

## With GUI

    python ./main.py

## Without GUI

    # stats preview
    python ./backend.py filename.dlog

or:

    # adding task/event + stats preview
    python ./backend.py filename.dlog "Task nr N"


# TBD

* buttons - no log but real actions

* minimize to tray

    * http://stackoverflow.com/a/758352

    * http://pyqt.sourceforge.net/Docs/PyQt4/qsystemtrayicon.html

