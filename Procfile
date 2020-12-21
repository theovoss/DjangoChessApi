web: uvicorn config.asgi:application --port=$PORT
release: python manage.py migrate && python manage.py cleandata
