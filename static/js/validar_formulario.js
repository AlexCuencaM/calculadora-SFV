
function validar(e){	
	const array=datosformulario();		
	const validar = array.every(value => value !== "");		
	if(!validar){
		e.preventDefault();
		alert("Todos los campos son obligatorios");
	}	
}
async function mostrarFormulario(url,id) {				
	fetch(url, initParams())
		.then(response => response.text())		
		.catch(error => alert('Error:' + error))
		.then(response =>{
			document.getElementById(id).innerHTML = response;			
		});
}

function form(){			
	const form = document.querySelector('#impl');	
	form.addEventListener('submit',validar);
	buttons();
}

function buttons(){
	const buttons = document.getElementsByClassName("preven");	
	for(let i=0; i<buttons.length; i++)
		buttons[i].addEventListener("click",(e) => e.preventDefault());
}

function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}