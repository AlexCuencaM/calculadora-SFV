function validar(){	
	var array=datosformulario();
	for(var i=0;i<array.length;i++){
		if(array[i]===""){
			alert("Todos los campos son obligatorios");
			return false;
		}
	}

}


function datosformulario(){
	var array,consumo,radiacion,potencia,autonomia,capacidad,voltaje;
	consumo=document.getElementById("valor_consumo").value;
	radiacion=document.getElementById("hsp").value;
	potencia=document.getElementById("potenciadepanel").value;
	autonomia=document.getElementById("autonomiaDias").value;
	capacidad=document.getElementById("capacidad").value;
	voltaje=document.getElementById("voltaje").value;
	array=[consumo,radiacion,potencia,autonomia,capacidad,voltaje];
	return array;
}