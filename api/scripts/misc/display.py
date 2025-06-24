from scripts.renderer import render_tex
from scripts.utils import Result, Error, Response


def display_text(args: dict) -> Response:
    try:
        text = args['text']
        pretty = {"text": text}  # Don't make pretty as did not parse
        image = render_tex(text)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
