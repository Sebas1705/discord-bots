"""A tiny HTTP server whose only job is to give an uptime pinger something
to hit, so free hosts that sleep on inactivity (Replit's free tier) stay up.
No-op anywhere else — `main.py` only starts this when `REPL_ID` is set.
"""

import threading

from aiohttp import web


async def _handle(_: web.Request) -> web.Response:
    return web.Response(text="Overlord is alive.")


def _run() -> None:
    app = web.Application()
    app.router.add_get("/", _handle)
    web.run_app(app, host="0.0.0.0", port=8080, print=None)


def start() -> None:
    threading.Thread(target=_run, daemon=True).start()
