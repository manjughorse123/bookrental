$(document).ready(function(){
    
 $('.test_slider').slick({
    infinite: true,
    slidesToShow: 1,
    dots: true,
    slidesToScroll: 1,
    autoplay: true,
    prevArrow: false,
    nextArrow: false,
    autoplaySpeed: 3000,
    responsive: [ 
            {  
              breakpoint: 681,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1
              }
            }
          ]
});    
    
// Carousal
$('.carousal').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        prevArrow: false,
        nextArrow: false, 
        responsive: [
                {
                  breakpoint: 1024,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                  }
                },
                {
                  breakpoint: 769, 
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },  
                {
                  breakpoint: 570,   
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
              ]
    }); 

});
