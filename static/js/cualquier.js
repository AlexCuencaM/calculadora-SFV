/*$('nav a').click(function(){	
	var b=$(this).attr('href');
	console.log(b);
});*/

document.getElementById("pestana1").addEventListener("click",function(){
	pestanasTodas("0");
});
document.getElementById("pestana2").addEventListener("click",function(){
	pestanasTodas("1");
});
document.getElementById("pestana3").addEventListener("click",function(){
	pestanasTodas("2");
});
document.getElementById("pestana4").addEventListener("click",function(){
	pestanasTodas("3");
});

	function pestanasTodas(id){
		const base= "/home";
		var xhr=new XMLHttpRequest();
		const url=[base + "/info",base + "/implementacion",
		base + "/imagenes",base + "/contact"];
		xhr.onreadystatechange=function(){			//mapear el estado de la solicitud
			if(this.readyState==4 && this.status==200)//4.respuesta a finalizado y response is ready 200ok(XMLHttpRequestObject)
			{
				console.log(this.responseText);
				document.getElementById("pestanas").innerHTML=this.responseText;
			}
		};
		// Open especifica la solicitud		
					xhr.open("GET",url[id],true);
					xhr.send();			
	}


	



