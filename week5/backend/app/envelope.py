import json
from typing import Any

from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute


class EnvelopeRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()

        async def custom_handler(request) -> Response:
            response: Response = await original(request)

            if not isinstance(response, JSONResponse):
                return response

            try:
                payload: Any = json.loads(response.body)
            except Exception:
                return response

            if isinstance(payload, dict) and "ok" in payload:
                return response

            headers = {
                k: v
                for k, v in response.headers.items()
                if k.lower() != "content-length"
            }

            return JSONResponse(
                status_code=response.status_code,
                headers=headers,
                content={"ok": True, "data": payload},
            )

        return custom_handler
