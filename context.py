#python imports
import os
import asyncio
import datetime


# expiry
# pip install python-whois
import whois

# SSL
import socket
import ssl

# 301 errors
import requests

# formats the url message
def url_format(url, starts, mode=""):
    url = str(url)
    url = url.lower()

    # weird bug where the letter W is being removed
    starts = starts.lower()
    if url.startswith(starts):
        url = url.strip(starts)

    if url.startswith(" "):
        url = url[1:]

    remove_items = ["https://",
                    "http://",
                    "www.",
                    "."
                    ]

    ends_with = [   ".com",
                    ".com.au",
                    ".io",
                    ".net",
                    ".co.uk",
                ]

    # removes unwanted items
    for item in remove_items:
        if url.startswith(item):
            item_len = len(item)
            url = url[item_len:]

    # allows full links to be used so user doesnt have to edit own data by removing anything after .com/etc/etc
    if "/" in url:
        split_url = url.split("/")
        url = split_url[0]

    # filter TLD from url 
    for item in ends_with:
        if url.endswith(item):
            url = url
        else:
            url = url + ".com"
    splitting_url = url.split(".com")
    url = splitting_url[0]
    if "." not in url:
        url = url + ".com"


    if mode == "basic":
        return url

    elif mode == "full":
        url = 'https://www.' + url
        return url

# checks ssl expiarys
def ssl_expiry_datetime(url, mode="SSL"):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=url,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((url, 443))
    ssl_info = conn.getpeercert()
    ssl_other_info = conn.cipher()


    if mode == "SSL":
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        #ssl_date_fmt = r'%b %d %Y %Z %H:%M:%S'

        # parse the string from the certificate into a Python datetime object
        website_SSL = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        website_SSL = str(website_SSL)
        website_SSL = website_SSL[0:-8]

        if website_SSL == "":
            website_SSL = "Unable to obtain SSL info."

        return website_SSL

    elif mode=="details":
        pprint.pprint(ssl_info)
        pprint.pprint(ssl_other_info)

#checks for 301 errors
def get_status_code(url):
    try:
        r = requests.get(url)

        if len(r.history) > 0:
            chain = ""
            code = r.history[0].status_code
            final_url = r.url
            for resp in r.history:
                chain += resp.url + " | "
            return str(code) + '\t' + str(len(r.history)) + '\t' + chain + '\t' + final_url + '\t'
        else:
            return str(r.status_code)
    except requests.ConnectionError:
        print("Error: failed to connect.")
        return 'Error: failed to connect'

# works out expiry code
def expiry_code(url):
    # checks the website details
    website_raw_data = whois.whois(url)

    # formats raw website data into mangiable chunks
    domain_name = website_raw_data["domain_name"]
    exp_date = website_raw_data["expiration_date"]
    try: 
        exp_date = str(exp_date[0])
    except:
        exp_date = str(exp_date)

    exp_date = exp_date[0:-8]

    if exp_date == "":
        exp_date = "Can only search for .com .net. org. gov"

    return exp_date