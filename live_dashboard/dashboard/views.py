from django.db import connection
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden
import json
import os



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
            cursor.execute("SELECT TOP 10 id, first_name, last_name, date_of_birth, program FROM clients")
        else:
            cursor.execute("SELECT id, first_name, last_name, date_of_birth, program FROM clients LIMIT 10")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(rows, safe=False)

def gpd_clients(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, first_name, last_name, program
            FROM clients
            WHERE program = 'GPD'
        """)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(rows, safe=False)

@csrf_exempt
def run_query(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method is allowed.")

    try:
        data = json.loads(request.body)
        query = data.get('query')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not query or not isinstance(query, str):
        return HttpResponseBadRequest("Missing or invalid 'query'")

    # Only allow queries that start with SELECT
    lowered = query.strip().lower()
    if not lowered.startswith('select'):
        return HttpResponseBadRequest("Only read-only SELECT queries are allowed.")

    with connection.cursor() as cursor:
        try:
            # Log each allowed query to a file
            with open("query_log.txt", "a") as log:
                log.write(f"{query.strip()}\n")
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            return HttpResponseBadRequest(f"Query error: {str(e)}")

    return JsonResponse(rows, safe=False)
