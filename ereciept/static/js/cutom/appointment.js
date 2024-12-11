function handlePetExamination(pet_type,res_id){
    let url =`/examination/new?pet_type=${pet_type}&res_id=${res_id}` //"{% url 'pet_examination' %}"
    window.open(url, "", "width=1160,height=1000");
}
function openeditform(id,res_id="",pet_id=""){
    let url =""
    if (res_id != "undefined"){
        url =`/examination/edit_pet_examination?id=${id}&res_id=${res_id}` //"{% url 'pet_examination' %}"
    }else{
        url =`/examination/edit_pet_examination?id=${id}&pet_id=${pet_id}`
    }

    window.open(url, "", "width=1160,height=1000");
}
function calcchange(){
    let previous_weigth=document.getElementById("previos_weigth").value
    let current_weigth=document.getElementById("curent_weigth").value
    let change_percentage=document.getElementById("change")
    if(previous_weigth && current_weigth){
        let percent = ((current_weigth - previous_weigth)/previous_weigth)*100
        percent=percent.toFixed(2)
        change_percentage.value=percent + "%"
    }
}
function handlePetHistory(pet_type,res_id){
    let url =`/clinical_history?pet_type=${pet_type}&res_id=${res_id}`
     window.open(url, "", "width=1000,height=1000");
}

function CloseButton(){
    //window.close();
    //window.close()
     setTimeout(() => {
         window.close()
         window.opener.location.reload();
         }, 55);
	

}
function openhistoryeditform(id,res_id,pet_id){
    let url=""
    if(res_id !="undefined"){
        url =`/clinical_history/edit?id=${id}&res_id=${res_id}` //"{% url 'pet_examination' %}"
    }else{
        url =`/clinical_history/edit?id=${id}&pet_id=${pet_id}`
    }
    window.open(url, "", "width=1000,height=1000");
}

