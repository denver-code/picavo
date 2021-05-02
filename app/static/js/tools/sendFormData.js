// Влад сказал что название modalkoOtpravlalkaFunc фигня нечитаемая, теперь это sendFormData
sendFormData = (fid) => {
    let data = $(fid).serialize();
    $.ajax({
        method: "POST",
        url: "#{url_for('.reset_password')}",
        data: data,
        success: (msg) => {
            if (fid === "#emailForm") {
                email = data.split(/\=/)[1];
                email = email.replace('%40', '@')
                $('#confirm p').append(email);
            }
            stepper.next();
            $('.toast-body').text(msg)
            var toastElList = [].slice.call(document.querySelectorAll('.toast'))
            var toastList = toastElList.map(function(toastEl) {
                return new bootstrap.Toast(toastEl,{
                    animation: true,
                    autohide: true,
                    delay: 5000
                })
            });
            toastList.forEach(toast => toast.show());
        },
        error: (msg) => {
            $('.toast-body').text(msg.responseText)
            var toastElList = [].slice.call(document.querySelectorAll('.toast'))
            var toastList = toastElList.map(function(toastEl) {
                return new bootstrap.Toast(toastEl,{
                    animation: true,
                    autohide: true,
                    delay: 5000
                })
            });
            toastList.forEach(toast => toast.show());
        },
    });
};
