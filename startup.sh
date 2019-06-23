#!/bin/bash
echo $(date) >> log.log && python3 /home/user/sertroid/pubmed-searcher.py && bash /home/user/sertroid/web_push.sh && python3 /home/user/sertroid/irc_relay.py
