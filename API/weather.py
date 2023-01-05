import requests
from config import load_conf
from logging import getLogger

logger = getLogger(__name__)


class WeatherQueryError(Exception):
    def __init__(self):
        self.message = "Weather - во время запроса что-то пошло не так"


class WeatherRequestError(Exception):
    def __init__(self):
        self.message = "Weather - неправильный ответ от сервера"


class WeatherClient(object):

    def __init__(self):
        self.config = load_conf()
        self.base_url = self.config.WEATHER_URL

    def _request(self, method=None, query_params=None, params=None, headers=None):
        url = self.base_url
        if method is not None:
            url += method
        if query_params is not None:
            url += query_params
        try:
            request = requests.get(url, params=params, headers=headers)
            response = request.json()
        except:
            logger.exception("WeatherQueryError")
            raise WeatherQueryError

        if response.get("now"):
            return response
        else:
            logger.exception("WeatherRequestError")
            raise WeatherRequestError

    def get_weather(self, lat=55.833333, lon=37.616667, lang="ru_RU"):
        query_params = f"?lat={lat}&lon={lon}&lang={lang}"
        headers = {
            "X-Yandex-API-Key": self.config.WEATHER_TOKEN
        }

        return self._request(method="/v2/informers", query_params=query_params, headers=headers)

    def get_fact_temp(self, **kwargs):
        result = self.get_weather(**kwargs)
        return result["fact"]["temp"]
