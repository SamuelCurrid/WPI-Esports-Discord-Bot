import discord
import os
import sys
import traceback
from datetime import datetime
from discord.ext import commands


wpi_esports = commands.Bot(command_prefix=".", case_insensitive=True, intents=discord.Intents.default())

startup_cogs = [
    "BotTools",
    "Messaging",
    "Streaming"
]

for cog in startup_cogs:
    wpi_esports.load_extension(f"cogs.{cog}")
    print(f"Loaded cog {cog}")


# Overwrite help command
wpi_esports.remove_command("help")

# Events
@wpi_esports.event
async def on_ready():
    """
    Loads default settings
    """
    await wpi_esports.change_presence(activity=discord.Game(name="Valorant", start=datetime.utcnow()))
    print("Logged on as {0}".format(wpi_esports.user))


@wpi_esports.event
async def on_command_error(ctx, error):
    """
    Default error handling for the bot

    :param ctx: context object
    :param error: error
    """
    if isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
        print("!ERROR! " + str(ctx.author.id) + " did not have permissions for " + ctx.command.name + " command")
    elif isinstance(error, commands.BadArgument):
        argument = list(ctx.command.clean_params)[len(ctx.args[2:] if ctx.command.cog else ctx.args[1:])]
        await ctx.send("Could not find the " + argument)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.command.name + " is missing arguments")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Bot is missing permissions.")
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@wpi_esports.command(pass_context=True)
@commands.is_owner()
async def help(ctx, command_name=None):
    """
    Sends help information
    Usage: .help (command)

    :param ctx: context object
    :param command_name: command in question
    """
    if command_name is None:
        help_embed = discord.Embed(title=wpi_esports.user.display_name, colour=discord.Colour.blue())
        help_embed.add_field(name="Documentation", value="N/A")
        help_embed.set_thumbnail(url=wpi_esports.user.avatar_url)
        help_embed.set_footer(text="N/A")
        await ctx.send(embed=help_embed)
    else:
        command = wpi_esports.get_command(command_name)
        if command is None:
            await ctx.send("Could not find the command " + command_name)
        else:
            description = command.help[:command.help.find("Usage:") - 1]
            usage = command.help[command.help.find("Usage:") + 7:command.help.find("\n\n")]
            embed = discord.Embed(
                title=command.name,
                colour=discord.Colour.blue(),
                description=description + "\n\n**Usage:** `" + usage + "`\n\n**Aliases:** " + ", ".join(command.aliases)
            )

            embed.set_footer(text="<> = required, () = optional")
            await ctx.send(embed=embed)


@wpi_esports.command()
@commands.is_owner()
async def ping(ctx):
    """
    Sends bot latency
    Usage: .ping

    :param ctx: context object
    """
    await ctx.send(f'Pong! `{int(wpi_esports.latency * 1000)}ms`')


# Run the bot
wpi_esports.run(os.environ["DISCORD_TOKEN"])
