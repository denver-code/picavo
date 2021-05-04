eyeHideShow = (pass, repass = "") => {
    if ($(pass).attr("type") == "password") {
        $(".icon.eye").attr("src", "/static/img/icons/svg/eyeOff.svg");
        $(pass).attr("type", "text");
    } else {
        $(".icon.eye").attr("src", "/static/img/icons/svg/eye.svg");
        $(pass).attr("type", "password");
    }
    if (repass && $(repass).attr("type") == "password") {
        $(".icon.eye").attr("src", "/static/img/icons/svg/eyeOff.svg");
        $(repass).attr("type", "text");
    } else if (repass && $(repass).attr("type") == "text") {
        $(".icon.eye").attr("src", "/static/img/icons/svg/eye.svg");
        $(repass).attr("type", "password");
    }
    return false;
};
