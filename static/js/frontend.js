/**
 * Created by kearailoe on 2014/08/17.
 */
// sending a csrftoken with every ajax request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

    function call_api(url, method, data, callback) {
        jQuery.ajax({
            url: '/api/v1/' + url,
            type: method,
            dataType: "application/json",
            data: JSON.stringify(data),
            processData: false,
            contentType: "application/json",
            complete: callback
        });
    };

function update_nav_cart_counter(){
    var counter=$("#nav-cart-counter");
    call_api('shopping_cart/','get',{},function(request){
        var response = JSON.parse(request.responseText);
        counter.text(response['meta']['total_count']);
    })
}