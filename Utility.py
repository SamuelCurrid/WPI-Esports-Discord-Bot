async def yes_no_helper(bot, ctx):
    """
    Waits for a yes or no response for the user

    :param bot: Bot that is processing the message
    :param ctx: Context object for the message
    :return: True if yes, False if no
    """
    while True:
        def check_author(m):
            return m.author.id == ctx.author.id

        response = await bot.wait_for('message', check=check_author)

        if response.content.lower() == "y" or response.content.lower() == "yes":
            return True
        elif response.content.lower() == "n" or response.content.lower() == "no":
            return False
        else:
            await ctx.send("Did not recognize your response. Make sure it is a yes or a no.")


def administrator_perms(ctx):
    return ctx.message.author.guild_permissions.administrator
