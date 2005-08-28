#code to convert python scripts into windows .exe files using py2exe
#requires py2exe 0.5

#import modules or warn user if not possible
try:
    import os, string, time
except:
    raw_input('ERROR: Could not import needed modules, check your python lib')
    pass

try: #system to avoid shutdown because of errors

    #get the users temp file from the os module
    temp = os.environ['TEMP']+'setup.py'

    # take needed inputs from user and test for existing files
    while 1:
        src = raw_input('SOURCE:')
        if os.path.exists(src):
            break
        else:
            print "File not found, please try again."
    while 1:
        data = raw_input('DATA-DIR:')
        if os.path.exists(data):
            break
        else:
            print "File not found, please try again."

    new = '' #change this is you have a specific place you keep your converted files
    if new == '':
        new = os.environ['HOMEPATH']+'\\EXEs'
        
    #tell if this is a windows or console program (the windows option can also be used to make a program invisible)
    mode = raw_input('Is this a console program?:')
    if string.lower(mode) <> 'yes':
        mode = 'windows'
    else:
        mode = 'console'

    #make the text for a temporary setup.py script
    text = '#setup.py \nfrom distutils.core import setup \nimport py2exe\nsetup('+mode+'="'+old+'")'

    #create a command line with all options
    cmd = temp, 'py2exe', mode, '--dist-dir', new

    #make the setup script
    file = open(temp, 'w')
    file.write(text)
    file.close()

    #and run the command line
    os.system(cmd)

    #wait a couple of seconds while the command line is running
    #I'm not sure if this is needed but it's here just in case
    time.sleep(2)

    #copy data files to the dist-dir
    if data <> '':
        shutil.copytree(data, new+os.path.split(data)[1])

    #delete the setup script (finishing the program and closing)
    os.remove(temp)

except:
    raw_input('ERROR!\nPossible Cause: missing or currupted python lib components')
    pass
