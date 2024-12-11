
   function queryParams() {
    var params = {}
    $('#toolbar').find('input[name]').each(function () {
      params[$(this).attr('name')] = $(this).val()
    })
    console.log(params)
    return params
  }
  function detailFormatter(index, row) {
    var html = []
    $.each(row, function (key, value) {
      html.push('<p><b>' + key + ':</b> ' + value + '</p>')
    })
    return html.join('')
  }

  function TableActions (value, row, index) {
    return [
        `<button class="btn btn-success" onclick="openeditform('${row.id}','${row.reservation_id}','${row.pet_id}')">`,
        'Open',
        '</button>',
        `<a class="btn btn-danger ml-2" href="/reservation/delete_clinical/${row.id}">`,
        'Delete',
        '</a>'
    ].join('');
}
 function ClinicalTableActions (value, row, index) {
    return [
        `<button class="btn btn-success" onclick="openhistoryeditform('${row.id}','${row.reservation_id}','${row.pet_id}')">`,
        'Open',
        '</button>',
        `<a class="btn btn-danger ml-2" href="/reservation/delete_patient_history/${row.id}">`,
        'Delete',
        '</a>'
    ].join('');
}

function buttons () {
    var pet_type    = document.getElementById("pet_type").value;
    var res_id      = document.getElementById("reservation_id").value;
    return {
        btnAdd: {
            text: 'Add new Owner',
            icon: 'fa-plus',
            event: ()=>handlePetExamination(pet_type,res_id),
        }
    }
}
function clinicalbuttons () {
    var pet_type    = document.getElementById("pet_type").value;
    var res_id      = document.getElementById("reservation_id").value;
    return {
        btnAdd: {
            text: 'Add new Owner',
            icon: 'fa-plus',
            event: ()=>handlePetHistory(pet_type,res_id),
        }
    }
}


