import discord
from abc import ABC, abstractmethod


class View(ABC, discord.ui.View):
    """ Represents an abstract view. """
    TIMEOUT = 3.0 * 60

    def __init__(self, btns: list[discord.ui.Button] | None = None) -> None:
        super().__init__(timeout=self.TIMEOUT)
        self._add_btns(btns if btns else [])
        self.msg = None

    def _add_btns(self, btns: list[discord.ui.Button]) -> None:
        """ Attaches the buttons to this view. """
        for btn in btns:
            self.add_item(btn)

    @abstractmethod
    async def send(self) -> None:
        """ Responds to the user with this view. """
        # This method must initialise self.msg so that timeout works
        pass

    async def on_timeout(self) -> None:
        """ Removes the buttons from this view on timeout. """
        try:
            await self.msg.edit(view=self.clear_items())  # type: ignore
        except discord.errors.NotFound:
            pass  # As message may have already been deleted.
        finally:
            self.stop()
