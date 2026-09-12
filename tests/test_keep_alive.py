from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from overlord.keep_alive import _handle


async def test_handle_returns_200_ok() -> None:
    app = web.Application()
    app.router.add_get("/", _handle)

    async with TestClient(TestServer(app)) as client:
        response = await client.get("/")
        assert response.status == 200
        assert "alive" in (await response.text()).lower()
