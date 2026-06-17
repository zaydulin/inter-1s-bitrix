import base64
import json
from dataclasses import dataclass
from typing import Any
from urllib import error, parse, request


class IntegrationError(Exception):
    pass


@dataclass
class HttpClient:
    base_url: str
    timeout: int
    headers: dict[str, str]

    def get_json(self, path: str) -> list[dict[str, Any]]:
        response = self._request("GET", path)
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            items = response.get("items")
            if isinstance(items, list):
                return items
        raise IntegrationError("Ожидался JSON-массив или объект с ключом 'items'.")

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self._request("POST", path, payload)
        if isinstance(response, dict):
            return response
        return {"result": response}

    def post_json_list(self, path: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
        response = self._request("POST", path, payload)
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            items = response.get("items")
            if isinstance(items, list):
                return items
        raise IntegrationError("Ожидался JSON-массив или объект с ключом 'items'.")

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = parse.urljoin(self.base_url.rstrip("/") + "/", path.lstrip("/"))
        data = None
        headers = {"Content-Type": "application/json", **self.headers}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        req = request.Request(url=url, data=data, method=method, headers=headers)
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise IntegrationError(f"HTTP {exc.code} for {url}: {detail}") from exc
        except error.URLError as exc:
            raise IntegrationError(f"Не удалось подключиться к {url}: {exc.reason}") from exc

        if not body:
            return {}

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise IntegrationError(f"Ответ от {url} не является JSON.") from exc


def build_basic_auth(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"
