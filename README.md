checkreg - mobile check registry
================================

<span>![checkreg screenshot1](http://deanproxy.com/static/images/checkreg/1.png "Home Screen")</span>
<span>![checkreg screenshot2](http://deanproxy.com/static/images/checkreg/2.png "Expenses Screen")</span>
<span>![checkreg screenshot3](http://deanproxy.com/static/images/checkreg/3.png "Add Screen")</span>

This was a simple app created by me to track purchases between my wife and I
before they hit our bank account.  It gives us a way to enter a purchase
immediately after it was done so that the other person could see how much 
was *really* available in the checking account before making a big purchase
of their own.

Sometimes living paycheck to paycheck makes you do funny things...

Install
-------

This is a Django application. So, install with WSGI on Apache or nginx.  Make sure to set a
reroute for the /static/ directory so that all static files are not served by the WSGI module.

You'll also need to set up a database and run syncdb and edit settings.py with your settings.
I'll get around to making this more friendly at some point...  Just write me if you need help.
