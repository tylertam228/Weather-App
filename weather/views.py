from django.shortcuts import render

from .services import get_all_weather_data


def index(request):
    weather_data = get_all_weather_data()



    context = {
        'current': weather_data.get('current_weather', {}),
        'warnings': weather_data.get('warnings', []),
        'forecast': weather_data.get('forecast', {}),
    }
    return render(request, 'weather/weather.html', context)