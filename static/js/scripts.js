function get_graph() {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/GraphSensors',
    });
}

function set_values() {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/SetValues', // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "value": document.getElementById("value").value,
            "name": document.getElementById("name").value,
            "check": Number(document.getElementById("check").checked)
            
        },        
    });
}
