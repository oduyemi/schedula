(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });    


    
})(jQuery);

// $(document).ready(function () {
//     $("#livebox").on("input", function (e) {
//         var live_text = $(this).val();
//         $.ajax({
//             method: "POST",
//             url: "/livesearch",
//             data: { text: live_text },
//             success: function (rsp) {
//                 var data = "<ul>";
//                 $.each(rsp, function (index, value) {
//                     data += "<li style='list-style:none'>" + value.menu_item + "<li>";
//                 });
//                 data += "</ul>";
//                 $("#tasklist").html(data);
//             }
//         });
//     });


//     $("gettask").on("click", function (e) {
//       var choice = $("#choosetask").val();
//       $.ajax({
//           method: "POST",
//           url: "/search",
//           data: { text: choice },
//           success: function (rsp) {
//               var data = "<ul>";
//               $.each(rsp, function (index, value) {
//                   data += "<li style='list-style:none'>" + value.menu_item + "<li>";
//               });
//               data += "</ul>";
//               $("#task").html(data);
//           }
//       });
//   });
// });

