#!/usr/bin/python
# ------------------------------------------------------------------+
# Name: FTPClient.py                                               |
# Autor: oTropicalista                                             |
# Github: https://github.com/oTropicalista                         |
# Repository: https://github.com/oTropicalista/silver-enigma.git   |
# Data: 12/11/2020                                                 |
# ------------------------------------------------------------------+

# To-do
# Histórico de comandos com FileHistoriry > prompt_toolkit.history

import os
import sys
import getpass
import argparse
from configparser import ConfigParser
from prompt_toolkit import prompt
from ftplib import FTP
from time import sleep
import FTPUtils


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
        FTPUtils.quitConn(ftp)
    elif comm == "clear" or comm == "cls":
        clearTerm()
    elif comm == "ls":
        ret = FTPUtils.listDir(ftp, array[1:])
        showTerm(ret)
    elif comm == "pwd":
        print(FTPUtils.workDir(ftp))
    elif comm == "cd":
        res = FTPUtils.changeDir(ftp, array[1])
        if res == False:
            print(color.RED + color.BOLD + "[!] Não foi possível acessar o diretório {}".format(array[1]) + color.END)
    elif comm == "get":
        FTPUtils.getFile(ftp, array[1])
    elif comm == "up":
        res = FTPUtils.upFile(ftp, array[1])
        if res == False:
            print(color.RED + color.BOLD + "[!] Falha ao fazer upload do(s) arquivo(s) {}".format(array[1]) + color.END)
        else:
            print(color.GREEN + color.BOLD + "[*] Upload concluído do arquivo {}".format(array[1]) + color.END)
    elif comm == "mkdir":
        res = FTPUtils.makeDir(ftp, array[1])
        if res == False:
            print(color.RED + color.BOLD + "[!] Erro ao criar o diretório {}".format(array[1]) + color.END)
        else:
            print(color.GREEN + color.BOLD + "[*] Diretório criado {}".format(array[1]) + color.END)



    elif comm == "reset":
        resetSelf()

def showTerm(obj):
    for line in obj:
        n = ' '.join(line)
        print("- {}".format(n))

def clearTerm():
    os.system("clear")

def resetSelf():
    os.execv(sys.executable, ['python'] + sys.argv)

def init():
    print(FTPUtils.welcome(ftp))
    while True:
        user_input = prompt(color.BLUE + "{}".format(params.NAME) + color.END + " [{}] ".format(FTPUtils.whereAmI(ftp)))
        readCmd(user_input)

if __name__ == "__main__":
    print(color.BLUE + color.BOLD + params.TITLE + color.END)
    sleep(1)
    if len(sys.argv) == 1:
        user = getpass.getuser()
        while True:
            passwd = getpass.getpass(f"[+] Senha: ")
        #user = input(color.BLUE + "[+] Usuário: " + color.END)
        #sswd = color.BLUE + "[+] Senha:" + color.END
        ftp = FTPUtils.conn(params.USER, params.PASSWD)
    else:
        if sys.argv[1] == "-d":
            ftp = FTPUtils.conn(params.USER, params.PASSWD)
        elif sys.argv[1] == "-l":
            ftp = FTPUtils.conn(sys.argv[2], sys.argv[3])

    print(color.BLUE + "[+] Conectando ao servidor FTP..." + color.END)
    
    if ftp == False:
        print(color.RED + color.BOLD + "[!] Erro na conexão com o servidor" + color.END)
    init()
