README for BlazeBot.py
----------------------

The bot is started on the server through an
undisclosed URL that triggers a new "BlazeBot.py"
process. This almost instantly connects to the IRC
server and channel then to be controlled through
"admins" on IRC using the following commands:

BOT: admin *nickname* <-- add *nickname* to controllers list
BOT: ban *nickname*   <-- remove *nickname* from controllers
BOT: start            <-- start recording a log
BOT: stop             <-- stop recording the log (doubles as "pause")
BOT: post             <-- post current log to the website
BOT: reset            <-- reset the log to an empty string
BOT: disconnect       <-- post current log and terminate program

TODO
----
* Add more event handlers
    * "AWAY"
    * "ME" ???
    * etc.
