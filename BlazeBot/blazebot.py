#!/usr/bin/python
'''
IRC Bot to record conversations in "#trailblazer" on "irc.freenode.net"
to http://blazeofglory.org/wiki as HTML pages
will probably be controlled by a CGI script and placed in the /wiki/ directory
---todo---
* add more event handlers
* set up on the blaze site with controls
'''

from testbot import *
import string, time, os
from cgi import escape

# constants
channel = '#trailblazer'
nickname = 'BlazeBot'
server = 'irc.freenode.net'

def make_log(s, title=time.strftime('%A, %B %d %Y', time.gmtime(time.time()))):
    '''
    function to parse logs into HTML, post them, and modify the log index
    accordingly
    '''
    
    # add HTML header
    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" >

<html xmlns="http://www.w3.org/1999/xhtml">
<head profile="http://infomesh.net/pwyky/profile#">
<title>%s</title>
<link rel="stylesheet" type="text/css" href="http://blazeofglory.org/wiki/style.css" />
</head>
<body>
<center><iframe src="http://blazeofglory.org/main/nav.html" width="900" height="100" frameborder="0" scrolling="no"></iframe></center><div class="about">(<a href="./">home</a> | <a 
href="./@meta/about">about</a> | <a 
href="./@info/file3">stats</a>)</div>

<div class="content">
<h1>%s</h1>''' % (title, title)

    # add all lines of the log as HTML paragraphs (so that we have line breaks)
    html += '\n'.join(['<p>%s</p>' % string.replace(escape(line),'}', '}}') for line in s.split('\n')])

    # add HTML footer
    html += '''
</div>

<address>BlazeOfGlory.org. This is a <a 
href="http://infomesh.net/pwyky/">pwyky</a> site. <a 
href="./@edit/file3" class="edit">Edit this document</a>.</address>
</body>
</html>'''

    # make sure we're making a new file and not overwriting an old one
    fn = 'file'
    if os.path.exists(fn):
        num = 1
        while os.path.exists(fn+'.html'):
            num += 1
            fn = 'file'+str(num)

    # write finished HTML to file
    open(fn+'.html', 'w').write(html)
    
    description = '<p><a href="./%s">%s</a></p>' % (fn, title)
    index = open('IRCIntoLog.html').read()
    index = '\n'.join([index[:index.rfind('</p>')+4], description,
                       index[index.rfind('</p>')+4:]])
    open('IRCIntoLog.html', 'w').write(index)

class BlazeBot(TestBot):
    '''
    the bot object for the program
    '''
    def __init__(self, channel, nickname, server, port=6667):
        TestBot.__init__(self, channel, nickname, server, port)
        self.channel = channel
        self.log = ''

    def on_pubmsg(self, c, e):
        '''
        when message is posted:
        * check to see if we shoudl stop
        * if stop then post log and quit
        * if continue then add time, username, and message to log
        '''
        msg = e.arguments()[0]
        nick = nm_to_n(e.source())
        if msg == 'STOPBOT' and nick == 'mcferrill':
            make_log(self.log)
            os.startfile('IRCIntoLog.html')
            self.die()
        t = time.gmtime(time.time())
        self.log += '%s <%s> %s\n' % (time.strftime('[%H:%M]', t), nick, msg)
        return

if __name__=='__main__':
    bot = BlazeBot(channel, nickname, server)
    bot.start()


