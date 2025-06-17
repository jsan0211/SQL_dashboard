from django.db import connection
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os

from django.http import HttpResponseForbidden

def debug_view(request):
    if not settings.DEBUG:
        return HttpResponseForbidden("This view is only available in development.")

    db_config = settings.DATABASES['default']
    return JsonResponse({
        "engine": db_config['ENGINE'],
        "name": str(db_config.get('NAME')),
        "host": db_config.get('HOST'),
        "driver": db_config.get('OPTIONS', {}).get('driver'),
        "env_secret_key_loaded": os.getenv('SECRET_KEY') is not None
    })



def home(request):
    return render(request, 'dashboard/index.html')


def sample_data(request):
    with connection.cursor() as cursor:
        if settings.DATABASES['default']['ENGINE'] == 'sql_server.pyodbc':
            cursor.execute("SELECT TOP 10 id, name, value FROM YourTable")
        else:
            cursor.execute("SELECT id, name, value FROM YourTable LIMIT 10")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(rows, safe=False)
