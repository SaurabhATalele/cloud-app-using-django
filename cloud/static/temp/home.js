// Variables__________________________________________








// ___________________________________________
//          context menu 
// ___________________________________________

document.onclick = hideall;
var name = "" ;

function showmen(event,namer) {
            window.name= namer;
            
            var menu = document.querySelector(".context-menu");
            var msg = document.querySelector(".msg");
            var renamer = document.querySelector(".renamer");
            var newname = document.querySelector(".newname");
			renamer.style.display = "none";
			msg.style.display = "none";

			event.preventDefault();
			menu.style.display = "block";


			menu.style.left = event.clientX+"px";
			menu.style.top = event.clientY+"px";
			return false;
		}

		function hiderenamer() {
            var renamer = document.querySelector(".renamer");
			renamer.style.display = "none";
					}

		function hideall() {
            var menu = document.querySelector(".context-menu");
            var msg = document.querySelector(".msg");
			
			menu.style.display = "none";
			msg.style.display = "none";

		}

		function showrename() {
 
			var renamer = document.querySelector(".renamer");
			var val = document.getElementById("newname");
			
            
			val.value = window.name;
			renamer.style.display = "block";
			// body...
		}

		function redren(event) {
			event.preventDefault();
            var msg = document.querySelector(".msg");
            var renamer = document.querySelector(".renamer");
			var newname = document.getElementById("newname").value;
			renamer.style.display = "none";
			msg.style.display = "block";
			 document.location.href = "rename/"+window.name+"/"+newname
			// body...
		}

        function deletefile(event){
            event.preventDefault();
           
            document.location.href =  "delete/"+window.name
        }

		function showconf(){
			var confirm = document.querySelector(".confirmation");
			confirm.style.display = "block";

		}

		function hideconf(){
			var confirm = document.querySelector(".confirmation");
			confirm.style.display = "none";

		}





        function showinfo(name,date,size){
            console.log(name)
            console.log("clicked");
        var inf = document.getElementById('Info');
        inf.style.display= 'flex';
        }
        
        function hideinfo(){
        var inf = document.getElementById('Info');
        inf.style.display= 'none';
        }
        