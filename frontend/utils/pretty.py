def pretty_cmds(cmds) -> str:
    """ Returns a string representation of the bot's commands. """
    return ', '.join([f'`{cmd.name}`' for cmd in cmds])


def pretty_uptime(seconds) -> str:
    """ Returns a string representation of bot's uptime. """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days:.0f}d, {hours:.0f}h, {minutes:.0f}m and {seconds:.0f}s"


def pretty_inputs(itx) -> str:
    """ Returns the original inputs of an application command. """
    if 'graph' in itx.command.qualified_name:
        data = itx.data['options'][0]['options'][0]['options']
    else:
        data = itx.data['options']
    raw = {arg['name']: arg['value'] for arg in data}
    pretty = " ".join(f"{name}: {value}" for name, value in raw.items())
    return pretty
