from requests import session, JSONDecodeError
import uuid
import curlify

from restclient.configuration import Configuration


class RestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_logs = configuration.disable_logs
        self.session = session()
        # Логгер убран, чтобы не зависеть от structlog в окружении тестов
        self.log = None

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def get(self, path, **kwargs):
        return self._send_request(method="GET", path=path, **kwargs)

    def post(self, path, **kwargs):
        return self._send_request(method="POST", path=path, **kwargs)

    def put(self, path, **kwargs):
        return self._send_request(method="PUT", path=path, **kwargs)

    def delete(self, path, **kwargs):
        return self._send_request(method="DELETE", path=path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        # even_id используется для трассировки запроса
        even_id = str(uuid.uuid4())
        full_url = self.host + path

        # вкл/откл логирование
        if self.disable_logs:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            return rest_response

        # настройка логирования Запроса (упрощённый вывод в консоль)
        print(
            f"[Request][{even_id}] method={method}, url={full_url}, "
            f"params={kwargs.get('params')}, headers={kwargs.get('headers')}, "
            f"json={kwargs.get('json')}, data={kwargs.get('data')}"
        )

        # настроиваем ответ и возвращаем его
        rest_response = self.session.request(method=method, url=full_url, **kwargs)

        # тут формируем curl (для разраба, отчетность)
        curl = curlify.to_curl(rest_response.request)
        print(curl)

        # логируем ответ (тоже через print, чтобы не требовать structlog)
        print(
            f"[Response][{even_id}] status_code={rest_response.status_code}, "
            f"headers={rest_response.headers}, json={self._get_json(rest_response)}"
        )

        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
