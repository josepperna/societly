$(document).ready(function(){ 
    if("{{ member }}"){
        $('.subscribe').hide();
        $('.unsubscribe').show(); 
    }else {
        $('.subscribe').show();
        $('.unsubscribe').hide(); 
    }
    $('.subscribe').click(function(){  
        society = $(this).attr("data-society"); 
        $.get('/subscribe/', {society: society}, function(){  
            $('.subscribe').toggle();
            $('.unsubscribe').toggle(); 
        }); 

    });
    $('.unsubscribe').click(function(){  
        society = $(this).attr("data-society"); 
        $.get('/unsubscribe/', {society: society}, function(){  
            $('.subscribe').toggle();
            $('.unsubscribe').toggle(); 
        }); 

    });
});