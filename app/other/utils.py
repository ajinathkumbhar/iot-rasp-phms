import os
import datetime
import random, string

TAG = os.path.basename(__file__)
prog_name = ''

# version
major_ver = '1'
minor_ver = '01'

VERBOSE = True
DEBUG = True



def get_line(symbol='-', len=90):
    """Print dash line
    """
    line = symbol * len
    return line + '\n'


def get_empty_line():
    """Print empty line
    """
    line = '' + '\n'
    return line


def PrintLine(symbol='-', len=90):
    print symbol * len


def PrintEmptyLine():
    print ''


def GetVersion():
    """ Get app version
    """
    version = 'PHMS ' + '- V' + major_ver + '.' + minor_ver
    return version

def get_device_id():
    id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    return id.upper()

def get_current_time():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("%Y-%m-%d %H:%M:%S")

def GetLogMsg(tag, log_type, msg, arg=None):
    tag = tag + ' ' * (20 - len(tag))
    if type(msg) != str:
        log_msg = get_current_time() + ' ' + tag + ' ' + log_type + ':  ' + str(msg) + ' ' + arg
    else:
        log_msg = get_current_time() + ' ' + tag + ' ' + log_type + ':  ' + msg + ' ' + arg
    return log_msg


def PLOGE(tag='tag', msg=None, arg='', exit=False, strip=False):
    """Print Error logs
    """
    log_type = 'E'
    log_msg = GetLogMsg(tag, log_type, msg, arg)
    if not strip:
        print log_msg
    else:
        print log_msg,
    if exit is True:
        os.sys.exit(-1)


def PLOGD(tag='', msg='', arg='', strip=False):
    """Print Debug logs
    """
    log_type = 'D'
    log_msg = GetLogMsg(tag, log_type, msg, arg)
    if not strip:
        print log_msg
    else:
        print log_msg,


def PLOGV(tag='', msg='', arg='', strip=False):
    """Print Verbose logs
    """
    if VERBOSE:
        log_type = 'V'
        log_msg = GetLogMsg(tag, log_type, msg, arg)
        if not strip:
            print log_msg
        else:
            print log_msg,
