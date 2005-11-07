#!/usr/bin/python
'''
IRC Bot to record conversations in "#trailblazer" on "irc.freenode.net"
to http://blazeofglory.org/wiki as HTML pages
will probably be controlled by a CGI script and placed in the /wiki/ directory
---todo---
* add more event handlers
'''

from testbot import *
import string, time, os
from cgi import escape

class variables:

    # constants
    channel = '#trailblazer'
    nickname = 'BlazeBot'
    server = 'irc.freenode.net'

    # other variables
    admins = ['mcferrill', 'maia', 'nathortheri']
    logging = False
    blocklist = []
    log = ''

def make_log(s):
    '''
    function to parse logs into HTML, post them, and modify the log index
    accordingly
    '''
    title=time.strftime('%A, %B %d %Y', time.gmtime(time.time()))

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
href="./@info/%s">stats</a>)</div>

<h1>%s</h1>
<div class="content">''' % (title, title, title)

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
    if os.path.exists(fn+'.html'):
        num = 1
        while os.path.exists(fn+'.html'):
            num += 1
            prev = fn
            fn = 'file'+str(num)

    # see if we have a log entry for this already
    description = '<p><a href="./%s">%s</a></p>' % (fn, title)
    index = open('IRCIntoLog.html').read()
    if index.count(title):
        fn = prev

    else:
        # add entry to log index (IRCIntoLog on the site)
        index = '\n'.join([index[:index.rfind('</p>')+4], description,
                           index[index.rfind('</p>')+4:]])
        open('IRCIntoLog.html', 'w').write(index)
        
    # write finished HTML to file
    open(fn+'.html', 'w').write(html)

def stat():
    return '\n'.join([
        'Admins: '+', '.join(variables.admins),
        'Logging: '+str(variables.logging),
        'Blocked: '+', '.join(variables.blocklist)
        ])+'\n'

def command(cmd):
    '''
    commands function for control via IRC
    '''
    cmd = cmd[len('BOT: '):].split()
    if cmd[0] == 'admin':
        if not cmd[1] in variables.admins:
            variables.admins.append(cmd[1])
    elif cmd[0] == 'start':
        variables.logging = True
    elif cmd[0] == 'stop':
        variables.logging = False
    elif cmd[0] == 'ban':
        if cmd[1] in variables.admins:
            variables.admins.remove(cmd[1])
    elif cmd[0] == 'block':
        if cmd[1] not in variables.blocklist:
            variables.blocklist.append(cmd[1])
    elif cmd[0] == 'allow':
        if cmd[1] in variables.blocklist:
            variables.blocklist.remove(cmd[1])
    elif cmd[0] == 'post':
        make_log(variables.log)
    elif cmd[0] == 'reset':
        variables.log = ''
        
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
        * check to see if we should stop
        * if stop then post log and quit
        * if continue then add time, username, and message to log
        --todo--
        * more controls (see top of page)
          * --admin--
            * ban
            * admin
            * start
            * stop
            * post
            * disconnect
            * block
            * reset
          * -?-user-?-
        '''
        msg = e.arguments()[0]
        nick = nm_to_n(e.source())
        if msg == 'BOT: disconnect':
            if variables.log <> '': make_log(variables.log)
            self.die()
        elif msg[:5] == 'BOT: ' and nick in variables.admins:
            command(msg)
        else:
            if variables.logging:
                if nick not in variables.blocklist:
                    t = time.gmtime(time.time())
                    variables.log += '%s <%s> %s\n' % (time.strftime('[%H:%M]', t), nick, msg)
        return

if __name__=='__main__':
    bot = BlazeBot(variables.channel, variables.nickname, variables.server)
    bot.start()


