import discord


async def silent_delete_msg(msg: discord.Message) -> None:
    """ If the message is not found, then no error is raised. """
    try:
        await msg.delete()
    except discord.errors.NotFound:
        pass  # As message already deleted


async def silent_delete_ref_msg(channel: discord.TextChannel,
                                msg_ref: discord.MessageReference) -> None:
    """ Fetches the reference message before silently deleting it.
    :raises AttributeError: if msg_ref is None
    """
    try:
        ref_msg = await channel.fetch_message(msg_ref.message_id)
    except discord.errors.NotFound:
        pass  # As message already deleted
    else:
        await silent_delete_msg(ref_msg)
