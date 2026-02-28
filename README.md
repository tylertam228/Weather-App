# HK Weather

A real-time weather dashboard for Hong Kong, powered by the [Hong Kong Observatory](https://www.hko.gov.hk) Open Data API. Available in English and Traditional Chinese.

## Features

- **Live weather data** — temperature, humidity, and rainfall fetched directly from HKO API on every page load (no caching, always up-to-date)
- **27 district temperatures** — readings from all HKO weather stations across Hong Kong
- **Weather warnings** — active warning signals with issue time
- **Local forecast & outlook** — general situation, daily forecast, and multi-day outlook
- **Bilingual** — full English (`/`) and Traditional Chinese (`/tc/`) support, including API data
- **Responsive UI** — dark glassmorphism design that adapts from mobile (390px) to desktop (1200px+)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Django 6 |
| HTTP Client | Requests |
| WSGI Server | Gunicorn |
| Frontend | Django Templates, CSS (glassmorphism, CSS Grid, custom properties) |
| Data Source | [HKO Open Data API](https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf) |

## Quick Start

```bash
git clone <repo-url> && cd weatherapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) (English) or [http://127.0.0.1:8000/tc/](http://127.0.0.1:8000/tc/) (繁體中文).

## Data Freshness

All weather data is fetched from the HKO API in real time on each request. There is no local database or cache for weather data — every page load hits the HKO endpoints directly, so information is always as current as the Observatory provides:

| Data | HKO Update Frequency |
|------|---------------------|
| Current weather (temperature, humidity, rainfall) | Every hour |
| Weather warnings | Every 10 minutes |
| Local forecast | Every hour |

## Project Structure

```
weatherapp/
├── weather/
│   ├── services.py      # HKO API client & data parsing
│   ├── views.py          # View logic & i18n strings
│   ├── urls.py           # Route definitions
│   └── templates/weather/
│       └── weather.html  # Responsive dark-theme template
├── weatherapp/
│   ├── settings.py       # Django configuration
│   └── urls.py           # Root URL config
├── requirements.txt
└── manage.py
```

## Data Attribution

This project uses the **Hong Kong Observatory Open Data API**. All weather data displayed — including temperatures, humidity, rainfall, warnings, and forecasts — is provided by the [Hong Kong Observatory](https://www.hko.gov.hk), a department of the Government of the Hong Kong Special Administrative Region.

The HKO Open Data API is free to use and does not require an API key. Please refer to the [HKO Open Data API Documentation](https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf) and the [Terms and Conditions](https://data.weather.gov.hk/weatherAPI/doc/TermsAndConditions.pdf) for usage guidelines.

## License

MIT
