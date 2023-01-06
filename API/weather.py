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
        self.condition = {
            "clear": "☀️",
            "partly-cloudy": "🌤",
            "cloudy": "🌥",
            "overcast": "☁️",
            "drizzle": "🌦",
            "light-rain": "🌧",
            "rain": "🌧",
            "moderate-rain": "🌧",
            "heavy-rain": "🌧",
            "continuous-heavy-rain": "🌧",
            "showers": "🌧",
            "wet-snow": "🌨",
            "light-snow": "❄️",
            "snow": "❄️",
            "snow-showers": "❄️️",
            "hail": "🥶",
            "thunderstorm": "🌩",
            "thunderstorm-with-rain": "⛈️",
            "thunderstorm-with-hail": "⛈️"
        }
        self.wind_dir = {
            "nw": "↖️",
            "n": "⬆️",
            "ne": "↗️",
            "e": "➡️",
            "se": "↘️",
            "s": "⬇️",
            "sw": "↙️",
            "w": "⬅️",
            "c": "⏺️"
        }
        self.daytime = {
            "d": "☀️ ",
            "n": "🌙 "
        }
        self.moon_code = ['🌕', '🌖', '🌖', '🌖', '🌗', '🌘', '🌘', '🌘', '🌑', '🌒', '🌒', '🌒', '🌓', '🌔', '🌔', '🌔']
        self.lat = self.config.WEATHER_DEFAULT_LAT
        self.lon = self.config.WEATHER_DEFAULT_LON
        self.lang = self.config.WEATHER_DEFAULT_LANG

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

    def get_weather(self, lat=self.lat, lon=self.lon, lang=self.lang):
        query_params = f"?lat={lat}&lon={lon}&lang={lang}"
        headers = {
            "X-Yandex-API-Key": self.config.WEATHER_TOKEN
        }

        return self._request(method="/v2/informers", query_params=query_params, headers=headers)

    def get_fact_weather_message(self, **kwargs):
        fact_weather = self.get_weather(**kwargs)

        if fact_weather['fact']['daytime'] == "d":
            text = self.daytime["d"]
        else:
            text = self.daytime["n"]
        if fact_weather['forecast']['parts'][0]['part_name'] == "night":
            text += "Добрый вечер \n"
        elif fact_weather['forecast']['parts'][0]['part_name'] == "morning":
            text += "Доброй ночи \n"
        elif fact_weather['forecast']['parts'][0]['part_name'] == "evening":
            text += "Добрый день \n"
        else:
            text += "Доброе утро \n"
        text += f"{self.condition[fact_weather['fact']['condition']]} "\
                f"{fact_weather['fact']['temp']} ℃  " \
                f"💧{fact_weather['fact']['humidity']}%\n" \
                f"💨 {self.wind_dir[fact_weather['fact']['wind_dir']]} " \
                f"{fact_weather['fact']['wind_speed']} м/с\n" \
                f"🕛 {fact_weather['fact']['pressure_mm']} мм. рт. ст.\n" \
                f"🌞 {fact_weather['forecast']['sunrise']} " \
                f"{self.moon_code[fact_weather['forecast']['moon_code']]} " \
                f"{fact_weather['forecast']['sunset']}"

        return text
