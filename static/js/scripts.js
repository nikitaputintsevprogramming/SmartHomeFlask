function set_values(addr) {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/'&zaddr, // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "value": document.getElementById("value").value,
            "name": document.getElementById("name").value,
            "check": Number(document.getElementById("check").checked)
        },        
    });
}
