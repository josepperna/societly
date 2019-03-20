$('#subscribe').click(function(){  
    society = $(this).attr("data-society"); 
    $.get('/subscribe/', {society: society}, function(){  
        $('#subscribe').hide();
        $('#unsubscribe').show(); 
    }); 
});