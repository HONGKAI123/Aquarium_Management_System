//  function matchpassword(){                          //check if password match confirm password before form loading
//          var pw1 = document.getElementById("pswd1");     
//          var pw2 = document.getElementById("pswd2");  
//          if(pw1 != pw2)  
//          {   
//          alert("Passwords did not match");                  //alert if password not equal to confrim password
//           } else {  
//        alert("Password created successfully");  
//      }  
//         }
   
      function empty(){
        let userName = document.getElementById("user").value;
        let Password = document.getElementById("pswd1").value;
        let cfmpassword = document.getElementById("pswd2").value;
        let Email = document.getElementById("email1").value;
        let Phone = document.getElementById("phone1").value;

        if(userName !='' && Password !='' && cfmpassword !='' && Email !='' && Phone !='' && Password == cfmpassword){
          document.getElementById("submit1").removeAttribute("disabled")


        }
        else{

        }
      }