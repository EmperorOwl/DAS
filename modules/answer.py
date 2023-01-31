""" Code for responding to the user. """

import discord

from modules.buttons import Buttons

TITLES = {
    'display': 'Display',
    'limit': 'Limit',
    'derive': 'Derivative',
    'integrate': 'Integral',
    'solve': 'Solution',
    'expand': 'Expansion',
    'factor': 'Factorisation',
    'simplify': 'Simplification',
}


async def send(itx: discord.Interaction,
               inputs: str,
               cmd_name: str = None,
               btns: list[discord.ui.Button] = None) -> None:
    """ Sends the user the answer. """
    cmd_name = itx.command.qualified_name if not cmd_name else cmd_name
    await itx.response.send_message(
        embed=_get_embed(itx, cmd_name, inputs),
        file=_get_file(cmd_name)
    )
    await Buttons.with_msg(await itx.original_response(), btns)


def _get_embed(itx: discord.Interaction,
               cmd_name: str,
               inputs: str) -> discord.Embed:
    """ Returns the appropriate embed. """
    if 'graph' in cmd_name:
        cmd = itx.client.get_nested_app_command(cmd_name)
    else:
        cmd = itx.client.get_app_command(cmd_name)
    return discord.Embed(
        title=f"{itx.user.display_name}'s {TITLES.get(cmd_name, 'Graph')}",
        description=(
            f"{inputs}\n"
            f"Syntax: `/{cmd_name} "
            f"{' '.join([f'<{param.name}>' for param in cmd.parameters])}`\n"
            f"Time Taken: "
            f"`{(discord.utils.utcnow() - itx.created_at).total_seconds()}s`"
        ),
        colour=discord.Colour.blue(),
        timestamp=discord.utils.utcnow()
    ).set_image(
        url=f"attachment://{'plot.png' if 'graph' in cmd_name else 'tex.png'}"
    ).set_footer(
        text="Powered by Matplotlib"
    )


def _get_file(cmd_name: str) -> discord.File:
    """ Returns the appropriate image. """
    if 'graph' in cmd_name:
        return discord.File('renders/plot.png')
    return discord.File('renders/tex.png')
