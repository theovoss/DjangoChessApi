web: uvicorn config.asgi --log-file -
release: python manage.py migrate && python manage.py cleandata
