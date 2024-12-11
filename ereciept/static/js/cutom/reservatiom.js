function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function create_pet(){
        let id = document.getElementById("owner").value
        if (id){
            window.location.href=`/owner/edit_owner/${id}`
        }
    }
function add_atach(){
    console.log("add Attach")
}
function returnchange(){
    var amount =  document.getElementById('finde').value ; 
    var paid_amount = document.getElementById('paid_amount_pay').value ; 
    if (parseFloat(amount) > parseFloat(paid_amount)) {
        document.getElementById('paid_amount_pay').value = ' '
        document.getElementById('return_amount_pay').value= ' '
        alert('Value error !')

    }
    if (parseFloat(amount)< parseFloat(paid_amount)) {
        document.getElementById('return_amount_pay').value =  parseFloat(paid_amount) - parseFloat(amount)  
    }


}
function PaymentService(amount ,id ,lab_type,lab_name,owner){
    document.getElementById('owner_field').setAttribute('value', owner );
    document.getElementById('service_name').setAttribute('value', lab_name );
    document.getElementById('service_type_m').setAttribute('value', lab_type  );
    document.getElementById('finde').setAttribute('value', amount );
    document.getElementById('paid_amount_pay').setAttribute('value', amount );
    document.getElementById('service_id').setAttribute('value', id );
    document.getElementById('return_amount_pay').setAttribute('value', '0' );
    
    
}
function myFunction(amount, id) {
    document.getElementById("amount").setAttribute('value', amount);
    document.getElementById("spare_amount").setAttribute('value', amount);
    document.getElementById("hidentag").setAttribute('value', id)
    /// reset form
    let x = document.getElementById("paid_amount") //.setAttribute('value', "");
    x.value = amount
    document.getElementById("return_amount").setAttribute('value', "");
    Add_discount()
}
function handleonchange(e) {
    var paid_amount = document.getElementById("paid_amount").value
    var amount = document.getElementById("amount").value
    //  if(parseInt(paid_amount) > parseInt(amount)){
    //let diff= parseInt(paid_amount) - parseInt(amount)
    // document.getElementById("return_amount").setAttribute('value', diff);
    //  }

    if (parseInt(paid_amount) < parseInt(amount)) {
        document.getElementById("errorMessage").innerHTML = '<div class="alert alert-danger" role="alert"> Invalid Paid Amount</div>'
        document.getElementById('b-save').disabled = true;

    } else {
        let diff = parseInt(paid_amount) - parseInt(amount);
        document.getElementById("return_amount").setAttribute('value', diff);
        document.getElementById('b-save').disabled = false;
        document.getElementById("errorMessage").innerHTML = '<div class="alert alert-success" role="alert">   Valid </div>'
    }
}
function get_tax_rate(){
    var tax         = document.getElementById("tax").value
    var tax_rate    = document.getElementById('tax_amount')
    var total       = document.getElementById("price_from_db").value
    let amount      = document.getElementById("amount-id").value
   if (amount == 0){
       amount = 1 ;
   }
    $.ajax({
        type: "GET",
        url:  "/reservation/get_tax_rate",
        data: {'tax': tax },
    
    success : function(r) {
        if (r.rate   ) {
            tax_rate.value =  (parseFloat(r.rate) / 100 ) * (parseFloat(total) * parseFloat(amount) )
            document.getElementById("price").value =  (parseFloat(total)  *parseFloat(amount)) +parseFloat(tax_rate.value)  //((parseFloat(r.rate) / 100 ) * ((parseFloat(total) || 0 +parseFloat(amount))))
        }
        else{
         document.getElementById("price").value =  (parseFloat(total) * parseFloat(amount))

        }
    }
    })

}
function get_tax_rate_pay(){
    var tax = document.getElementById("tax_pay").value
    var tax_rate = document.getElementById('tax_amount_pay')
    var total = document.getElementById("finde").value
    $.ajax({
        type: "GET",
        url:  "/reservation/get_tax_rate",
        data: {'tax': tax },
    
    success : function(r) {
        if (r.rate) {
            tax_rate.value =  (parseFloat(r.rate) / 100 ) * parseFloat(total)
            document.getElementById("finde").value =  parseFloat(total)+  (parseFloat(r.rate) / 100 ) * parseFloat(total)
        }
    }
    })

}
function handlemodalclose() {
    document.getElementById("paid_amount").setAttribute('value', 0);
    document.getElementById("return_amount").setAttribute('value', 0);
}
function validation() {
    var price = document.getElementById('price').value
    var paid_amount = document.getElementById('paid_amount').value
    var save = document.getElementById('b-save')
    if (parseInt(paid_amount) < parseInt(price)) {
        document.getElementById("errorMessage").innerHTML = '<div class="alert alert-danger" role="alert"> Invalid Paid Amount</div>'
        document.getElementById('b-save').disabled = true;

    } else {
        document.getElementById('b-save').disabled = false;
        document.getElementById("errorMessage").innerHTML = '<div class="alert alert-success" role="alert">   Valid </div>'
    }
}
$(document).ready(function () {
    document.getElementById('owner').addEventListener('change', function () {
        var id = this.value
        let url = `/reservation/filtered-car/${id}`
        if (id == "new") {
            window.location = ""
        }
        $.get(url,function(res){
            let cars = res.cars
            let ss = document.getElementById("car")
            ss.innerHTML=""
            for (let i = 0; i < cars.length; i++) {
                    var option = document.createElement("option")
                    option.text = cars[i].description
                    option.value = cars[i].id
                    ss.append(option)
                }
        })
    });
});

function handlechange(val){
    let owner_id = document.getElementById("owner").value
    if(val=="new"){
        window.location.href=`/owner/edit_owner/${owner_id}`
    }
}
function craeteNew() {
    var value = document.getElementById('owner').value
    if (value == 'new') {
        window.location = "{% url 'create_owner' %}"

    }
}
function get_price(){
    var item = document.getElementById('service').value
    var data = {'item': item }
   
    $.ajax({
        type: "GET",
        url:  "/reservation/get_item_price",
        data: {'item': item },
    
    success : function(r) {
       
        if (r.price){
            var price = document.getElementById('price')
            var tax = document.getElementById('tax')
            let amount_div = document.getElementById("tax_amount")
            document.getElementById("price_from_db").value=r.price
            document.getElementById('tax').value = r.tax_rate
            price.value =r.price
            amount_div.value = r.tax_amount
            price.readonly = true
            // tax.readonly = false
        }else{
            price.readonly = false
        }
    }
    
    })

}
function select_type() {
    let ser_type = document.getElementById("service_type")
    $.ajax({
        url: `/reservation/filtered-types/${ser_type.value}`,
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            console.log("dataaaa",data)
            let ss = document.getElementById("service")
            ss.innerHTML = ""
            var option = document.createElement("option")
            ss.append(option)
            for (let i = 0; i < data.items.length; i++) {
                var option = document.createElement("option")
                option.text = data.items[i].name
                option.value = data.items[i].id
                ss.append(option)
            }
        }
    });
}

function select_service() {
    var val = document.getElementById(''.value)
}
function handleSearchButton() {
    let s_f = document.getElementById("search")

    $.ajax({
        type: "POST",
        url: "/reservation/reservation_search/",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            'search_f': s_f.value
        },
        success: function (data) {
            let res = document.getElementById("res_box")
            let html_str = '<h3 class="mb-3" style="text-align: right;color: black;">New Service</h3>' +
                '<div class="row p-2 m-2" style="border: 2px dashed black;color: white;border-radius: 7%">' +
                '<div class="plus" data-toggle="modal" data-target="#rmodal"></div>' +
                '</div>'
            for (let i = 0; i < data.res.length; i++) {
                html_str += '<div class="row p-2 m-2" style="border: 2px dashed black;color: white;border-radius: 7%">' +
                    '<div class="col-md-12">' +
                    `<div class="row"><span>Client Name : ${data.res[i].owner}</span> </div>` +
                    ` <div class="row"><span>Contac No : ${data.res[i].mobile}</span></div>` +
                    `<div class="row"><span>Email : ${data.res[i].email}</span></div>` +
                    ` <div class="row"><span>Pet Name : ${data.res[i].pet_name}</span></div>` +
                    `<div class="row"><span>Doctor : ${data.res[i].doctor}</span></div>` +
                    `<div class="row"><span>Price : ${data.res[i].price}</span></div>` +
                    `<div class="row"><span>Type : ${data.res[i].type}</span></div>` +
                    `<div class="row"><span>Service Name : ${data.res[i].service_name}</span></div>` +
                    `<button type="button" class="btn btn-danger" data-toggle="modal" data-target="#pmodal" onclick="myFunction(${data.res[i].price},${data.res[i].id})">Payment</button>` +
                    "</div></div>"

            }
            res.innerHTML = ""
            res.innerHTML = html_str
        }
    });
}


function find_owner(){
  
    var fnd = document.getElementById('find').value
    var owners= document.getElementById('owner')
    let url = "{% url 'get_owner' %}"
    var data = {'find': fnd}
    $.ajax({
        type: "GET",
        url:  "/reservation/get_owner",
        data: {
            'find': fnd
        },
        success: function (data) {
        

           
            if(data){
                owners.innerHTML=''
                var option = document.createElement("option")
                option.text = "______________"
                owners.append(option)
                for(var i = 0 ; i < data.data.length ; i ++){
                  
                    var option = document.createElement("option")
                    option.text = data.data[i].name
                    option.value = data.data[i].id
                    owners.append(option)

                }
            }
           
            var option = document.createElement("option")
            option.text = "+ Create New"
            option.value = "new"
            // option.innerHTML = ` <option value="new"  class="boldoption" style="background-color: brown;">+ Create New </option>     `
            owners.append(option)
        } })
}


function doctor_select_type() {
    let ser_type = document.getElementById("service_type")
    // var csrftoken = getCookie('csrftoken');
    let amount = document.getElementById("amount-div")
    if(ser_type.options[ser_type.selectedIndex].text == "BOARDING"){
        amount.removeAttribute("hidden")
    }else{
        amount.setAttribute("hidden","")
    }
    $.ajax({
        type: "POST",
        url: "/reservation/filtered_types/",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            'id': ser_type.value
        },
        success: function (data) {
            let ss = document.getElementById("service")
            ss.innerHTML = ""
        
            for (let i = 0; i < data.items.length; i++) {
                var option = document.createElement("option")
                option.text = data.items[i].name
                option.value = data.items[i].id
                ss.append(option)
            }
        }
    });
}

function doctor_select_types() {
    let ser_type = document.getElementById("service_type")
    let selected_text   =   ser_type.options[ser_type.selectedIndex].text
    if( selected_text =="EXAMINATION ROOM" || selected_text == "Surgery" ){
       let doctor   =  document.getElementById("doctor_id")
        doctor.style.display="block"
        doctor.required = true;
    }else{
        let doctor = document.getElementById("doctor_id")
        doctor.style.display="none"
        doctor.required = false;
    }
    $.ajax({
        type: "POST",
        url: "/reservation/filtered_types/",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            'id': ser_type.value
        },
        success: function (data) {
            let ss = document.getElementById("service")
            ss.innerHTML = ""

            for (let i = 0; i < data.items.length; i++) {
                var option = document.createElement("option")
                option.text = data.items[i].name
                option.value = data.items[i].id
                ss.append(option)
            }
        }
    });
}
function validatedate(){
    let date_value = new Date(document.getElementById("date").value)
    var now = new Date();
    date_value.setDate(date_value.getDate() + 1)
    if(now > date_value){
        alert("Invalid Date")
        document.getElementById("date").value=null
    }
}