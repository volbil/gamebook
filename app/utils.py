from markupsafe import Markup
import json
import re


def get_book():
    return json.load(open("book.json", "r"))


def process_paragraph(raw_paragraph):
    italic_pattern = r"\*(.*?)\*"
    bold_pattern = r"\*\*(.*?)\*\*"
    paragraph_pattern = re.compile(r"\[(\d+)\]")

    raw_paragraph = re.sub(bold_pattern, r"<b>\1</b>", raw_paragraph)
    raw_paragraph = re.sub(italic_pattern, r"<i>\1</i>", raw_paragraph)
    raw_paragraph = re.sub(
        paragraph_pattern,
        r"""<button
            class="font-medium text-blue-400 hover:underline"
            hx-get="/paragraph/\1"
            hx-trigger="click"
            hx-target="#paragraph-content"
            hx-swap="innerHTML"
        >\1</button>""",
        raw_paragraph,
    )

    return Markup(raw_paragraph)
