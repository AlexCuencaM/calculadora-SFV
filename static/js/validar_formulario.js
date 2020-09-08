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
			agregarMaterialesDefault();
		});
}
function form(){			
	const form = document.querySelector('#impl');
	form.addEventListener('submit',validar);
	buttons();
	mostrarMateriales();
}

function buttons(){
	const buttons = document.getElementsByClassName("preven");	
	for(let i=0; i<buttons.length; i++)
		buttons[i].addEventListener("click",(e) => e.preventDefault());
}

function Material(descripcion, cantidad = 1)
{
	this.descripcion = descripcion;
	this.cantidad = cantidad;
}

const materialsDefault = () => [new Material("Cable solar 6mm color negro por metro",1),
	new Material("Cable solar 6mm color rojo por metro",1),
	new Material("Conector MC4 por par",1),
	new Material("Conectores MC4 Triple Grado A",1),	
	new Material("Conectores MC4 Dobles en Y.",1),
	new Material("Estructura del panel",1),
];

function mostrarMateriales(){
	const materialesForm = document.getElementById("boton-materiales");
	materialesForm.addEventListener("click",(e)=>{		
		mostrarFormulario("/materiales/","materiales-modal");	
	});	
}

function agregarMaterialesDefault(){
	const materiales = materialsDefault();
	
	let inputsMateriales = document.getElementsByName("descripcion-material[]");
	console.log(inputsMateriales);
	for(let i =0; i<inputsMateriales.length; i++)
		inputsMateriales[i].value = materiales[i].descripcion;
	
}
function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}