var main = document.getElementById("main_content");
var statistic = document.getElementById("statistic_content");
var autosArr = [];
var orderId = 0;
var mapper = {"#/main/": mainPage, "#/statistic/": statisticPage, "#/order/": orderPage}

function mainPage(){
    loadAutos();
    document.getElementById("main").style.borderBottom = "0.5vh solid orange";
    document.getElementById("statistic").style.borderBottom = "none";
    statistic.style.display = "none";
    main.style.display = "";
}

function statisticPage(){
    loadStatistic();
    document.getElementById("main").style.borderBottom = "none";
    document.getElementById("statistic").style.borderBottom = "0.5vh solid orange";
    main.style.display = "none";
    statistic.style.display = "";
}

function fillOrder(tempAutoName){
    if(document.getElementById("orderAutoName"))
    {
        document.getElementById("orderAutoName").innerHTML = tempAutoName;
    }
    else{
        var orderForm = document.getElementsByClassName("b-popup-content")[0];
        let labelName = document.createElement('label');
        labelName.htmlFor = "orderAutoName";
        labelName.innerHTML = "Автомобиль: ";
        let labelDate = document.createElement('label');
        labelDate.htmlFor = "orderDate";
        labelDate.innerHTML = "Дата доставки:";
        let autoName = document.createElement('div');
        autoName.id = "orderAutoName";
        autoName.innerHTML = tempAutoName;
        let orderDate = document.createElement('input');
        orderDate.id = "orderDate";
        orderDate.type = "date";
        let tempDiv1 = document.createElement('div');
        tempDiv1.className = "labCont";
        let tempDiv2 = document.createElement('div');
        tempDiv2.className = "labCont";
        orderForm.insertBefore(tempDiv1, orderForm.children[1]);
        orderForm.insertBefore(tempDiv2, orderForm.children[1]);
        orderForm.children[1].appendChild(labelName);
        orderForm.children[1].appendChild(autoName);
        orderForm.children[2].appendChild(labelDate);
        orderForm.children[2].appendChild(orderDate);
    }
}

function orderPage(){
    if(orderId){
        let tempAuto = autosArr.find(element => {
            return ("order" + element["id"]) == orderId;
        })
        fillOrder(tempAuto["name"])
    }
    else fillOrder("Машина не выбрана");
    document.getElementsByClassName("b-popup")[0].style.display="";
    document.getElementsByClassName("b-popup-content")[0].style.display=""
}

function locationHashChanged(){
    (mapper[location.hash] || mainPage)();
}

function loadAutos(){
    let xhr = new XMLHttpRequest;
    xhr.open('GET', '/catalog/main');
    xhr.onload = function(){
        autosArr = JSON.parse(xhr.responseText);
        addAutos(autosArr);
    };
    xhr.send();
}

function loadStatistic(){
    let xhr = new XMLHttpRequest;
    xhr.open('GET', '/catalog/statistic')
    xhr.onload = function(){
        addStatistic(JSON.parse(xhr.responseText));
    }
    xhr.send();
}

document.getElementById("main").addEventListener("click", event => {
    location.hash = "#/main/";
})

document.getElementById("statistic").addEventListener("click", event => {
    location.hash = "#/statistic/";
})

window.onload = locationHashChanged;
window.onhashchange = locationHashChanged;

function addAutos(autosArray){
    if(document.getElementById("autos")){
        var autos = document.getElementById("autos");
        var autosCont = autos.parentElement;
        autosCont.removeChild(autos);
        var newauto = document.createElement('div');
        newauto.id = "autos";
        autosCont.appendChild(newauto);
    }
    autos = document.getElementById("autos");
    for(let i = 0; i < autosArray.length; i++)
    {
            let textCont = document.createElement('div');
            textCont.id = "textCont";
            let auto = document.createElement('div');
            auto.className = "auto";
            autos.appendChild(auto);
            let nameAuto = document.createElement('div');
            nameAuto.className = "nameAuto";
            nameAuto.id = "id " + autosArray[i]["name"];
            nameAuto.innerHTML = autosArray[i]["name"];
            let priceAuto = document.createElement('div');
            priceAuto.className = "priceAuto";
            priceAuto.innerHTML ="От " + autosArray[i]["price"] + "BYN";
            let autoImageContainer = document.createElement('div');
            autoImageContainer.className = "autoImageContainer";
            let autoImage = document.createElement('img');
            autoImage.id = "autoImage";
            let tempsrc = "/static/" + autosArray[i]["image"];
            autoImage.src = tempsrc;
            autoImage.alt = autosArray[i][Object.keys(autosArray[i])[1]];
            let orderAuto = document.createElement('button');
            orderAuto.className = "orderAuto";
            orderAuto.id = "order" + autosArray[i]["id"];
            orderAuto.innerHTML = "ЗАКАЗАТЬ";
            orderAuto.addEventListener('click', event => {
                orderId = event.target.id;
                location.hash = "#/order/"
            })
            let tempAuto = document.getElementsByClassName("auto");
            tempAuto[tempAuto.length - 1].appendChild(textCont);
            tempAuto[tempAuto.length - 1].childNodes[0].appendChild(nameAuto);
            tempAuto[tempAuto.length - 1].childNodes[0].appendChild(priceAuto);
            tempAuto[tempAuto.length - 1].appendChild(autoImageContainer);
            tempAuto[tempAuto.length - 1].childNodes[1].appendChild(autoImage);
            tempAuto[tempAuto.length - 1].appendChild(orderAuto);
    }
}

function addStatistic(tempArrayStat){
    var dataStat1 = [
        {
            x: tempArrayStat[0],
            y: tempArrayStat[1],
            type: 'bar',
        }
    ];
    var dataStat2 = [
        {
            labels: tempArrayStat[2],
            type: 'pie',
            hoverinfo: 'label+percent'
        }
    ];
    var layout1 = {
        xaxis: {
            title: 'Месяц'
        },
        yaxis: {
            title: 'Выручка,(BYN)'
        },
    };
    var layout2 = {
        showlegend: false,
    };
    Plotly.newPlot('statImage1', dataStat1, layout1, {responsive: true});
    Plotly.newPlot('statImage2', dataStat2, layout2, {responsive: true});
}

document.getElementById("orderButton").addEventListener("click", event => {
    var param1 = orderId.substring(5);
    var param2 = document.getElementById("orderDate").value;
    var params = 'id=' + encodeURIComponent(param1) + '&date=' + encodeURIComponent(param2);
    if(param2){
        let xhr = new XMLHttpRequest;
        xhr.open('Post', '/catalog/order/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function(){
            if(xhr.status == 404) document.getElementById('orderMade').innerHTML = "Ошибка (указанный автомобиль отсутствует в базе данных)"
            if(xhr.status == 200) document.getElementById('orderMade').innerHTML = "Заказ успешно совершен!"
            if(xhr.status == 500) document.getElementById('orderMade').innerHTML = "Ошибка сервера!"
            document.getElementsByClassName('b-popup-content')[0].style.display="none";
            document.getElementsByClassName('b-popup-order-response')[0].style.display="";
        }
        xhr.send(params);
    }
})

document.getElementsByClassName('b-popup')[0].addEventListener('click', event => {
    if(event.target === event.currentTarget){
    event.currentTarget.style.display="none";
    document.getElementsByClassName('b-popup-order-response')[0].style.display="none";
    location.hash="#/main/"
    }
})