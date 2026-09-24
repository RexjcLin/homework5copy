from django.shortcuts import render, redirect
from .models import temperature_db
from django.forms.models import model_to_dict
from django.http import HttpResponse

# Create your views here.
def view_history_temperature(request):
    history = temperature_db.objects.all().order_by('-myid')
    #return HttpResponse("test")
    return render(request, "views.view_history_temperature.html", {"history": history})

from django.http import JsonResponse
import django.views.decorators.csrf as csrf
@csrf.csrf_exempt
def add_temperature_API(request):
    if request.method not in ('GET', 'POST'):
        return JsonResponse({
            "status": "error",
            "message": "Only GET and POST requests are supported"
        }, status=405)

    data = request.GET if request.method == 'GET' else request.POST
    required_fields = ('sensor_id', 'temperature', 'humidity')
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return JsonResponse({
            "status": "error",
            "message": "Missing required fields",
            "missing_fields": missing_fields
        }, status=400)

    sensor_id = data['sensor_id']
    temperature = data['temperature']
    humidity = data['humidity']
    save_data = temperature_db(sensor_id=sensor_id, temperature=temperature, humidity=humidity)
    save_data.save()
    return JsonResponse({
            "status": "success",
            "sensor_id": sensor_id,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": save_data.timestamp
        })
def add_temperature(request):
    if request.method == 'POST':
        sensor_id = request.POST["sensor_id"]
        temperature = request.POST["temperature"]
        humidity = request.POST["humidity"]
        save_data = temperature_db(sensor_id=sensor_id, temperature=temperature, humidity=humidity)
        save_data.save()
        return redirect("view_history_temperature")
    return render(request, "add_temperature.html")
def show_temperature(request):
    temperatures = temperature_db.objects.all().order_by('-timestamp')
    return render(request, "show_temperature.html", {"data": model_to_dict(temperatures[0])}) if temperatures else HttpResponse("No temperatures found")
def show_temperature_API(request):
    temperatures = temperature_db.objects.all().order_by('-timestamp')[:1]
    if temperatures:
        #顯示包含時間的即時資料
        return JsonResponse({
            "status": "success",
            "data": list(temperatures.values())
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "No temperatures found"
        })
def show_temperature2(request):
    temperatures = temperature_db.objects.all().order_by('-timestamp')[:2]
    return render(request, "show_temperature2.html", {"data": list(temperatures.values())}) if temperatures else HttpResponse("No temperatures found")  