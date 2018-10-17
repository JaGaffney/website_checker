# #python imports
# import os
# import asyncio
# import datetime

# #discord imports
# import discord
# from discord.ext.commands import Bot
# from discord.ext import commands

# # expiry
# # pip install python-whois
# import whois

# # SLL
# import socket
# import ssl

# # 301 errors
# import requests

# def url_format(url, starts, mode=""):
#     url = url.lower()
#     starts = starts.lower()

#     remove_items = [    starts,
#                         "https://",
#                         "http://",
#                         "www."
#                         ]

#     if url.endswith(".com"):
#         url = url
#     else:
#         url = url + ".com"

#     for items in remove_items:
#         if url.startswith(items):
#             url = url.strip(items)

#     if mode == "basic":
#         return url

#     elif mode == "full":
#         url = 'https://www.' + url
#         return url


# def ssl_expiry_datetime(hostname):
#     ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

#     context = ssl.create_default_context()
#     conn = context.wrap_socket(
#         socket.socket(socket.AF_INET),
#         server_hostname=hostname,
#     )
#     # 3 second timeout because Lambda has runtime limitations
#     conn.settimeout(3.0)

#     conn.connect((hostname, 443))
#     ssl_info = conn.getpeercert()
#     print(ssl_info)
#     # parse the string from the certificate into a Python datetime object
#     return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


# def get_status_code(url):
#     try:
#         r = requests.get(url)
#         print("Processing " + url)

#         if len(r.history) > 0:
#             chain = ""
#             code = r.history[0].status_code
#             final_url = r.url
#             for resp in r.history:
#                 chain += resp.url + " | "
#             return str(code) + '\t' + str(len(r.history)) + '\t' + chain + '\t' + final_url + '\t'
#         else:
#             return str(r.status_code) + '\t\t\t\t'
#     except requests.ConnectionError:
#         print("Error: failed to connect.")
#         return '0\t\t\t\t'

# # works out expiry code
# def expiry_code(url):
#     basic_url = url_format(url, '!expiry ', mode="basic")
#     # checks the website details
#     website_raw_data = whois.whois(basic_url)

#     # formats raw website data into mangiable chunks
#     domain_name = website_raw_data["domain_name"]
#     exp_date = website_raw_data["expiration_date"]
#     try: 
#         exp_date = str(exp_date[0])
#     except:
#         exp_date = str(exp_date)

#     return exp_date