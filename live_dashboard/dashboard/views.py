from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'dashboard/index.html')  # ✅ not HttpResponse!

def sample_data(request):
    data = [
        {"id": 1, "name": "Alpha", "value": 100},
        {"id": 2, "name": "Beta", "value": 200},
        {"id": 3, "name": "Gamma", "value": 300},
    ]
    return JsonResponse(data, safe=False)
