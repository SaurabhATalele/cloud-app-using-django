var block = document.getElementById("up");
			function tog(x)
			{
			console.log("clicked...")
			up.style.display = "block";
			}

			function closer(x){
				up.style.display = "none";
			}
// *************************************************************************************************************************************
//the add page
			 function cancler(x){
            var db = document.getElementById("one");
            db.style.display = "none";
        }

        function showcreate(x){
            var db = document.getElementById("one");
            db.style.display = "grid";
        }

// *******************************************************************************************************************************

// show more options 
function showmore(x){
	var more = document.getElementById('more');
	more.style.display = "block";
}

// ***********************************************************************************************************************
function onFormSubmit(event) {
        event.preventDefault();

        var formData=new FormData();
        var f =document.getElementById("file");

        formData.append("file1",f.files[0]);


        console.log(formData);

        var xhr=new XMLHttpRequest();
        xhr.open("POST","http://192.168.1.6:8000/u/upload_file",true);
        xhr.upload.addEventListener("progress",function (ev) {
           if(ev.lengthComputable){
                 var percentage=(ev.loaded/ev.total*100|0);
               document.getElementById("progress_div").style["display"]="block";
               document.getElementById("container").style["display"]="block";
               document.getElementById("progress_bar").style["width"]=""+percentage+"%";
               document.getElementById("progress_bar").innerHTML=""+percentage+"%";
               document.getElementById("progress_text").innerHTML="Uploaded : "+parseInt(ev.loaded/1000000)+"/"+parseInt(ev.total/1000000)+" MB";
               console.log("Uploaded : "+ev.loaded);
               console.log("TOTAL : "+ev.total);

               console.log(percentage)
           }
        });
        xhr.send(formData);

    }

    /*******************************************************************************************************/

    function close_cont(x){
    var cont = document.getElementById('container');
    cont.style.display = 'none';
    }