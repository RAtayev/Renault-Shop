from django.shortcuts import render_to_response, render
from .models import Auto, Order
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64


import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.io as pio

# Create your views here.

def index(request):
    return render(
        request, 'index.html'
    )

def main(request):
    return JsonResponse(list(Auto.objects.values()), safe=False)

@csrf_exempt
def order(request):
    temp_order = Order.objects.create(auto=Auto.objects.get(name=request.POST.get('name')), date=request.POST.get('date'))
    return HttpResponse("Заказ №"+str(temp_order.id)+" успешно создан!")

def statistic(request):
    stat_arrX = []
    stat_arrY = []
    stat_arr_name = []
    orderSum = Order.objects.count()
    for i in range(orderSum):
        temp_date = Order.objects.all()[i].date
        stat_arrX.append(str(temp_date.month) + "/" + str(temp_date.year))
        stat_arrY.append(Order.objects.all()[i].auto.price)
        stat_arr_name.append(Order.objects.all()[i].auto.name)
    return JsonResponse(list([stat_arrX, stat_arrY, stat_arr_name]), safe=False)




