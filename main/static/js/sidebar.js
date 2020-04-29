nav = $(".sidebar")[0];

nav.onmouseenter = function () {
    $(".sidebar").addClass("active");
}
nav.onmouseleave = function () {
    $(".sidebar").removeClass("active");
}

mobile_arrow = $("#arrow-mobile")[0];

console.log(mobile_arrow);

mobile_arrow.onclick = function () {
    arrow = $("#arrow-mobile")[0];
    nav = $("#mobile-nav");
    sidebar = $("#mobile-sidebar");
    panel = $("#panel");

    console.log(nav);
    console.log(sidebar);

    src = arrow.src;
    if (src.includes("down")) {
        nav.addClass("active");
        sidebar.addClass("open-sidebar-nav");
        panel.addClass("open-top-panel-phone");

        src = arrow.src;
        src = src.replace("down", "up");
        console.log(src);
        arrow.src = src;
        
    } else {
        nav.removeClass("active");
        sidebar.removeClass("open-sidebar-nav");
        panel.removeClass("open-top-panel-phone");
        src = arrow.src;
        src = src.replace("up", "down");
        console.log(src);
        arrow.src = src;
    }
}
