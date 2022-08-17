const notification=(titleText, text, type, confirmButtonText)=>{
    Swal.fire({
        titleText: titleText,
        text: text,
        type: type,
        confirmButtonText: confirmButtonText,
        confirmButtonColor: '#98c1d9',
    })
}
const confirmNotification=(text, confirmButtonText, confirmColor, redirectUrl)=>{
    Swal.fire({
        text:text,
        showCancelButton: true,
        confirmButtonText: confirmButtonText,
        confirmButtonColor: confirmColor,
        backdrop: true,
        showLoaderOnConfirm: true,
        preConfirm:()=>{
          location.href=redirectUrl;
        },
        allowOutsideClick:()=>false,
        allowEscapeKey:() =>false
      })
}
const errorNotification=(titleText, text, type, confirmButtonText)=>{
    Swal.fire({
        title: titleText,
        type: "warning",
        text: text,
        confirmButtonColor: '#98c1d9'
     });
}