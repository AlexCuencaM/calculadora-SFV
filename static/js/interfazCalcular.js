var posicion = 0;
let horarios = [];
async function mostrarFormularioCalcular() {		
	const url = "/calcular/";
	mostrarFormulario(url,"mostrar");	
}

//Método que llama a la función datos tabla para su posterior  inserción
function Equipo(id, descripcion, consumo = 0, cantidad = 1) {
	this.id = id;
	this.descripcion = descripcion;
	this.consumo = consumo;
	this.cantidad = cantidad;
}
const horarioDefault = (inicio = 1, fin = 24) => {	
	let horario =[];
	for(let i = inicio; i <= fin; i++)
		horario.push(i);	
	return horario;
};

async function anadir(id, descripcion) {	
	//nombre de la tabla html
	const tabla = document.getElementById("table-body");	
	//llama al método datosTabla la cual inserta los datos en la tabla	
	await datosTabla(new Equipo(id, descripcion), tabla);	
}

function checkbox(i){
	let input = document.createElement("input");
	input.value= i;
	input.type="checkbox";
	input.name="horas[]";
	input.className= "form-check-input";		
	return input;
}
function checking(array){
	let checks = document.getElementsByName("horas[]");	
	for(let i = 0; i<array.length;i++)
		checks[array[i] - 1].checked = true;		
}
function label(i){
	let l=document.createElement("label");
	l.innerHTML = i;
	l.className="form-check-label";
	return l;
}
function addcheckboxLabel(i,inicio=9,fin=19){	
	let div = document.createElement("div");
	div.className="form-check form-check-inline";
	div.appendChild(checkbox(i));
	div.appendChild(label(i));	
	return div;
}
//AQUI :D input.checked = true;
function addGroup(r){		
	//arrayPrincipal[obtener_fila].push(getArray());
	const obtener_fila = r.parentNode.parentNode.rowIndex - 1;
	posicion = obtener_fila;
	let div = document.querySelector(".modal-body.horario-js");
	div.innerHTML = "";
	//Sustituible	
	for(let i = 1; i <= 24; i++ )
		div.appendChild(addcheckboxLabel(i));	
	checking(horarios[obtener_fila]);		
}
const contentRow = (equipo) => [
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.cantidad}" min="0" name="cantidad[]"></td>`,		
	`<td><input type="text" class="form-control form-control-sm" value="${equipo.descripcion}" name="descripcion-producto[]"><input type="hidden" name="producto[]" value="${equipo.id}" id="tv"></td>`,
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.consumo}" step="0.01" min="0" name="consumo[]"></td>`,	
	`<td class="text-center">${button()}</td>`,
	`<td class="text-center"><button class="btn btn-outline-danger" name="eliminar[]" id="eliminar" onclick="eliminarFila(this)"><i class="fa fa-trash-o"></i></button></td>`
];

function getArray(){
	let checks = document.getElementsByName("horas[]");	
	let result = [];
		for(let i = 0; i<checks.length;i++)	
			if(checks[i].checked)
				result.push(Number(checks[i].value));
	return result;
}

const cerrar = () =>{
	$('#staticBackdrop').modal('hide');
}

const guardarHoras = () =>{
	horarios[posicion] = getArray();
	cerrar();	
}
const button = () => `<button class="btn btn-success" name="agregar[]" id="agregar" data-toggle="modal" data-target="#staticBackdrop" onclick="addGroup(this)"> <i class="fa fa-plus"></i> </button>`;
//Método que inserta los datos en la tabla
async function datosTabla(electrodomestico, tabla) {
	horarios.push(horarioDefault());
	const array = contentRow(electrodomestico);
	fila = tabla.insertRow(-1);
	//se añade una fila a la tabla
	fila.innerHTML = array.join(' ');
}
//Método de eliminar fila de la tabla
async function eliminarFila(r) {	
	/*Obtiene la fila que se va a eliminar*/
	const obtener_fila = r.parentNode.parentNode.rowIndex;		
	document.getElementById("tablaConsumo").deleteRow(obtener_fila);

}
//Cambiadisimo :V
//Llama desde el html
function validateModal(array,type="string"){
	floatCondition = (i) => type=="float" ? 
		!Number.isNaN(Number(i.value)): 
		Number.isInteger(Number(i.value)) && !Number.isNaN(Number(i.value));

	condition = (i) => type == "string" ? true : floatCondition(i) 	
	return [...array].every(i => i.value !== "" && condition(i));	
}
function allValidateModal(array_descripcion, array_cantidad, array_consumo){	
	return validateModal(array_descripcion) && validateModal(array_cantidad,"int") &&
		validateModal(array_consumo,"float")
}
async function obtenerAllDateTable() {
	const array_descripcion = document.getElementsByName("descripcion-producto[]");
	const array_id = document.getElementsByName("producto[]");			
	const array_cantidad = document.getElementsByName("cantidad[]");
	const array_consumo = document.getElementsByName("consumo[]");
	if(allValidateModal(array_descripcion,array_cantidad,array_consumo))
	{
		console.log(array_cantidad[0].value);		
		json = getJson(array_descripcion, array_id, horarios, array_cantidad,array_consumo);	
		enviarDatosPost(json);
		$('#exampleModal').modal('hide');		
		cleanData();
	}
	else alert("Ingrese datos de manera correcta :(");
}
function cleanData()
{
	horarios = [];
	posicion = 0;
}
function Result(id, descripcion, cantidad, consumoKwH, horarios) {
	this.id = id;
	this.descripcion = descripcion;
	this.cantidad = cantidad;
	this.consumoKwH = consumoKwH;
	this.horarios = horarios;
}

const getJson = (array_descripcion, array_id, array_horarios, array_cantidad,array_consumo) => {
	const json = {
		result: []
	}
	for (let i = 0; i < array_id.length; i++)
		json.result.push(new Result(array_id[i].value,
			array_descripcion[i].value,
			array_cantidad[i].value,
			array_consumo[i].value,
			array_horarios[i]));
	return json;
}

const enviarPost = (json) => {
	return {
		method: 'POST', // or 'PUT'
		body: JSON.stringify(json), // data can be `string` or {object}!
		headers: {
			'Content-Type': 'application/json'
		}
	}
}
const enviarDatosPost = (json) => {
	const url = "/consumo/";
	
	fetch(url, enviarPost(json))
		.then(response => response.json())		
		.catch(error => alert('Error:' + error))
		.then(response => {
			consumoDiario(response)
		});	
}

const consumoDiario = (responseText) => {	
	document.getElementById("valor_consumo").innerHTML = responseText.total + " KW/H";
	document.getElementById("consumoDiario").value = responseText.total;
}
