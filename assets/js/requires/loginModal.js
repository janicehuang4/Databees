foundation = require("foundation");
csrfToken = require("./csrfToken.js");
var init = function() {
    var csrftoken = csrfToken.getCookie('csrftoken'),
        register = false;
    $(document).foundation();

    function revealLoginForm(callback) {
        $('#loginModal').foundation('reveal', 'open');
        register = false;
        $(".response").html("");
        $(".submit-button").val("Sign In");
        $(".switch").hide("fast");
        $(".firstName").hide("slow");
        $(".lastName").hide("slow");
        $(".signUpBlock").show();
        $(".signInBlock").hide();
        callback && callback();
    }

    function revealRegisterForm(callback) {
        register = true;
        $(".response").html("");
        $(".submit-button").val("Sign Up");
        $(".switch").show("fast");
        $(".firstName").show("slow");
        $(".lastName").show("slow");
        $(".signInBlock").show();
        $(".signUpBlock").hide();
        callback && callback();
    }

    $(".reveal-modal-bg").on("click", function() {
        $('[data-reveal]').foundation('reveal','close');
    });

    $("#loginCall").on("click", function() {
        revealLoginForm(function(){
            $('#loginModal').foundation('reveal', 'open');
        });
    });

    $(".sign.in").on("click", function() {
        revealLoginForm();
    });

    $("#registerCall").on("click", function() {
        revealRegisterForm(function(){
            $('#loginModal').foundation('reveal', 'open');
        });
    });

    $(".sign.up").on("click", function() {
        revealRegisterForm();
    });

    $(".auth").submit(function(event) {
        $(".response").html("");
        event.preventDefault();
        var urlPost;
        if (register) {
            urlPost = "/account/register/";
        } else {
            urlPost = "/account/login/";
        }
        $.ajax({
            url: urlPost,
            type: 'POST',
            data: $(".auth").serialize(),
            beforeSend: function(xhr, settings) {
                $(".subIcon").addClass("loading");
                $(".submit-button").addClass("disabled");
                $(".submit-button").prop("disabled", true);
                $(".submit-button").val("Loading...");
                if (!csrfToken.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        }).done(function(response) {
            $(".subIcon").removeClass("loading");
            $(".submit-button").removeClass("disabled");
            $(".submit-button").prop("disabled", false);
            $(".submit-button").val("Submit");
            if (response == "success") {
                $(".response").css("color", "#3fa565");
                if (register) {
                    $(".response").append("You are successfully registered. <br> Wait till page refreshes");
                } else {
                    $(".response").append("You are logged in. <br> Wait till page refreshes");
                }
                window.location = window.location;
            } else {
                $(".response").css("color", "#dd1e31");
                for (var key in response) {
                    if (response.hasOwnProperty(key)) {
                        $(".response").append(response[key]);
                    }
                }
            }
        }).fail(function(response) {
            $(".subIcon").removeClass("loading");
            $(".response").css("color", "#dd1e31");
            $(".response").html("Our server is not responding.");
            $(".submit-button").removeClass("disabled");
            $(".submit-button").prop("disabled", false);
            $(".submit-button").val("Submit");
        });;
    });
}

module.exports = {
    init: init
}
