$ = jQuery = require("jquery");
    bxSlider = require("bxslider-4");
    loginModal = require("./requires/loginModal.js");
    Morphext = require("Morphext");

var register, sliderCntrl;
var firstSlide = true;

//////////////////Page initializing (Visual)//////////////
$(document).ready(function() {
    loginModal.init();
  var sliderCntrl = $('.bxslider').bxSlider({
      auto: false,
      mode: 'fade',
      speed: 1500,
      controls: false,
      pagerCustom: ' ',
      onSliderLoad: function(currentIndex) {
        $(".content").css("visibility", "visible"); 
      }
      });
  $("#js-rotating").Morphext({
    // The [in] animation type. Refer to Animate.css for a list of available animations.
    animation: "fadeIn",
    // An array of phrases to rotate are created based on this separator. Change it if you wish to separate the phrases differently (e.g. So Simple | Very Doge | Much Wow | Such Cool).
    separator: ",",
    // The delay between the changing of each phrase in milliseconds.
    speed: 3500,
    complete: function () {
        if(sliderCntrl && !firstSlide) {
          sliderCntrl.goToNextSlide();
        }
        if(firstSlide) firstSlide = false;
    }
  });

  $("#aboutus").on("click", function() {
      $('html, body').animate({
        scrollTop: $(".second").offset().top
    }, 1000);
  });
});