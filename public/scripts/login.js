$(document).ready(function() {
    $(function() {
        var submitBtn = document.getElementById('form');
        $('form').submit(function(event){
            var email = $("#username").val();
            var password = $('#pwd').val();
            event.preventDefault();
            Data.logIn(email,password,function(resp){
                console.log(resp);
                if (resp.success == false){
                    console.log("invalid usrname");
                    alert("Invalid Password or Username");
                  }
                else{
                    window.location.href="index.html"
                }
            });     
        });

        function validateUsrname(){
            var usrname = document.getElementById('username');
            if(usrname.value === null || usrname.value === ""){
                document.getElementById("username-err").style.visibility = "none";
                return false
            }
            else{
                document.getElementById("username-err").style.visibility = "hidden";
                return true
            }
        }

        function validatePwd(){
            var pswd = document.getElementById('pwd');
            var pswdlen = pswd.value.length;
            if( pswdlen < 5 || pswdlen >20 ){
                document.getElementById("pwd-err").style.display = "block";
            }
            else{
                document.getElementById("pwd-err").style.display = "none";
            }
        }
        
        if (Data.isLoggedIn()) {
            location.href = 'index.html';
        }
    });
     
});


