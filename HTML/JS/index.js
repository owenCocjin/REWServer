var counter=0;
function getExampleData(v_no){
	var xhttp=new XMLHttpRequest();
	xhttp.onreadystatechange=function(){
		//if readyState request is done and response is ready (4)
		//and the status was OK (200)
		if(this.readyState==4 && this.status==200){
			document.getElementById("tool_"+v_no).innerHTML+="<p>"+counter+"</p>";
			++counter;
			//Keep scroll bar on bottom
			var viewerscroll=document.getElementById("viewer_"+v_no)
			viewerscroll.scrollTop=viewerscroll.scrollHeight;
		}//if()
	}//function()
	xhttp.open("GET", "example_data.txt", true);  //'true' is whether it's async or not
	xhttp.send();
}//function()
