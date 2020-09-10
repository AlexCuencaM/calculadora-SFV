var posicion = 0;
let horarios = [];
async function mostrarFormularioCalcular() {		
	const url = "/calcular/";
	mostrarFormulario(url,"mostrar");	
}

//Método que llama a la función datos tabla para su posterior  inserción
function Equipo(id, descripcion, consumo = 2.4, cantidad = 1) {
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
	`<td><input type="text" class="form-control form-control-sm" value="${equipo.descripcion}" name="descripcion-producto[]"><input type="hidden" name="producto[]" value="${equipo.id}" id="tv"></td>`,
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.consumo}" step="0.01" name="consumo[]"></td>`,
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.cantidad}" name="cantidad[]"></td>`,	
	// `<td><label class="form-control form-control-sm" name="consumo-total[]">${equipo.cantidad * equipo.consumo}</label></td>`,
	`<td class="text-center">${button()}</td>`,
	`<td class="text-center"><button class="btn btn-outline-danger" name="eliminar[]" id="eliminar" onclick="eliminarFila(this)"><i class="fa fa-trash-o"></i></button></td>`
];
const cerrar = () =>{
	$('#staticBackdrop').modal('hide');
}

function getArray(){
	let checks = document.getElementsByName("horas[]");	
	let result = [];
		for(let i = 0; i<checks.length;i++)	
			if(checks[i].checked)
				result.push(Number(checks[i].value));
	return result;
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
async function obtenerAllDateTable() {
	const array_descripcion = document.getElementsByName("descripcion-producto[]");
	const array_id = document.getElementsByName("producto[]");			
	const array_cantidad = document.getElementsByName("cantidad[]");
	const array_consumo = document.getElementsByName("consumo[]");	
	json = getJson(array_descripcion, array_id, horarios, array_cantidad,array_consumo);	
	enviarDatosPost(json);
	cleanData();
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
// {
// 	"result" : [
// 		{
// 			"id": 1,
// 			"descripcion": "mouse",
// 			"consumoKwH": 3.4
// 			"cantidad" : 3
// 			"horarios" : [
// 				1,2,3,4,5,6
// 			]
		
// 		},
// 	]
// }

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