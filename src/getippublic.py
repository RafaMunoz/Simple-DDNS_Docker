#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot
import sys
import json
import os
import urllib3
import time
from nslookup import Nslookup

# Check environment variable
def checkEnviron(env):
    try:
        val = os.environ[env]
        print("{0}: {1}".format(env, val))
        return val

    except KeyError:
        print("Please set the environment variable '{0}'".format(env))
        sys.exit(1)


# Request to API data
def requestAPI(argurl):
    try:
        resp = http.request('GET', url=argurl)

        if resp.status != 200:
            data_json = {"ok": False, "error_code": resp.status, "description": resp.data.decode('utf-8')}
        else:
            data_json = json.loads(resp.data.decode('utf-8'))
        return data_json

    except Exception as e2:
        data_json = {"ok": False, "description": str(e2)}
        return data_json


# Send message Telegram
def send_message(message):
    if telegram_token != "":
        bot.send_message(chat_id=int(id_telegram), text=message, parse_mode='Markdown')


# Mandatory environment variables
domains = checkEnviron("DOMAINS")
domains_list = domains.split(",")

url_ddns = checkEnviron("URL_DDNS")
username = checkEnviron("USERNAME")
password = checkEnviron("PASSWORD")

# Optional environment variables
try:
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    id_telegram = int(os.environ["ID_TELEGRAM"])

except KeyError:
    telegram_token = ""
    id_telegram = 0

    print("Telegram notifications not activated, to activate them put the environment variables 'TELEGRAM_TOKEN' "
          "and 'ID_TELEGRAM'")
    pass

# Objet HTTP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

# Bot telegram
bot = telebot.TeleBot(telegram_token)

# URL API
url_getip = "https://api.ipify.org?format=json"
request_ddns = "{0}/nic/update?hostname={1}&myip={2}"

# Set DNS server
# set optional Cloudflare public DNS server
dns_query = Nslookup(dns_servers=["1.1.1.1","8.8.8.8"])

last_ip = ""
dns_update = 0

while True:

    # Check IP Public
    ip_now = requestAPI(url_getip)["ip"]

    # Check DNS change
    if dns_update == 0:
        for domain in domains_list:
            ips_record = dns_query.dns_lookup(domain)

            if len(ips_record.answer) >= 1 and ips_record.answer[0] == ip_now:
                mes = "DNS servers already resolve the new IP address: *{0}* for domain: *{1}*".format(ip_now, domain)
                print(mes)
                send_message(mes)
                dns_update = 1

    if last_ip != ip_now:
        print("Public IP different: {0}, update Dynamic DNS".format(ip_now))

        # Check de IP for domains
        for domain in domains_list:
            url_update = request_ddns.format(url_ddns, domain, ip_now)
            headers = urllib3.util.make_headers(basic_auth="{0}:{1}".format(username, password),
                                                user_agent='simple-ddns')
            response = http.request(method="GET", url=url_update, headers=headers)

            if response.status == 200:
                data_split = response.data.decode('utf-8').split(" ")

                # Parse response
                if data_split[0] == "good" or data_split[0] == "nochg":
                    print("Updated domain: {0} IP address: {1}".format(domain, ip_now))
                    send_message("Updated domain: *{0}*\nIP address: *{1}*".format(domain, ip_now))
                    dns_update = 0

                else:
                    print("Error updating domain: {0} IP address: {1} Return code: "
                          "{2}".format(domain, ip_now, data_split[0]))
                    send_message("Error updating domain: *{0}*\nIP address: *{1}*\nReturn code: "
                                 "*{2}*".format(domain, ip_now, data_split[0]))

                last_ip = ip_now

            else:
                print("ERROR: Code {0} Data: {1}".format(response.status, response.data))

    time.sleep(5)
