document.getElementById("pestana1").addEventListener("click",() => {pestanasTodas("0")});
document.getElementById("pestana2").addEventListener("click",function(){
	pestanasTodas("1");
});
document.getElementById("pestana3").addEventListener("click",function(){
	pestanasTodas("2");
});
document.getElementById("pestana4").addEventListener("click",function(){
	pestanasTodas("3");
});
document.getElementById("pestana5").addEventListener("click",function(){
	pestanasTodas("4");
});

const pestanasTodas = (id = "0") => {
	const base= "/home";	
	const xhr=new XMLHttpRequest();
	const url=[`${base}/slider`, `${base}/info`,`${base}/implementacion`,
		`${base}/imagenes`,`${base}/contact`];
	xhr.onreadystatechange=function(){			//mapear el estado de la solicitud
		if(this.readyState==4 && this.status==200)//4.respuesta a finalizado y response is ready 200ok(XMLHttpRequestObject)				
			document.getElementById("pestanas").innerHTML=this.responseText;
		
	};
	// Open especifica la solicitud		
	xhr.open("GET",url[id],true);
	xhr.send();			
}
pestanasTodas();