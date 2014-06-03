#encoding=utf8

import os, sys
import logging.config
import uuid


def get_current_file_path():
    path = sys.path[0]

    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
    

#logger = logging.getLogger()
#logging.config.fileConfig("/var/www/webot/blog/config.conf")
   
def getLogger():
    return logging.getLogger()

def getUUUID():
    return str(uuid.uuid4())

def IsLinux():
    import platform
    sysstr = platform.system()
    if sysstr=="Linux":
        return True
    return False

fp = None
def IsRunning():
    '''
    功能：判断是否已经启动了一个进程
    '''
    global fp
    lock_file_path = get_current_file_path() + "/running.lock"
    pid_file_path =  get_current_file_path() + "/running.pid"
    
    if IsLinux():
        fp = open(lock_file_path, "w")
        import fcntl
        try:
            fcntl.flock(fp.fileno(),  fcntl.LOCK_EX | fcntl.LOCK_NB)
            import os
            fpid = open(pid_file_path, "w")
            pid = os.getpid()
            fpid.write("%s"%pid)
            fpid.close()
        except IOError:
            return True
        
        return False

    else:
        try:
            import os
            if os.path.exists(lock_file_path):
                os.unlink(lock_file_path)

            fp = os.open(lock_file_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            
            fpid = open(pid_file_path, "w")
            pid = os.getpid()
            fpid.write("%s"%pid)
            fpid.close()
        except EnvironmentError, e:
            if e.errno == 13:
                return True
            else:
                return False
        
    return False

    
def StopRunning():
    '''
    通过进程Id杀掉进程
    '''
    pid_file_path =  get_current_file_path() + "\\running.pid"
    pid = open(pid_file_path, "r").read()
    print pid
    pid = int(pid)
    
    if IsLinux():
        #绑定通知关闭
        import os,signal
        os.kill(pid, signal.SIGTERM)
    else:
        #windows
#         try:
#             import win32api
#             win32api.SetConsoleCtrlHandler(callback, True)
#         except ImportError:
#             raise Exception("pywin32 not install for Python")
        
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(1, 0, pid )
        kernel32.TerminateProcess(handle, 0)

if __name__=="__main__":
    
    is_stop = False
    for arg in sys.argv[1:]:
        if arg=="stop":
            StopRunning()
            print "start to stop"
            is_stop = True

    if is_stop == False:
        print "is_stop false"
        if IsRunning():
            print "Another Instance is running .."
            sys.exit(-1)
        else:
            import time
            time.sleep(1000)

    
    
    
