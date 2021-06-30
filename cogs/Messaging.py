from Utility import yes_no_helper, administrator_perms
from discord.ext import commands

import discord
import typing


class Messaging(commands.Cog):
    """
    Messaging tools
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(administrator_perms)
    @commands.guild_only()
    async def echo(self, ctx, channel: discord.TextChannel, *, msg: typing.Optional[str]):
        """
        Forwards message / attachments appended to the command to the given channel
        Usage: .echo <channel> <message>

        :param ctx: context object
        :param channel: channel to send the message to
        :param msg: message to send
        """
        # Check for attachments to forward
        attachments = []
        if len(ctx.message.attachments) > 0:
            for i in ctx.message.attachments:
                attachments.append(await i.to_file())

        mention_perms = discord.AllowedMentions.none()

        # Check for user mentions
        if len(ctx.message.mentions) > 0:
            # Check if users are to be pinged

            users = " ".join([x.mention for x in ctx.message.mentions])
            await ctx.send(
                f"This message mentions {users} - would you like it to ping them? (Y/N)",
                allowed_mentions=mention_perms
            )

            if await yes_no_helper(self.bot, ctx):
                mention_perms.users = True

        # Check for role mentions
        if len(ctx.message.role_mentions) > 0:
            # Check if author has perms to mention roles
            if administrator_perms(ctx):
                perms = True
            else:
                for role in ctx.message.role_mentions:
                    if not role.mentionable:
                        perms = False
                        break
                else:
                    perms = True

            if perms:
                roles = " ".join([x.mention for x in ctx.message.role_mentions])
                await ctx.send(
                    f"This message mentions {roles} - would you like it to ping them? (Y/N)",
                    allowed_mentions=mention_perms
                )

                if await yes_no_helper(self.bot, ctx):
                    mention_perms.roles = True

        # Check for @everyone and @here mentions
        if ctx.message.mention_everyone:
            if ctx.author.guild_permissions.mention_everyone:
                await ctx.send(
                    "This message mentions @here or @everyone - would you like it to ping those? (Y/N)",
                    allowed_mentions=mention_perms
                )

                if await yes_no_helper(self.bot, ctx):
                    mention_perms.everyone = True

        if msg is not None:
            message = await channel.send(msg, files=attachments, allowed_mentions=mention_perms)
            await ctx.send(
                "Message sent (<https://discordapp.com/channels/" + str(ctx.guild.id) + "/" + str(message.channel.id) +
                "/" + str(message.id) + ">)",
            )
        elif len(attachments) > 0:
            message = await channel.send(files=attachments)
            await ctx.send(
                "Message sent (<https://discordapp.com/channels/" + str(ctx.guild.id) + "/" + str(message.channel.id) +
                "/" + str(message.id) + ">)",
            )
        else:
            await ctx.send("No content to send.")

    @commands.command(pass_context=True, aliases=["echoEdit", "editEcho"])
    @commands.check(administrator_perms)
    @commands.guild_only()
    async def echo_edit(self, ctx, bot_msg: discord.Message, *, msg):
        """
        Edits a message sent by the bot with the message given
        Usage: .echoEdit <messageLink> <message>

        :param ctx: context object
        :param bot_msg: link or id of the message to edit
        :param msg: message to edit to
        """
        # Check if Gompei is author of the message
        if bot_msg.author.id != self.bot.user.id:
            await ctx.send("Cannot edit a message that is not my own")
        else:
            await bot_msg.edit(content=msg)
            await ctx.send(
                "Message edited (<https://discordapp.com/channels/" + str(ctx.guild.id) + "/" +
                str(bot_msg.channel.id) + "/" + str(bot_msg.id) + ">)"
            )


def setup(bot):
    bot.add_cog(Messaging(bot))
