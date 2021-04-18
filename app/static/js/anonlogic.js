var socket;
            Notification.requestPermission().then(function(result) {});
            sessvars.$.debug()
            var isActive = true;
            function onBlur() {
                isActive = false;
            
            }
            function onFocus() {
                isActive = true;
            }
            if (false) {
                document.onfocusin = onFocus;
                document.onfocusout = onBlur;
            } else {
                window.onfocus = onFocus;
                window.onblur = onBlur;
            }

            function play() {
            var audio = new Audio("{{ url_for('static', filename='Sound_17216.mp3') }}");
            audio.play();
            }
            $(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
                socket.on('connect', function() {
                    socket.emit('joined', {});
                });
                socket.on('status', function(data) {
                    var div = document.getElementById("messages");

                    var div2 = document.createElement('div');
                    div2.classList.add("message", "info");
                    div.appendChild(div2);

                    var user_span = document.createElement('span');
                    user_span.classList.add("nick");
                    user_span.innerHTML =  "* | " + data.user; 
                    div2.appendChild(user_span)

                    var p_text = document.createElement('p');
                    p_text.classList.add("text");
                    p_text.innerHTML = data.msg;
                    div2.appendChild(p_text);

                });
                socket.on('message', function(data) {
                    var div = document.getElementById("messages");
                    

                    var div2 = document.createElement('div');
                    if(data.user === "{{ name }}" ){
                        div2.classList.add("me");
                    } else{
                        if (!document.getElementById('mutenot').checked) {
                            if(isActive === false){
                                play();
                            }
                        } 
                    }
                    div2.classList.add("message");
                    div.appendChild(div2);

                    var user_span = document.createElement('span');
                    user_span.classList.add("nick");
                    user_span.innerHTML =  data.user; 
                    div2.appendChild(user_span)

                    var p_text = document.createElement('p');
                    p_text.classList.add("text");
                    p_text.innerHTML = data.msg;
                    div2.appendChild(p_text);
                    
                    if(document.getElementById("AutoScroll").checked){
                        window.scrollTo(0,document.body.scrollHeight);
                    }
                });
                $('#text').keypress(function(e) {
                    var code = e.keyCode || e.which;
                    if (code == 13) {
                        text = $('#text').val();
                        $('#text').val('');
                        socket.emit('text', {msg: text});
                    }
                });
            });
            function leave_room() {
                socket.emit('left', {}, function() {
                    socket.disconnect();

                    window.location.href = "{{ url_for('main.index') }}";
                });
            }