#!/usr/bin/python
# ------------------------------------------------------------------+
# Name: FTPUtils.py                                                |
# Autor: oTropicalista                                             |
# Github: https://github.com/oTropicalista                         |
# Repository: https://github.com/oTropicalista/silver-enigma.git   |
# Data: 13/11/2020                                                 |
# ------------------------------------------------------------------+

import os
from ftplib import FTP
from FTPClient import params

def conn(user, passwd):
    try:
        ftp = FTP('192.168.0.111')
        ftp.login(user, passwd)
        whereAmI(ftp)
    except:
        return False

    return ftp

def whereAmI(ftp):
    return ftp.pwd()

def quitConn(ftp):
    print("Fechando conexão...")
    ftp.quit()
    print("Bye")
    exit()

def welcome(ftp):
    return ftp.getwelcome()


def listDir(ftp, array):
    #recebe argumentos    
    dir_list = []

    ftp.dir(dir_list.append)

    n_dir_list = []
    f_dir_list = []

    for line in dir_list:
            n_dir_list.append(line[29:].strip().split(' '))

    if not array:
        for line in n_dir_list:
            f_dir_list.append(line[4:])
        return f_dir_list

    elif array[0] == "--all" or array[0] == "-l":
        return n_dir_list


def changeDir(ftp, dst):
    try:
        ftp.cwd(dst)
        whereAmI(ftp)
        return True
    except:
        return False


def workDir(ftp):
    wdir = ftp.pwd()
    return wdir


def makeDir(ftp, dirname):
    try:
        ftp.mkd(dirname)
        return True
    except:
        return False

def getSizeText(ftp, name):
    ftp.size(name)


def getSizeBin(ftp, name):
    ftp.sendcmd('TYPE I')  # for ASCII name
    ftp.size(name)


def getFile(ftp, name):
    filename = name

    try:
        with open(filename, 'wb') as fp:
            res = ftp.retrbinary(f"RETR {filename}", fp.write)
            if not res.startswith('226 Transfer complete'):
                print("Erro no download")
#            res = ftp.retrlines('RETR' + f_src, fp.write)

#            if not res.startswith('226 Transfer complete'):
#                print("Download falido")
#                if os.path.isfile(f_copy):
#                    os.remove(f_copy)
    except:
        print("Erro no getTextFile")

def upFile(ftp, name):
    try:
        with open(name, 'rb') as fp:
            res = ftp.storbinary(f"STOR {name}", fp)
            if not res.startswith('226 Transfer complete'):
                return False
            return True
    except:
        print("Erro no upTextFile")
        return False