eyeHideShow = (pass, repass) => {
    $("body").on("click", ".icon", () => {
        if ($(pass).attr("type") == "password") {
            $(this).addClass("view");
            $(pass).attr("type", "text");
        } else {
            $(this).removeClass("view");
            $(pass).attr("type", "password");
        }
        return false;
    });
};
