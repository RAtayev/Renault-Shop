from django.shortcuts import render_to_response, render
from .models import Auto, Order
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from collections import Counter
from django.shortcuts import get_object_or_404


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
    print(request.POST.get('id'))
    print(Auto.objects.get(id='1'))
    if(get_object_or_404(Auto, id=request.POST.get('id'))):
        temp_order = Order.objects.create(auto=Auto.objects.get(id=request.POST.get('id')), date=request.POST.get('date'))
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
    temp_prices = {}
    for i in range(len(stat_arrX)):
        temp_var = temp_prices.get(stat_arrX[i])
        if(temp_var):
            temp_prices.update({stat_arrX[i]: temp_var + stat_arrY[i]})
        else:
            temp_prices.update({stat_arrX[i]: stat_arrY[i]})
    final_stat_X = []
    final_stat_Y = []
    for i in sorted(temp_prices):
        final_stat_X.append(i)
        final_stat_Y.append(temp_prices.get(i))
    return JsonResponse(list([final_stat_X, final_stat_Y, stat_arr_name]), safe=False)




