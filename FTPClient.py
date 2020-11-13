#!/usr/bin/python
# ------------------------------------------------------------------+
# Name: FTPClient.py                                                   |
# Autor: oTropicalista                                             |
# Github: https://github.com/oTropicalista                         |
# Repository: https://github.com/oTropicalista/****   |
# Data: 12/11/2020                                                 |
# ------------------------------------------------------------------+

# To-do
# Histórico de comandos

import os
import argparse
from configparser import ConfigParser
from ftplib import FTP


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class params:
    cfg = ConfigParser()
    cfg.read('config.txt')

    NAME = cfg['app']['NAME']
    VERSION = cfg['app']['VERSION']
    DESCRIPTION = cfg['app']['DESCRIPTION']
    AUTHOR = cfg['app']['AUTHOR']
    TITLE = """
     _____ _____ ____        
    |  ___|_   _|  _ \ _   _ 
    | |_    | | | |_) | | | |
    |  _|   | | |  __/| |_| |
    |_|     |_| |_|    \__, |
                       |___/ {}
    """.format(VERSION)

    USER = cfg['params']['user']
    PASSWD = cfg['params']['pass']
    PORT = cfg['params']['port']

    WDIR = ''

def readCmd(cmd):
    array = cmd.split(' ') #separar entradas
    comm = array[0]

    if comm == "quit" or comm == "bye":
        quitConn()
    elif comm == "clear" or comm == "cls":
        clearTerm()
    elif comm == "ls":
        listDir()
    elif comm == "pwd":
        workDir()
    elif comm == "cd":
        changeDir(array[1])
    elif comm == "get":
        getTextFile(array[1])

def changeWDir():
    params.WDIR = ftp.pwd()

def quitConn():
    print("Fechando conexão...")
    ftp.quit()
    print("Bye")
    exit()

def clearTerm():
    os.system("clear")

def welcome():
    ftp.getwelcome()


def listDir():
    list = []
    ftp.retrlines('LIST', list.append)
    for fl in list:
        fl.split(' ')
        print(fl)


def changeDir(dst):
    ftp.cwd(dst)
    changeWDir()


def getFile(filename):
    try:
        ftp.retrbinary("RETR" + filename, open(filename).write)
    except:
        print("Erro no getFile")


def workDir():
    wdir = ftp.pwd()
    print(wdir)


def makeDir(dirname):
    try:
        ftp.mkd(dirname)
    except:
        print("Erro ao criar o diretório {}".format(dirname))


def getSizeText(name):
    ftp.size(name)


def getSizeBin(name):
    ftp.sendcmd('TYPE I')  # for ASCII name
    ftp.size(name)


def getTextFile(name):
    f_src = name
    f_copy = name

    try:
        with open(f_copy, 'w') as fp:
            res = ftp.retrlines('RETR' + f_src, fp.write)

            if not res.startswith('226 Transfer complete'):
                print("Download falido")
                if os.path.isfile(f_copy):
                    os.remove(f_copy)
    except:
        print("Erro no getTextFile")

        if os.path.isfile(f_copy):
            os.remove(f_copy)

def upTextFile(name):
    try:
        with open(name, 'rb') as fp:
            res = ftp.storlines("STOR " + name, fp)

            if not res.startswith('226 Transfer complete'):
                print("Erro no upload")
    except:
        print("Erro no upTextFile")


def init():
    print(color.BLUE + color.BOLD + params.TITLE + color.END)
    # ftp.retrlines('LIST')
    # ftp.cwd("/dir")
    welcome()
    # list_dir()
    while True:
        cmd = input("{} [{}] ".format(params.NAME, params.WDIR))
        readCmd(cmd)

    ftp.quit()


if __name__ == "__main__":
    try:
        ftp = FTP('192.168.0.111')
        ftp.login(params.USER, params.PASSWD)
        print("Conectado a 192.168.0.111...")
        changeWDir()
    except:
        print("Erro na conexão")

    init()
