<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <link rel="shortcut icon" href="assets/favicon.ico"/>
    <title>AIML 2.5 Web Test</title>
    <script src="assets/jquery.js" type="text/javascript"></script>
    <link rel="stylesheet" href="assets/main.css" type="text/css"/>


    <script type="text/javascript">
	var webServiceUrl = 'http://localhost:8080/cmd';
        $(document).ready(function () {
			                $.ajax({
                    type: "GET",
                    url: webServiceUrl,
                    data: {
                        userInput: 123456,
                    },
                    success: function (response) {
                        AddText('B ', response);
                        $('#fMessage').show();
                        $('input[name="userInput"]').focus();
                    },
                    error: function (request, status, error) {
                        alert('error');
						console.log('lll');
                        $('.userMessage').show();
                    }
                });

            // só um advinhador simples

            //console.log(webServiceUrl);
            $('.clean').click(function () {

                Clear();
                AddText('system ', 'cleaning...');

                $('.userMessage').hide();

				AddText('system ', 'Ok!');
				$('.userMessage').show();
            });


            $('#fMessage').submit(function () {

                // get user input
                var userInput = $('input[name="userInput"]').val();

                // basic check
                if (userInput == '')
                    return false;
                //

                // clear
                $('input[name="userInput"]').val('');

                // hide button
                $(this).hide();

                // show user input
                AddText('A ', userInput);
				// initialize config
				//AddText('A ', '到了这一步');
				console.log(webServiceUrl);
                $.ajax({
                    type: "GET",
                    url: webServiceUrl,
                    data: {
                        userInput: userInput,
                    },
                    success: function (response) {
                        console.log(webServiceUrl);
                        //console.log(response.message);
                        AddText('B ', response);
                        $('#fMessage').show();
                        $('input[name="userInput"]').focus();
                    },
                    error: function (request, status, error) {
                        console.log(error);
                        alert('error');
                        $('#fMessage').show();
                    }
                });

                return false;
            });

            function Clear() {
                $('.chatBox').html('');
            }

            function AddText(user, message) {
                console.log(user);
                console.log(message);
				var message_array=message.split('<br/>');
                var div = $('<div>');
                var name = $('<labe>').addClass('name');
                //var text = $('<span>').addClass('message');

                name.text(user + ':');
                

                div.append(name);
				  for(let index in message_array) {  
				  var message=message_array[index];
					var text= $('<span>').addClass('message');
					if (index != 0){
					text.css("margin-left","135px");}
					text.text(message);
					div.append(text);
					div.append($('<br>'));
						};
                $('.chatBox').append(div);

                $('.chatBox').scrollTop($(".chatBox").scrollTop() + 100);
            }


        });
    </script>
</head>
<body id="body">

<center>
    <div id="box1">
        <br>
        <br>
        <h2><a target="_blank" href="https://github.com/kompasim/chatbot-utf8">Chatbot</a></h2>
        <br>
        <br>
        <div class="chatBox" style="height: 372px;">
            welcome , i am chatbot ...
        </div>

        <div>
            <br>
            <a target="_blank" href="api.php?requestType=talk&userInput=ياخشىمۇسىز">api</a>
        </div>
    </div>
    <div id="box2" class="userMessage">
        <form id="fMessage">
            <input id="clean" type="button" class="clean" value="clean"/>
            <input type="text" name="userInput" id="userInput"/>
            <input id="send" type="submit" value="send" class="send"/>
        </form>
    </div>
</center>
</body>


</html>