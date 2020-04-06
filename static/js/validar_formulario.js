function validar(){	
	const array=datosformulario();		
	for(let field of array){		
		if(field===""){
			alert("Todos los campos son obligatorios");
			return false;
		}
	}
	return true;
}

function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,
		document.getElementById("potenciadepanel").value,
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("voltaje").value,
	];
}