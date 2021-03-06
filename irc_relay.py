#!/usr/bin/python3
import socket
import time
import threading
import sys
import os
import json
from config import *

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("irc_relay.py now running")
irc.connect((server, 6667))
print("Connecting to " + server)
time.sleep(15)
irc.send(bytes("USER "+nick+" * * *:user \n", "UTF-8"))
irc.send(bytes("NICK "+nick+" \n", "UTF-8"))
time.sleep(15)
irc.send(bytes("PRIVMSG nickserv :identify sertroid "+ password +" \n", "UTF-8"))
time.sleep(10)
irc.send(bytes("JOIN "+channel+" \n", "UTF-8"))
print("Connected to IRC, beginning flood")

def irc_text():
    while True:
        text = irc.recv(2040)
        text = text.decode("UTF-8")
        if text.find("PING") != -1:
            irc.send(bytes("PONG \n", "utf-8"))
            #print("PONG")


def output():
    with open('/home/user/sertroid/pubmed_data.json') as f:           
            f = json.load(f)
            for dict in f:  
                url = dict['url']  
                doi = dict['doi']
                title = dict['title']
                name = dict['name']                   
                irc.send(bytes("PRIVMSG " + channel + " :[Pubmed] " + "[{}] ".format(name) + title + " URL: " + url  + " DOI: " + doi + " \n", 'utf-8'))
                time.sleep(1)
            print("Flood complete, exiting")
            os._exit(0)

def main():
    t1 = threading.Thread(target = irc_text)
    t2 = threading.Thread(target = output)
    t1.start()
    t2.start()

main()
