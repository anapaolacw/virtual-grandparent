$(document).ready(function(){
    var fontSize = parseInt($('body').css('font-size'),10);
    $('.inc').on('click',function(){
        fontSize+=2;
        $('body').css('font-size',fontSize+'px');
    })
    $('.dec').on('click',function(){
        fontSize-=2;
        $('body').css('font-size',fontSize+'px');
    })
})