import discord

from backend.config import TEX_PATH
from frontend.views.view import View


class TexRenderSuccess(View):

    def __init__(self, ori_msg: discord.Message) -> None:
        from frontend.buttons import Delete, Confirm
        super().__init__(btns=[Delete(del_ref_msg=True),
                               Confirm(del_ref_msg=True)])
        self.ori_msg = ori_msg

    async def send(self) -> None:
        """ Responds to the user with the rendered TeX. """
        content = f"**{self.ori_msg.author.display_name}**"
        self.msg = await self.ori_msg.reply(content=content,
                                            file=discord.File(TEX_PATH),
                                            mention_author=False,
                                            view=self)


class TexRenderFail(View):

    def __init__(self, ori_msg: discord.Message, err: ValueError) -> None:
        from frontend.buttons import Delete
        super().__init__(btns=[Delete(del_ref_msg=True)])
        self.ori_msg = ori_msg
        self.err = err

    async def send(self) -> None:
        """ Responds to the user with the error message. """
        cleaned = str(self.err).replace('ParseSyntaxException: ', '')
        content = (f"**☹  |  {self.ori_msg.author.display_name}**, your "
                   f"input has led to a `TeXParsingError`.\n"
                   f"*You may edit your message to generate a "
                   f"new image and then delete this one.*\n"
                   f"```{cleaned}```")
        self.msg = await self.ori_msg.reply(content=content,
                                            mention_author=False,
                                            view=self)
