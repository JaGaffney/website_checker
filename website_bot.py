from context import url_format, ssl_expiry_datetime, get_status_code, expiry_code

import discord
from discord.ext.commands import Bot
from discord.ext import commands

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
    website_SSL = ssl_expiry_datetime(basic_url)

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

    website_SSL = ssl_expiry_datetime(basic_url, mode="details")

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

    website_SSL = ssl_expiry_datetime(basic_url)

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
