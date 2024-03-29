#!/usr/bin/python
'''
IRC Bot to record conversations in "#trailblazer" on "irc.freenode.net"
to http://blazeofglory.org/wiki as HTML pages
will probably be controlled by a CGI script and placed in the /wiki/ directory
see "README.txt" for more information
'''

from testbot import *
from ircbot import *
import string, time, os, sys
from cgi import escape

class variables:

    # constants
    channel = '#trailblazer'
    nickname = 'BlazeBot'
    server = 'irc.freenode.net'

    # other variables
    admins = ['mcferrill', 'maia']
    logging = True
    blocklist = []
    log = ''

def make_log(s):
    '''
    function to parse logs into HTML, post them, and modify the log index
    accordingly
    '''
    title=time.strftime('%A, %B %d %Y', time.gmtime(time.time()))

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
href="./@edit/%s" class="edit">Edit this document</a>.</address>
</body>
</html>''' % fn[:-5]
        
    # write finished HTML to file
    open(fn+'.html', 'w').write(html)

def command(cmd):
    '''
    commands function for control via IRC
    '''
    if cmd.startswith('BOT: '): cmd = cmd[len('BOT: '):].split()
    if cmd[0] == 'admin':
        if not cmd[1] in variables.admins:
            variables.admins.append(cmd[1])
    elif cmd[0] == 'start':
        variables.logging = True
    elif cmd[0] == 'stop':
        variables.logging = False
    elif cmd[0] == 'ban':
        if cmd[1] in variables.admins and cmd[1] <> 'mcferrill':
            variables.admins.remove(cmd[1])
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

    '''
    event handlers
    --------------
    '''
    def on_topic(self, c, e):
        t = time.gmtime(time.time())
        nick = nm_to_n(e.source())
        variables.log += '''%s * %s changes topic to "%s"\n''' % (time.strftime(
            '[%H:%M]', t), nick, e.arguments()[-1])

    def _on_part(self, c, e):
        t = time.gmtime(time.time())
        """[Internal]"""
        nick = nm_to_n(e.source())
        channel = e.target()

        if nick == c.get_nickname():
            del self.channels[channel]
        else:
            self.channels[channel].remove_user(nick)
        variables.log += '%s * %s has left #trailblazer %s\n' % (time.strftime(
            '[%H:%M]', t), nick, e.arguments()[0])

    def _on_join(self, c, e):
        t = time.gmtime(time.time())
        """[Internal]"""
        ch = e.target()
        nick = nm_to_n(e.source())
        if nick == c.get_nickname():
            self.channels[ch] = Channel()
        self.channels[ch].add_user(nick)
        variables.log += '%s * %s has joined #trailblazer\n' % (time.strftime(
            '[%H:%M]', t), nick)

    def _on_nick(self, c, e):
        t = time.gmtime(time.time())
        """[Internal]"""
        before = nm_to_n(e.source())
        after = e.target()
        for ch in self.channels.values():
            if ch.has_user(before):
                ch.change_nick(before, after)
        variables.log += '%s * %s is now known as %s\n' % (time.strftime(
            '[%H:%M]', t), before, after)
        
    def _on_quit(self, c, e):
        t = time.gmtime(time.time())
        """[Internal]"""
        nick = nm_to_n(e.source())
        for ch in self.channels.values():
            if ch.has_user(nick):
                ch.remove_user(nick)
        variables.log += '%s * %s has quit IRC (%s)\n' % (time.strftime('[%H:%M]',
                                                                        t),
                                                         nick, e.arguments())

    def on_privmsg(self, c, e):
        msg = e.arguments()[0]
        if msg == 'quit':
            make_log(variables.log)
            self.die()
        elif msg == 'post': make_log(variables.log)
        elif msg.split()[0] == 'admin':
            if not msg.split()[1] in variables.admins:
                variables.admins.append(cmd[1])
        elif msg.split()[0] == 'ban':
             if cmd[1] in variables.admins and cmd[1] <> 'mcferrill':
                variables.admins.remove(cmd[1])
        else:
            c.privmsg('#trailblazer', msg)
            msg = 'ok'

    def on_pubmsg(self, c, e):
        '''
        when message is posted:
        * check to see if we should stop
        * if stop then post log and quit
        * if continue then add time, username, and message to log
        '''
        msg = e.arguments()[0]
        nick = nm_to_n(e.source())
        if msg == 'BOT: disconnect' and nick in variables.admins:
            if variables.log <> '': make_log(variables.log)
            self.die()
            sys.exit(0)
        elif msg[:5] == 'BOT: ' and nick in variables.admins:
            command(msg)
        else:
            if variables.logging:
                if nick not in variables.blocklist:
                    t = time.gmtime(time.time())
                    variables.log += '%s <%s> %s\n' % (time.strftime('[%H:%M]',
                                                                     t), nick,
                                                       msg)
        return

    '''
    /event handlers
    ---------------
    '''

    def _connect(self):
        """[Internal]"""
        password = 'burn'
        #if len(self.server_list[0]) > 2:
        #    password = self.server_list[0][2]
        try:
            self.connect(self.server_list[0][0],
                         self.server_list[0][1],
                         self._nickname,
                         password,
                         ircname=self._realname)
        except ServerConnectionError:
            pass

    def start(self):
        """Start the bot."""
        self._connect()
        starttime = time.time()+600
        while 1:
            if starttime < time.time():
                make_log(variables.log)
                starttime = time.time()+600
            self.ircobj.process_once()

if __name__=='__main__':
    bot = BlazeBot(variables.channel, variables.nickname, variables.server)
    bot.start()
