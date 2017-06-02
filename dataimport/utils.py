from datetime import datetime
from decimal import Decimal

def sizeof(num):
    for x in ['byte','Kb','Mb','Gb']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'Tb')

def sizeofS(str):
    num = float(str)
    for x in ['byte','Kb','Mb','Gb']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'Tb')

def point2comma(num):
    mystring=str(num)
    return mystring.replace(".",",")

def convertTime(unixtime):
    return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')

def convertTimeS(unixtime):
    time = Decimal(unixtime)
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def nowunix():
    return datetime.now().strftime('%s')

##convert format like 5,5 Mb from Cdcat
def bytesize(string):
    size = string.split()[0]
    size = size.replace(",",".")
    size = float(size)

    if "byte" in string:
        pass
    elif "Kb" in string:
        size *= 1024
    elif "Mb" in string:
        size *= 1024*1024
    elif "Gb" in string:
        size *= 1024*1024*1024
    elif "Tb" in string:
        size *= 1024*1024*1024*1024
    return size
