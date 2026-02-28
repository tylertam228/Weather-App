from datetime import datetime, timezone, timedelta

from django.shortcuts import render

from .services import get_all_weather_data, SUPPORTED_LANGS

HKT = timezone(timedelta(hours=8))

UI_STRINGS = {
    'en': {
        'page_title': 'Hong Kong Weather',
        'subtitle': 'Data from Hong Kong Observatory',
        'location': 'Hong Kong',
        'warnings_title': 'Weather Warnings',
        'issued_at': 'Issued at',
        'current_title': 'Current Weather',
        'updated_at': 'Updated at',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'rainfall': 'Rainfall',
        'at_hko': 'at HK Observatory',
        'district_temps_title': 'Temperatures across Hong Kong',
        'forecast_title': 'Weather Forecast',
        'general_situation': 'General Situation',
        'outlook': 'Outlook',
        'show_all': 'Show all districts ▾',
        'show_less': 'Show less ▴',
        'switch_lang_label': '繁',
        'switch_lang_code': 'tc',
    },
    'tc': {
        'page_title': '香港天氣',
        'subtitle': '資料來自香港天文台',
        'location': '香港',
        'warnings_title': '天氣警告',
        'issued_at': '發出時間',
        'current_title': '即時天氣',
        'updated_at': '更新時間',
        'temperature': '氣溫',
        'humidity': '相對濕度',
        'rainfall': '雨量',
        'at_hko': '香港天文台',
        'district_temps_title': '各區氣溫',
        'forecast_title': '天氣預報',
        'general_situation': '天氣概況',
        'outlook': '展望',
        'show_all': '顯示所有地區 ▾',
        'show_less': '收起 ▴',
        'switch_lang_label': 'EN',
        'switch_lang_code': 'en',
    },
}

DATE_FORMATS = {
    'en': '%A, %d %B',
    'tc': '%Y年%m月%d日',
}


def _get_max_rainfall(rainfall_data: list[dict]) -> int:
    if not rainfall_data:
        return 0
    return max((r.get('max', 0) for r in rainfall_data), default=0)


def index(request, lang='en'):
    if lang not in SUPPORTED_LANGS:
        lang = 'en'

    weather_data = get_all_weather_data(lang)
    strings = UI_STRINGS.get(lang, UI_STRINGS['en'])
    now_hkt = datetime.now(HKT)

    current = weather_data.get('current_weather', {})

    context = {
        'current': current,
        'warnings': weather_data.get('warnings', []),
        'forecast': weather_data.get('forecast', {}),
        'lang': lang,
        'ui': strings,
        'today_date': now_hkt.strftime(DATE_FORMATS.get(lang, DATE_FORMATS['en'])),
        'max_rainfall': _get_max_rainfall(current.get('rainfall', [])),
    }
    return render(request, 'weather/weather.html', context)
