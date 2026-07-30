import asyncio
from unittest.mock import AsyncMock, patch

from api.index import lifespan


def test_lifespan_does_not_raise_when_db_init_fails():
    async def run_lifespan():
        async with lifespan(None):
            pass

    with patch("api.index.init_db_pool", new=AsyncMock(side_effect=RuntimeError("boom"))), patch(
        "api.index.close_db_pool", new=AsyncMock()
    ):
        asyncio.run(run_lifespan())
