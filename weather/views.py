from django.shortcuts import render

from .services import get_all_weather_data, SUPPORTED_LANGS

UI_STRINGS = {
    'en': {
        'page_title': 'Hong Kong Weather',
        'subtitle': 'Data from Hong Kong Observatory',
        'warnings_title': 'Weather Warnings',
        'issued_at': 'Issued at',
        'current_title': 'Current Weather',
        'updated_at': 'Updated at',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'at_hko': 'at HK Observatory',
        'district_temps_title': 'Temperatures across Hong Kong',
        'forecast_title': 'Weather Forecast',
        'general_situation': 'General Situation',
        'outlook': 'Outlook',
        'switch_lang_label': '繁體中文',
        'switch_lang_code': 'tc',
    },
    'tc': {
        'page_title': '香港天氣',
        'subtitle': '資料來自香港天文台',
        'warnings_title': '天氣警告',
        'issued_at': '發出時間',
        'current_title': '即時天氣',
        'updated_at': '更新時間',
        'temperature': '氣溫',
        'humidity': '相對濕度',
        'at_hko': '香港天文台',
        'district_temps_title': '各區氣溫',
        'forecast_title': '天氣預報',
        'general_situation': '天氣概況',
        'outlook': '展望',
        'switch_lang_label': 'English',
        'switch_lang_code': 'en',
    },
}


def index(request, lang='en'):
    if lang not in SUPPORTED_LANGS:
        lang = 'en'

    weather_data = get_all_weather_data(lang)
    strings = UI_STRINGS.get(lang, UI_STRINGS['en'])

    context = {
        'current': weather_data.get('current_weather', {}),
        'warnings': weather_data.get('warnings', []),
        'forecast': weather_data.get('forecast', {}),
        'lang': lang,
        'ui': strings,
    }
    return render(request, 'weather/weather.html', context)
