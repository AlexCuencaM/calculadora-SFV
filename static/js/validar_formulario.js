function validar(e){	
	const array=datosformulario();	
	const validate = value => value !== "";
	const validar = array.every(validate);	
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