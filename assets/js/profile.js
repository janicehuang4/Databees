$ = jQuery = require("jquery");
loginModal = require("./requires/loginModal.js");


$(document).ready(function() {
    loginModal.init();
    $(".submitted").hide("fast")
    $(".fakeSubmit").on("click", function() {
    	$(".reviews").hide();
    	$(".submitted").show('fast');
    });
});
