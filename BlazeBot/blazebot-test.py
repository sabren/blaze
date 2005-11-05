#!/usr/bin/python
'''
IRC Bot to record conversations in "#trailblazer" on "irc.freenode.net"
to http://blazeofglory.org/wiki as HTML pages
will probably be controlled by a CGI script and placed in the /wiki/ directory
---todo---
* add more event handlers

--test variation for use on local machines
'''

from testbot import *
import string, time, os
from cgi import escape

class variables:

    # constants
    channel = '#trailblazer'
    nickname = 'BlazeBot-test'
    server = 'irc.freenode.net'

    # other variables
    admins = ['mcferrill', 'maia', 'nathortheri']
    logging = True
    blocklist = []
    log = ''

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

    # write to "temp.html" for testing
    fn = 'temp.html'
    
    # write finished HTML to file
    open(fn, 'w').write(html)

    # put link in logindex (IRCIntoLog on the site)
    description = '<p><a href="./%s">%s</a></p>' % (fn, title)
    index = open('logindex.html').read()
    index = '\n'.join([index[:index.rfind('</p>')+4], description,
                       index[index.rfind('</p>')+4:]])
    open('logindex.html', 'w').write(index)

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
        os.startfile('logindex.html')
    elif cmd[0] == 'reset':
        variables.log = ''
    elif cmd[0] == 'stat':
        print stat()
    else:
        print 'no such command!'

class BlazeBot(TestBot):
    '''
    the bot object for the program
    '''
    def __init__(self, channel, nickname, server, port=6667):
        TestBot.__init__(self, channel, nickname, server, port)
        self.channel = variables.channel
        variables.log = ''

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
            make_log(variables.log)
            os.startfile('logindex.html')
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


