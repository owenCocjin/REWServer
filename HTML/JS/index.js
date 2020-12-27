//Javascript
// Author:  Owen Cocjin
// Version: 0.1
// Date:    2020.12.26
// Description:  Index's javascript
// Notes:
//    - Manages AJAX
function sendCommand(v_no){
	var xhttp=new XMLHttpRequest();
	var input_data=document.getElementById("input_"+v_no).value;
	var viewerscroll=document.getElementById("viewer_"+v_no);  //Makes sure scroll stays on bottom
	xhttp.onreadystatechange=function(){
		//if readyState request is done and response is ready (4)
		//and the status was OK (200)
		if(this.readyState==4 && this.status==200){
			if(this.responseText!="nocmd"){
				document.getElementById("tool_"+v_no).innerHTML+=this.responseText;
				//Keep scroll bar on bottom
				viewerscroll.scrollTop=viewerscroll.scrollHeight;
			}//if()
			else{
				console.log("[|X:index.js:No command was send!");
			}//else()
		}//if()
	}//function()
	//Send the data
	xhttp.open("POST", "AJAX/cts.bridge", true);  //'true' is whether it's async or not
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");  //Only needed for POST requests
	xhttp.send("viewer="+v_no+'&'+"command_data="+input_data);
}//function()
