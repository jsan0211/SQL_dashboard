from django.db import connection
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os

def debug_view(request):
    db_config = settings.DATABASES['default']
    return JsonResponse({
        "engine": db_config['ENGINE'],
        "name": str(db_config.get('NAME')),  # 🔁 convert Path to string
        "host": db_config.get('HOST'),
        "driver": db_config.get('OPTIONS', {}).get('driver'),
        "env_secret_key_loaded": os.getenv('SECRET_KEY') is not None
    })


def home(request):
    return render(request, 'dashboard/index.html')


def sample_data(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT TOP 10 id, name, value FROM YourTable")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(rows, safe=False)
