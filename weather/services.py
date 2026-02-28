import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_URL = 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php'

ENDPOINTS = {
    'current_weather': {'dataType': 'rhrread', 'lang': 'en'}, # Hong Kong District Weather Report - every hour update
    'warning_summary': {'dataType': 'warnsum', 'lang': 'en'}, # Special Weather Warning - every 10 minutes update
    'forecast': {'dataType': 'flw', 'lang': 'en'}, # Weather Forecast - every hour update
}

REQUEST_TIMEOUT = 10


def _fetch_json(params: dict) -> dict | None:
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


def fetch_current_weather() -> dict:
    data = _fetch_json(ENDPOINTS['current_weather'])
    if not data:
        return {}

    update_time = _parse_hkt(data.get('updateTime', ''))

    humidity_block = data.get('humidity', {})
    humidity_data = humidity_block.get('data', [])
    hko_humidity = None
    for h in humidity_data:
        if h.get('place') == 'Hong Kong Observatory':
            hko_humidity = h.get('value')
            break

    temp_block = data.get('temperature', {})
    temp_record_time = _parse_hkt(temp_block.get('recordTime', ''))
    all_temps = temp_block.get('data', [])

    hko_temp = None
    district_temps = []
    for t in all_temps:
        entry = {
            'place': t.get('place', ''),
            'value': t.get('value'),
            'unit': t.get('unit', 'C'),
        }
        district_temps.append(entry)
        if t.get('place') == 'Hong Kong Observatory':
            hko_temp = t.get('value')

    rainfall_block = data.get('rainfall', {})
    rainfall_data = []
    for r in rainfall_block.get('data', []):
        rainfall_data.append({
            'place': r.get('place', ''),
            'max': r.get('max', 0),
            'min': r.get('min', 0),
            'unit': r.get('unit', 'mm'),
            'is_main': r.get('main') == 'TRUE',
        })

    icon_codes = data.get('icon', [])
    warning_messages = data.get('warningMessage', [])

    return {
        'update_time': update_time,
        'record_time': temp_record_time,
        'hko_temperature': hko_temp,
        'hko_humidity': hko_humidity,
        'district_temperatures': district_temps,
        'rainfall': rainfall_data,
        'icon_codes': icon_codes,
        'warning_messages': warning_messages,
    }


def fetch_warning_summary() -> list[dict]:
    data = _fetch_json(ENDPOINTS['warning_summary'])
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


def fetch_forecast() -> dict:
    data = _fetch_json(ENDPOINTS['forecast'])
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


def get_all_weather_data() -> dict:
    current = fetch_current_weather()
    warnings = fetch_warning_summary()
    forecast = fetch_forecast()

    return {
        'current_weather': current,
        'warnings': warnings,
        'forecast': forecast,
    }
