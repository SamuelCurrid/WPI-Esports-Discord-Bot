import os
from discord.ext import commands


class BotTools(commands.Cog):
    """
    Allows the bot owner to manage functions of the bot including (un|re|)loading cogs
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def bot(self, ctx):
        """
        Top level command for bot functions
        Usage: .bot <command>

        :param ctx: Context object
        """

    @bot.command(name="reload")
    async def reload_cog(self, ctx, arg):
        """
        Reloads a cog from the filesystem.
        Usage: .bot reload <cog>

        :param ctx: Context object
        :param arg: Cog to reload
        """
        try:
            self.bot.unload_extension(f"cogs.{str(arg)}")
            self.bot.load_extension(f"cogs.{str(arg)}")
        except Exception as e:
            await ctx.send(f"**ERROR**: {type(e).__name__} - {e}")
        else:
            await ctx.send("Success")

    @bot.command(name="load")
    async def load_cog(self, ctx, arg):
        """
        Loads a cog into the bot
        """
        print(f"Attempting to load {str(arg)}")
        try:
            self.bot.load_extension(f"cogs.{str(arg)}")
        except Exception as e:
            await ctx.send(f"**ERROR**: {type(e).__name__} - {e}")
        else:
            await ctx.send("Success")

    @bot.command(name="unload")
    async def unload_cog(self, ctx, arg: str):
        """
        Unloads a cog from the bot

        :param ctx: Context object
        :param arg: Cog to unload
        """
        try:
            self.bot.unload_extension(f"cogs.{arg}")
        except Exception as e:
            if ctx is not None:
                await ctx.send(f"**ERROR**: {type(e).__name__} - {e}")
        else:
            if ctx is not None:
                await ctx.send("Success")

    @bot.command(name="list")
    async def list_cogs(self, ctx):
        """
        Lists loaded cogs
        Usage: .bot list

        :param ctx Context object
        """
        loaded_cogs = "Loaded cogs:\n"
        for k in self.bot.extensions.keys():
            loaded_cogs += f"{k}\n"
        await ctx.send(loaded_cogs)

    @bot.command(name="update")
    async def update_bot(self, ctx):
        """
        Uses git to update the bot
        Usage: .bot update

        :param ctx: Context object
        """
        import subprocess

        async with ctx.typing():
            proc = subprocess.run(
                "/usr/bin/git pull",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )

            if proc.returncode != 0:
                await ctx.send(f"**ERROR**: {str(proc.stderr.decode('UTF-8'))}")
            else:
                await ctx.send(proc.stdout.decode("UTF-8"))

    @bot.command()
    async def die(self, ctx):
        """
        Makes the bot shutdown gracefully
        Usage: .bot die

        :param ctx:
        """

        await ctx.send("Shutting down...")

        # Disconnect all VCs
        for vc in self.bot.voice_clients:
            await vc.disconnect()

        # Logs out
        await self.bot.logout()

        os.exit(0)


def setup(bot):
    bot.add_cog(BotTools(bot))
