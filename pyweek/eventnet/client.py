import eventnet.driver
import eventnet.net
import time


def connect(p):
    print 'Connected. Sending PING event'
    p.post('PING',count=1)

def close(conn):
    print "Lost Conneciton."


@eventnet.driver.handle('PONG')
def pong(event):
    print 'PONG', event.count
    print 'PING... ',
    event.reply('PING', count=event.count)

eventnet.net.connect('127.0.0.1', 2080, connect, close)

while True:
    time.sleep(0.1)
    eventnet.net.poll()


