
var acumulador=1;
function nextCambiar(){

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
	imagen.src="../img/Imagenes SFV/"+acumulador+".jpg";
}

setInterval('nextCambiar()',10000);