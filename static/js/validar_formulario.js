function validar(e){	
	const array=datosformulario();		
	const validar = array.every(value => value !== "");	
	if(!validar){
		e.preventDefault();
		alert("Todos los campos son obligatorios");
	}		
}

function form(){	
	const form = document.querySelector('#impl')	
	form.addEventListener('submit',validar);
}

function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}