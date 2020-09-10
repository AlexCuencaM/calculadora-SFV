const materialsDefault = () => [
	new Material("Cable solar 6mm color negro por metro",1),
	new Material("Cable solar 6mm color rojo por metro",1),
	new Material("Conector MC4 por par",1),
	new Material("Conectores MC4 Triple Grado A",1),	
	new Material("Conectores MC4 Dobles en Y",1),
	new Material("Estructura del panel",1),
];

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
			f();
		});
}
function f(){	
	const boton = document.getElementById("guardar_cerrar_2");
	boton.addEventListener("click",saveMaterials);
}
function form(){			
	const form = document.querySelector('#impl');	
	form.addEventListener('submit',validar);
	buttons();
	mostrarMateriales();
	defaultMaterial();	
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
function mostrarMateriales(){
	const materialesForm = document.getElementById("boton-materiales");
	materialesForm.addEventListener("click",(e)=>{
		mostrarFormulario("/materiales/","materiales-modal");		
	});	
}

function getMaterials(){
	return{
		descripcion : document.getElementsByName("descripcion-material[]"),
		cantidad : document.getElementsByName("cantidad-material[]"),
	}
}
const saveMaterials = () => {
	const materiales = getMaterials();		
	for(let i = 0; i < materiales.descripcion.length; i++ )
	{
		let descripcion = document.getElementById("descripcion-materials" + i);
		let cantidad = document.getElementById("cantidad-materials" + i);	

		descripcion.value = materiales.descripcion[i].value;
		cantidad.value = materiales.cantidad[i].value;
		
	}
}
function defaultMaterial(){
	const materiales = materialsDefault();
	modifyValues(materiales);
}
function modifyValues(materiales){
	for(let i = 0; i < materiales.length; i++ )
	{
		let descripcion = document.getElementById("descripcion-materials" + i);
		let cantidad = document.getElementById("cantidad-materials" + i);	

		descripcion.value = materiales[i].descripcion;
		cantidad.value = materiales[i].cantidad;
		
	}
	
}
function agregarMaterialesDefault(){
	const materiales = materialsDefault();
	
	let inputsMateriales = document.getElementsByName("descripcion-material[]");	
	let inputsCantidades = document.getElementsByName("cantidad-material[]");
	for(let i =0; i<inputsMateriales.length; i++)
	{
		inputsMateriales[i].value = materiales[i].descripcion;
		inputsCantidades[i].value = materiales[i].cantidad;
	}
		
	
}
function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}