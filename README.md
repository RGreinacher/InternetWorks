InternetWorks (Python 2 / OS X)
===============================

A system tray icon indicates the Internet online &amp; offline status
for Mac OS X.

This script starts a GET request to `http://74.125.224.72/` every 2.5 seconds. It is using a static IP address of Google to make sure a DNS server doesn't fool you about you internet connection.

## Get it running

### Requirements

This script requires three non standard packages. You can install them using
*pip* and *brew*:

- Python Qt4 (`brew install pyqt`)
- requests (`pip install requests`)
- argparse (`pip install argparse`)
- daemonize (`pip install daemonize`)

### Start it

To start the application, simply call:

`python InternetWorks.py`

It also comes with a daemon mode to run it as a background service:

`python InternetWorks.py -d`

***


## Contribution & Contributors

I'd love to see your ideas for improving this project!
The best way to contribute is by submitting a pull request or a new Github issue. :octocat:

## Apart of the code

Thank you for reading this and for your interest in my work. I hope I could help you or even make your day a little better. Cheers!
