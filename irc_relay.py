#!/usr/bin/python3
import socket
import time


server = "irc.tripsit.me"
nick = "sertroid"
channel ="##testing"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

input_file = open("pubmed_output.txt", "r")

test_send = input_file.readlines()

irc.connect((server, 6667))
print("Connecting to " + server)

print("Waiting 15 seconds")
time.sleep(15)

irc.send(bytes("USER "+nick+" * * *:user \n", "UTF-8"))
irc.send(bytes("NICK "+nick+" \n", "UTF-8"))
print("Sent USER and NICK")

print("Waiting 15 seconds")
time.sleep(15)

irc.send(bytes("PRIVMSG nickserv :identify sertroid password1 \n", "UTF-8"))
print("Identifying with nickserv")

print("Waiting 10 seconds")
time.sleep(10)

irc.send(bytes("JOIN "+channel+" \n", "UTF-8"))
print("Joining channel")

while True:
    text = irc.recv(2040)
    text = text.decode("UTF-8")
    print(text)

    irc.send(bytes("PRIVMSG ##testing :{}".format(test_send), "utf-8"))
    time.sleep(1)

    if text.find("PING") != -1:
        irc.send(bytes("PONG \n", "utf-8"))
        print("PONG")