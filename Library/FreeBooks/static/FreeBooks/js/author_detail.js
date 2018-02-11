var button_id=document.getElementById("follow-button");
button_id.onclick=function() {follow()	}
function follow(){
	if(button_id.innerHTML==="+ Follow"){
		button_id.innerHTML="Unfollow";
		button_id.style.backgroundColor="#3CB371";
		button_id.style.color=" 	#F5FFFA";
		button_id.style.borderColor="#3CB371"
	}
	else{
		button_id.innerHTML="+ Follow";
		button_id.style.backgroundColor="#ffffff";
		button_id.style.color="#3399FF";
		button_id.style.borderColor="#3399FF"
	}
}
