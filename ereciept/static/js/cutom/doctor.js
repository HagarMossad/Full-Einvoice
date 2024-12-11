function handleonchange(e) {
    var paid_amount = document.getElementById("paid_amount").value
    var amount = document.getElementById("amount").value


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