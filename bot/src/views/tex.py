import discord

from src.api import TimeoutException, InputException, ServerException
from src.views.view import View


class TexRenderSuccess(View):

    def __init__(self, ori_msg: discord.Message, image: str) -> None:
        from src.buttons import Delete, Confirm
        super().__init__(btns=[Delete(del_ref_msg=True),
                               Confirm(del_ref_msg=True)])
        self.ori_msg = ori_msg
        from src.utils import decode_image
        self.image = decode_image(image)

    async def send(self) -> None:
        content = f"**{self.ori_msg.author.display_name}**"
        file = discord.File(fp=self.image, filename='tex.png')
        self.msg = await self.ori_msg.reply(content=content,
                                            file=file,
                                            mention_author=False,
                                            view=self)


class TexRenderFail(View):

    def __init__(self, ori_msg: discord.Message, error: Exception) -> None:
        from src.buttons import Delete
        super().__init__(btns=[Delete(del_ref_msg=True)])
        self.ori_msg = ori_msg
        self.error = error

    async def send(self) -> None:
        if isinstance(self.error, InputException):
            err_msg = self.error.message
            err_msg = err_msg.replace('ParseException: ', '')
            err_msg = err_msg.replace('ParseSyntaxException: ', '')
            err_msg = err_msg.replace('ParseFatalException: ', '')
            content = (f"☹ Looks like there was a `TeXParsingError`\n"
                       f"*You may edit your message to generate a "
                       f"new image and then delete this one.*\n"
                       f"```{err_msg}```")
        elif isinstance(self.error, TimeoutException):
            content = "Your request timed out, please try again."
        elif isinstance(self.error, ServerException):
            content = ("Looks like there is an issue with the bot.\n"
                       "Please try again later.")
        else:
            raise self.error
        self.msg = await self.ori_msg.reply(content=content,
                                            mention_author=False,
                                            view=self)
