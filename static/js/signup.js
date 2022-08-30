$(document).ready(function(){
  text = document.getElementById('typeOfUser').textContent;
  if(text == "helper"){
    document.getElementById("id_isHelper").checked = true;
  }
  $('#label_isHelper').on('click',function(){
    var checkbox = document.getElementById('id_isHelper')
    document.getElementById("id_isHelper").checked = !(checkbox.checked);
  })
});