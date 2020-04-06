function validar(){	
	const array=datosformulario();	
	const validate = (value,index,array) => value !== "";
	const validar = array.every(validate);	
	if(!validar)	
		alert("Todos los campos son obligatorios");		
	return validar;	
}

function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}