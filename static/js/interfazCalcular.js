async function mostrarFormularioCalcular() {		
	const url = "/calcular/";
	
	fetch(url, initParams())
		.then(response => response.text())		
		.catch(error => alert('Error:' + error))
		.then(response => document.getElementById("mostrar").innerHTML = response);	
}

//Método que llama a la función datos tabla para su posterior  inserción
function Equipo(id, descripcion, consumo = 2.4, cantidad = 10) {
	this.id = id;
	this.descripcion = descripcion;
	this.consumo = consumo;
	this.cantidad = cantidad;
}

async function anadir(id, descripcion) {
	//nombre de la tabla html
	const tabla = document.getElementById("table-body");	
	//llama al método datosTabla la cual inserta los datos en la tabla	
	await datosTabla(new Equipo(id, descripcion), tabla);
}
const contentRow = (equipo) => [
	`<td><input type="text" class="form-control form-control-sm" value="${equipo.descripcion}" name="descripcion-producto[]"><input type="hidden" name="producto[]" value="${equipo.id}" id="tv"></td>`,
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.consumo}" step="0.01" name="consumo[]"></td>`,
	`<td><input type="number" class="form-control form-control-sm" value="${equipo.cantidad}" name="cantidad[]"></td>`,	
	`<td class="text-center"><button class="btn btn-outline-danger" name="eliminar[]" id="eliminar" onclick="eliminarFila(this)"><i class="fa fa-trash-o"></i></button></td>`
	
];
//Método que inserta los datos en la tabla
async function datosTabla(electrodomestico, tabla) {	
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
	const array_horarios =[1,2,4,5,6,12,24];				
	const array_cantidad = document.getElementsByName("cantidad[]");
	const array_consumo = document.getElementsByName("consumo[]");	
	json = getJson(array_descripcion, array_id, array_horarios, array_cantidad,array_consumo);	
	enviarDatosPost(json);

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
			array_horarios));
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
	document.getElementById("valor_consumo").innerHTML = responseText.total + " W";
	document.getElementById("consumoDiario").value = responseText.total;
}