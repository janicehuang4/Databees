$ = jQuery = require("jquery");
loginModal = require("./requires/loginModal.js");


$(document).ready(function() {
    loginModal.init();
});

$(document).ready(function () {
    $(".reservePrice, .currentBid, .bidEndDate, .itemPrice").hide("fast");
    $(".auction").on("click",function(){
    	$(".itemPrice").hide("slow"); 
    	$(".reservePrice").show("slow"); 
      $(".currentBid").show("slow");  
      $(".bidEndDate").show("slow"); 
    })  

    $(".buyItNow").on("click",function(){
      $(".itemPrice").show("slow"); 
      $(".reservePrice").hide("slow");
      $(".currentBid").hide("slow"); 
      $(".bidEndDate").hide("slow");
    })

});