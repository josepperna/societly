$(document).ready(function(){ 
    var member = $('.subscribe').attr('data-member');
    if (member == "True"){
        $('.subscribe').hide();
        $('.unsubscribe').show(); 
    }else {
        $('.subscribe').show();
        $('.unsubscribe').hide(); 
    }
    $('.subscribe').click(function(){  
        society = $(this).attr("data-society"); 
        $.get('{% url 'subscribe' %}', {society: society}, function(){  
            $('.subscribe').toggle();
            $('.unsubscribe').toggle(); 
        }); 

    });
    $('.unsubscribe').click(function(){  
        society = $(this).attr("data-society"); 
        $.get('{% url 'unsubscribe' %}', {society: society}, function(){  
            $('.subscribe').toggle();
            $('.unsubscribe').toggle(); 
        }); 

    });
});