from django.db import connection
from django.http import JsonResponse

def sample_data(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT TOP 10 id, name, value FROM YourTable")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(rows, safe=False)
