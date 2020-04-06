/*Obtiene el selector*/	

/*Funcion que add una palabra a una clase de una etiqueta*/
const lightBox = () => document.querySelector(".gallery-lightbox");

async function mostrarFormularioCalcular(){
	/*Le agrega a la etiqueta ligtbox show*/
	lightBox().classList.add('show');
	/*Llama al metodo que muestra la pagina html BotonCalcular.html*/
	await this.mostrarCalcular();
}

/*Funcion que delete una palabra a una clase de una etiqueta*/

const cerrarFormularioCalcular = () => lightBox().classList.remove('show');

/*Funcion mostrar el html*/
async function mostrarCalcular(){
	let xhr=new XMLHttpRequest();
	const url="/calcular";
	xhr.onreadystatechange=function(){			//mapear el estado de la solicitud
		if(this.readyState==4 && this.status==200)//4.respuesta a finalizado y response is ready 200ok(XMLHttpRequestObject)
		{
			console.log(this.responseText);
			document.getElementById("mostrar").innerHTML=this.responseText;
		}
	};
	// Open especifica la solicitud		
	xhr.open("GET",url,true);
	xhr.send();			
}
//Método que llama a la función datos tabla para su posterior  inserción
function Electrodomestico (id,device,tiempo=24,cantidad=10){
	this.id = id;
	this.tipo = device;
	this.tiempo = tiempo;
	this.cantidad = cantidad;
}

async function anadir(id,device){		
	//nombre de la tabla html
	const nombreTabla=document.getElementById("tablaConsumo");
	//llama al método datosTabla la cual inserta los datos en la tabla
	await datosTabla(new Electrodomestico(id,device),nombreTabla);
}

//Método que inserta los datos en la tabla
async function datosTabla(electrodomestico,nombreTabla){		

	//se añade una fila a la tabla
	const fila=nombreTabla.insertRow(-1);	
	// le asigna al objeto cell 3
	let cell=[fila.insertCell(0),fila.insertCell(1),fila.insertCell(2),fila.insertCell(3)];		
	/*registro de practica*/	
	//inserta en cada celda los atributos del objeto
	cell[0].innerHTML='<div class="form-group"><td><input type="text" class="form-control form-control-sm" value="'+electrodomestico.tipo+'" name="descripcion-producto[]"><input type="hidden" name="producto[]" value="'+electrodomestico.id+'" id="tv">'+'</td>';
	cell[1].innerHTML='<td><input type="number" class="form-control form-control-sm" value="'+electrodomestico.tiempo+'" name="tiempo[]"></td>';
	cell[2].innerHTML='<td><input type="number" class="form-control form-control-sm" value="'+electrodomestico.cantidad+'" name="cantidad[]"></td>';
	cell[3].innerHTML='<td><input type="button" class="form-control form-control-sm btn btn-danger" value="Eliminar" name="eliminar[]"  id="eliminar" onclick="eliminarFila(this)"></td></div>';	

}
//Método de eliminar fila de la tabla
async function eliminarFila(r){
	/*Obtiene la fila que se va a eliminar*/
	const obtener_fila=r.parentNode.parentNode.rowIndex;
	/*elimina fila*/
	document.getElementById("tablaConsumo").deleteRow(obtener_fila);

}
//Llama desde el html
function obtenerAllDateTable(){	
	const array_descripcion=document.getElementsByName("descripcion-producto[]");
	const array_id=document.getElementsByName("producto[]");
	const array_tiempo=document.getElementsByName("tiempo[]");
	const array_cantidad=document.getElementsByName("cantidad[]");			
	enviarDatosPost(getJson(array_descripcion,array_id,array_tiempo,array_cantidad));
	cerrarFormularioCalcular();
	
}


const getJson = (array_descripcion,array_id,array_tiempo,array_cantidad) =>{	
	const json ={
		result:[			
		]
	}
	for(var i = 0; i<array_tiempo.length; i++)
	{
		json.result.push({
			id:array_id[i].value,//Suministrado
			descripcion:array_descripcion[i].value,
			horas:array_tiempo[i].value,
			watts:array_cantidad[i].value
		})
	}
	return json;
}

/*Funcion mostrar el html*/
function enviarDatosPost(json){	
	const xhr=new XMLHttpRequest();
	const url="/consumo/";
	xhr.open("POST",url,true);
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200)
			consumoDiario(xhr.responseText);		
	};	
	
	xhr.send(JSON.stringify(json));				
}
const consumoDiario = (responseText) =>{
	let sendJson = JSON.parse(responseText);
	document.getElementById("valor_consumo").innerHTML=sendJson.total + " W";
	document.getElementById("consumoDiario").value=sendJson.total;			
}