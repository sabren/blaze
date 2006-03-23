import eventnet.driver
import eventnet.net
import time

def connect(conn):
    print 'New Connection, waiting for events...'

def close(conn):
    print "Lost connection."

@eventnet.driver.handle('PING')
def ping(event):
    event.reply('PONG', count=event.count+1)
    
    

eventnet.net.listen(2080, connect, close)

while True:
    time.sleep(0.1)
    eventnet.net.poll()


