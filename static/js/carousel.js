var acumulador=1;
function nextCambiar(){	
	const imagenes=document.getElementById("imagenes");	
	if(imagenes == null)
		return;
	acumulador=acumulador+1;
	if(acumulador>=16){
		acumulador=1;
	}
	imagen(acumulador);
}

function backCambiar(){
	acumulador=acumulador-1;
	if(acumulador<=0){
		acumulador=16;
	}
	imagen(acumulador);
}

function imagen(acumulador){
	var imagen=document.getElementById("imagenes");	
	imagen.src="/static/img/Imagenes SFV/"+acumulador+".jpg";
}

setInterval(nextCambiar,5000);