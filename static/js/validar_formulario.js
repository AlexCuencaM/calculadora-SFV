function validar(){	
	var array=datosformulario();
	array.forEach(iterate);
	// for(var i=0;i<array.length;i++){
	// 	if(array[i]===""){
	// 		alert("Todos los campos son obligatorios");
	// 		return false;
	// 	}

	// }
}

function iterate(value,index,array){
	if(value === "")
	{
		alert("Todos los campos son obligatorios");
		return false	
	}
	
}

function datosformulario(){
	var array,consumo,radiacion,potencia,autonomia,capacidad,voltaje;
	consumo=document.getElementById("consumoDiario").value;	
	potencia=document.getElementById("potenciadepanel").value;
	autonomia=document.getElementById("autonomiaDias").value;
	capacidad=document.getElementById("capacidad").value;
	voltaje=document.getElementById("voltaje").value;	
	array=[consumo,radiacion,potencia,autonomia,capacidad,voltaje];
	return array;
}