from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi import Response
from typing import Annotated
from fastapi import Cookie
from . import utils


def create_app() -> FastAPI:
    templates = Jinja2Templates(directory="templates")
    templates.env.filters["process_paragraph"] = utils.process_paragraph

    app = FastAPI(redoc_url=None, docs_url=None)
    book = utils.get_book()

    @app.get("/", response_class=HTMLResponse)
    async def home_page(
        request: Request,
        index: Annotated[str, Cookie()] = "0",
        steps: Annotated[int, Cookie()] = 0,
    ):
        return templates.TemplateResponse(
            "home.html",
            {
                "paragraph": book[index],
                "request": request,
                "index": index,
                "steps": steps,
            },
        )

    @app.get("/paragraph/{index}", response_class=HTMLResponse)
    async def get_paragraph(
        request: Request,
        index: str,
        steps: Annotated[int, Cookie()] = 0,
    ):
        response = templates.TemplateResponse(
            "paragraph.html",
            {
                "request": request,
                "paragraph": book[index],
                "index": index,
            },
        )

        if index != "0":
            response.set_cookie(key="steps", value=steps + 1)
        else:
            response.set_cookie(key="steps", value=0)

        response.set_cookie(key="index", value=index)
        response.headers["HX-Trigger"] = "steps"

        return response

    @app.post("/reset", response_class=HTMLResponse)
    async def reset_game():
        response = Response("OK")

        response.set_cookie(key="index", value="0")
        response.set_cookie(key="steps", value=0)
        response.headers["HX-Trigger"] = "reset"

        return response

    @app.get("/steps", response_class=HTMLResponse)
    async def player_steps(
        request: Request,
        steps: Annotated[int, Cookie()] = 0,
    ):
        return templates.TemplateResponse(
            "steps.html",
            {
                "request": request,
                "steps": steps,
            },
        )

    return app
