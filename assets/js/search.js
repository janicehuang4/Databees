$ = jQuery = require("jquery");
loginModal = require("./requires/loginModal.js");

function parseCurrentRequest(request) {
	tokens = request.split('&');
	if(tokens.indexOf("BuyItNow=on") > -1) {
		$("#BuyItNow").prop('checked', true);
	}
	if(tokens.indexOf("Auction=on") > -1) {
		$("#Auction").prop('checked', true);
	}
}

$.fn.pressEnter = function(fn) {  

    return this.each(function() {  
        $(this).bind('enterPress', fn);
        $(this).keyup(function(e){
            if(e.keyCode == 13)
            {
              $(this).trigger("enterPress");
            }
        })
    });  
 }; 

$(document).ready(function() {
    loginModal.init();
    var currentRequest = window.location.href.split("/");
    currentRequest = currentRequest[currentRequest.length-1];
    parseCurrentRequest(currentRequest);
    $("#BuyItNow, #Auction").on("click", function() {
    	$("#filter-form").submit();
    });
    $(".category").on("click", function(e) {
    	categoryName = $(this).context.innerText;
    	$("#categoryInput").val(categoryName);
    	$("#filter-form").submit();
    });
    $(".page").on("click", function() {
    	pageNumber = $(this).context.innerHTML;
    	$("#page").val(pageNumber);
    	$("#filter-form").submit();
    });
    $(".to, .from").pressEnter(function() {
    	$("#filter-form").submit();
    });
    $("#filter-form").submit(function(event) {
    	event.preventDefault();
    	getRequest = '?' + $("#search-form").serialize() + '&' + $("#filter-form").serialize();
    	window.location = getRequest;
    });
});