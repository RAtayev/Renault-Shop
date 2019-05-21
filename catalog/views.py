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
        # stat_arrX.append("0"+str(i)+"/2019")
        # sum = 0
        # query_set = Order.objects.filter(date__month="0"+str(i), date__year="2019")
        # query_len = query_set.count()
        # for j in range(query_len):
        #     sum += query_set[j].auto.price
        # stat_arrY.append(sum)
    print(stat_arrX)
    print(stat_arrY)
    print(stat_arr_name)
    
    hist = go.Histogram(histfunc="sum", y=stat_arrY, x=stat_arrX, name="Выручка")
    data = go.Data([hist])
    layout=go.Layout(title='Статистика по продажам', xaxis={'title':'Месяц'}, yaxis={'title':'Выручка(BYN)'})
    fig=go.Figure(data=data,layout=layout)
    pio.write_image(fig, 'e:\\work\\js-tasks\\site\\autoshop\\autoshop\\catalog\\static\\statistic\\static_image.png')
    
    pie = go.Pie(labels=stat_arr_name)
    data1 = go.Data([pie])
    layout1 = go.Layout(title='Продаваемость авто')
    fig1 = go.Figure(data=data1,layout=layout1)
    pio.write_image(fig1, 'e:\\work\\js-tasks\\site\\autoshop\\autoshop\\catalog\\static\\statistic\\static_image1.png')

    return HttpResponse("Ok")




