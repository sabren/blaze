src = 'logfile.txt'
file = open(src, 'r')
list = file.readlines()
file.close()
txt = ''
for x in list:
    txt += x+'\n'
file = open(src, 'w')
file.write(txt)
file.close()
