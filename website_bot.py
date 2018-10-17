#python imports
import os
import asyncio
import datetime
import pprint

#discord imports
import discord
from discord.ext.commands import Bot
from discord.ext import commands

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

####################
# Discord code
####################
Client = discord.Client()
client = commands.Bot(command_prefix = "!")
client.remove_command('help')

TOKEN = "NDk0NzExMTAwNjgwNjk5OTE1.Do3fSg.5WYOWCzlXobo3aPPx0AEdMofooM"

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Type !help '))
    print("Bot is online and ready to go.")
    #await client.send_message(discord.Object(id='436684743807860746'), "Bot online")

@client.command(pass_context=True)
async def website(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    raw_message = ctx.message.content

    basic_url = url_format(raw_message, '!website', mode="basic")
    full_url = url_format(raw_message, '!website', mode="full")
    shothand_url = basic_url[0:-3]

    # expiry
    exp_date = expiry_code(basic_url)

    #SSL
    website_SSL = (ssl_expiry_datetime(basic_url))

    #301 error codes
    error_code = get_status_code(full_url)

    await client.send_message(channel, f"Full Website data for {shothand_url}:")
    await client.send_message(channel, f"SSL expiry date (Y/M/D): {website_SSL}")
    await client.send_message(channel, f"Domain expiry date: {exp_date}")
    await client.send_message(channel, f"Error Code: {error_code}")
    await client.send_message(channel, f"At the request of: {author}")

@client.command(pass_context=True)
async def details(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    raw_message = ctx.message.content

    basic_url = url_format(raw_message, '!details', mode="basic")
    full_url = url_format(raw_message, '!details', mode="full")
    shothand_url = basic_url[0:-3]

    website_SSL = (ssl_expiry_datetime(basic_url, mode="details"))

@client.command(pass_context=True)
async def expiry(ctx):
    # gets the date and formats it
    channel = ctx.message.channel
    raw_message = ctx.message.content
    basic_url = url_format(raw_message, "!expiry", mode="basic")
    
    exp_date = expiry_code(basic_url)

    await client.send_message(channel, f"{basic_url} expiry date: {exp_date}")

@client.command(pass_context=True)
async def SSL(ctx):
    channel = ctx.message.channel
    raw_message = ctx.message.content
    raw_message = ctx.message.content
    basic_url = url_format(raw_message, '!SSL', mode="basic")

    website_SSL = (ssl_expiry_datetime(basic_url))

    await client.send_message(channel, f"{basic_url} SSL expiry date (Y/M/D): {website_SSL}")

@client.command(pass_context=True)
async def error(ctx):
    channel = ctx.message.channel
    raw_message = ctx.message.content
    raw_message = ctx.message.content
    basic_url = url_format(raw_message, '!error', mode="basic")
    full_url = url_format(raw_message, '!error', mode="full")
    shothand_url = basic_url[0:-3]

    error_code = get_status_code(full_url)

    await client.send_message(channel, f"{shothand_url}:")
    await client.send_message(channel, f"Error Code: {error_code}")

# better way to make commands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed_message = discord.Embed(
            description="If not .com domain use full TLD (!website google.com.au or !website google.io) otherwise you can just !website google.",
            colour = discord.Colour.orange(),
    )

    embed_message.set_author(name='Mimirons website checker')
    embed_message.add_field(name='!website', value='Runs all website checks', inline=False)
    embed_message.add_field(name='!expiry', value='Checks for website name expiry', inline=False)
    embed_message.add_field(name='!SSL', value='Checks for SSL expiry date', inline=False)
    embed_message.add_field(name='!error', value='Check for common website errors, 301, 200', inline=False)

    await client.say(embed=embed_message)


client.run(TOKEN)
