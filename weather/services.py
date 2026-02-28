import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_URL = 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php'

SUPPORTED_LANGS = ('en', 'tc')

HKO_PLACE_KEY = {
    'en': 'Hong Kong Observatory',
    'tc': '香港天文台',
}

ENDPOINTS = {
    'current_weather': 'rhrread',
    'warning_summary': 'warnsum',
    'forecast': 'flw',
}

REQUEST_TIMEOUT = 10


def _fetch_json(data_type: str, lang: str = 'en') -> dict | None:
    params = {'dataType': data_type, 'lang': lang}
    try:
        resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        logger.exception("Failed to fetch HKO data with params %s", params)
        return None


def _parse_hkt(iso_string: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime('%H:%M HKT %d/%m/%Y')
    except (ValueError, TypeError):
        return iso_string or ''


def fetch_current_weather(lang: str = 'en') -> dict:
    data = _fetch_json(ENDPOINTS['current_weather'], lang)
    if not data:
        return {}

    update_time = _parse_hkt(data.get('updateTime', ''))
    hko_place = HKO_PLACE_KEY.get(lang, HKO_PLACE_KEY['en'])

    humidity_block = data.get('humidity', {})
    hko_humidity = None
    for h in humidity_block.get('data', []):
        if h.get('place') == hko_place:
            hko_humidity = h.get('value')
            break

    temp_block = data.get('temperature', {})
    temp_record_time = _parse_hkt(temp_block.get('recordTime', ''))

    hko_temp = None
    district_temps = []
    for t in temp_block.get('data', []):
        district_temps.append({
            'place': t.get('place', ''),
            'value': t.get('value'),
            'unit': t.get('unit', 'C'),
        })
        if t.get('place') == hko_place:
            hko_temp = t.get('value')

    rainfall_data = []
    for r in data.get('rainfall', {}).get('data', []):
        rainfall_data.append({
            'place': r.get('place', ''),
            'max': r.get('max', 0),
            'min': r.get('min', 0),
            'unit': r.get('unit', 'mm'),
            'is_main': r.get('main') == 'TRUE',
        })

    return {
        'update_time': update_time,
        'record_time': temp_record_time,
        'hko_temperature': hko_temp,
        'hko_humidity': hko_humidity,
        'district_temperatures': district_temps,
        'rainfall': rainfall_data,
        'icon_codes': data.get('icon', []),
        'warning_messages': data.get('warningMessage', []),
    }


def fetch_warning_summary(lang: str = 'en') -> list[dict]:
    data = _fetch_json(ENDPOINTS['warning_summary'], lang)
    if not data:
        return []

    warnings = []
    for _code, info in data.items():
        if not isinstance(info, dict):
            continue
        warnings.append({
            'name': info.get('name', ''),
            'code': info.get('code', ''),
            'action': info.get('actionCode', ''),
            'issue_time': _parse_hkt(info.get('issueTime', '')),
            'update_time': _parse_hkt(info.get('updateTime', '')),
        })
    return warnings


def fetch_forecast(lang: str = 'en') -> dict:
    data = _fetch_json(ENDPOINTS['forecast'], lang)
    if not data:
        return {}

    return {
        'update_time': _parse_hkt(data.get('updateTime', '')),
        'general_situation': data.get('generalSituation', ''),
        'forecast_period': data.get('forecastPeriod', ''),
        'forecast_desc': data.get('forecastDesc', ''),
        'outlook': data.get('outlook', ''),
        'tc_info': data.get('tcInfo', ''),
        'fire_danger_warning': data.get('fireDangerWarning', ''),
    }


def get_all_weather_data(lang: str = 'en') -> dict:
    if lang not in SUPPORTED_LANGS:
        lang = 'en'

    return {
        'current_weather': fetch_current_weather(lang),
        'warnings': fetch_warning_summary(lang),
        'forecast': fetch_forecast(lang),
    }
