import discord


async def silent_delete_msg(msg: discord.Message) -> None:
    """ If the message is not found, then no error is raised. """
    try:
        await msg.delete()
    except discord.HTTPException:
        pass  # As message may have already been deleted or bot may have
        # been kicked or had permissions removed


async def silent_delete_ref_msg(channel: 'InteractionChannel',  # type: ignore
                                msg_ref: discord.MessageReference) -> None:
    """ Fetches the reference message before silently deleting it. """
    try:
        if (not isinstance(channel,
                           discord.ForumChannel | discord.CategoryChannel)
                and msg_ref.message_id):
            ref_msg = await channel.fetch_message(msg_ref.message_id)
            await silent_delete_msg(ref_msg)
    except discord.HTTPException:
        pass  # As message may have already been deleted or bot may have
        # been kicked or had permissions removed
