/*Obtiene el selector*/
/*Funcion que add una palabra a una clase de una etiqueta*/
const lightBox = () => document.querySelector(".gallery-lightbox");

async function mostrarFormularioCalcular() {
	/*Le agrega a la etiqueta ligtbox show*/
	lightBox().classList.add('show');
	/*Llama al metodo que muestra la pagina html BotonCalcular.html*/
	await this.mostrarCalcular();
}

/*Funcion que delete una palabra a una clase de una etiqueta*/
const cerrarFormularioCalcular = async () => lightBox().classList.remove('show');

/*Funcion mostrar el html*/
async function mostrarCalcular() {
	const xhr = new XMLHttpRequest();
	const url = "/calcular";
	xhr.onreadystatechange = function () {			//mapear el estado de la solicitud
		if (this.readyState == 4 && this.status == 200)//4.respuesta a finalizado y response is ready 200ok(XMLHttpRequestObject)			
			document.getElementById("mostrar").innerHTML = this.responseText;
	};
	// Open especifica la solicitud		
	xhr.open("GET", url, true);
	xhr.send();
}
//Método que llama a la función datos tabla para su posterior  inserción
function Electrodomestico(id, device, tiempo = 24, cantidad = 10) {
	this.id = id;
	this.tipo = device;
	this.tiempo = tiempo;
	this.cantidad = cantidad;
}

async function anadir(id, device) {
	//nombre de la tabla html
	const tabla = document.getElementById("tablaConsumo");
	//llama al método datosTabla la cual inserta los datos en la tabla	
	await datosTabla(new Electrodomestico(id, device), tabla);
}

const contentRow = (electrodomestico) => [
	'<div class="form-group"><td><input type="text" class="form-control form-control-sm" value="' + electrodomestico.tipo + '" name="descripcion-producto[]"><input type="hidden" name="producto[]" value="' + electrodomestico.id + '" id="tv">' + '</td>',
	'<td><input type="number" class="form-control form-control-sm" value="' + electrodomestico.tiempo + '" name="tiempo[]"></td>',
	'<td><input type="number" class="form-control form-control-sm" value="' + electrodomestico.cantidad + '" name="cantidad[]"></td>',
	'<td><input type="button" class="form-control form-control-sm btn btn-danger" value="Eliminar" name="eliminar[]" id="eliminar" onclick="eliminarFila(this)"></td>' + '</div>'
];
//Método que inserta los datos en la tabla
async function datosTabla(electrodomestico, tabla) {
	//se añade una fila a la tabla
	const fila = tabla.insertRow(-1);
	let cell = [];
	const array = contentRow(electrodomestico);
	for (let i = 0; i < array.length; i++) {
		cell.push(fila.insertCell(i));
		cell[i].innerHTML = array[i];
	}
}
//Método de eliminar fila de la tabla
async function eliminarFila(r) {
	/*Obtiene la fila que se va a eliminar*/
	const obtener_fila = r.parentNode.parentNode.rowIndex;
	/*elimina fila*/
	document.getElementById("tablaConsumo").deleteRow(obtener_fila);

}
//Llama desde el html
async function obtenerAllDateTable() {
	const array_descripcion = document.getElementsByName("descripcion-producto[]");
	const array_id = document.getElementsByName("producto[]");
	const array_tiempo = document.getElementsByName("tiempo[]");
	const array_cantidad = document.getElementsByName("cantidad[]");
	enviarDatosPost(getJson(array_descripcion, array_id, array_tiempo, array_cantidad));
	await cerrarFormularioCalcular();

}

function Result(id, descripcion, horas, watts) {
	this.id = id;
	this.descripcion = descripcion;
	this.horas = horas;
	this.watts = watts;
}

const getJson = (array_descripcion, array_id, array_tiempo, array_cantidad) => {
	const json = {
		result: []
	}
	for (let i = 0; i < array_tiempo.length; i++)
		json.result.push(new Result(array_id[i].value, array_descripcion[i].value,
			array_tiempo[i].value, array_cantidad[i].value))

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
		.then(response => consumoDiario(response));

}

const consumoDiario = (responseText) => {
	let sendJson = responseText;
	document.getElementById("valor_consumo").innerHTML = sendJson.total + " W";
	document.getElementById("consumoDiario").value = sendJson.total;
}