$ = jQuery = require("jquery");
loginModal = require("./requires/loginModal.js");


$(document).ready(function() {
    loginModal.init();
    $(".addCart").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            processData: false,
            contentType: false,
            data: $(".addCart").serialize(),
        }).done(function(response) {
        	console.log(response);
            if (response == "success") {
                $(".addCartButton").addClass("disabled");
                $(".addCartButton").html("Added");
            }
        });
    });
});
