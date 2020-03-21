/*Obtiene el selector*/	

function ligthBox(){
	var lightbox=document.querySelector(".gallery-lightbox")
	return lightbox
}


/*Funcion que add una palabra a una clase de una etiqueta*/

async function mostrarFormularioCalcular(){

	/*Le agrega a la etiqueta ligtbox show*/
	this.ligthBox().classList.add('show');

	/*Llama al metodo que muestra la pagina html BotonCalcular.html*/
	this.mostrarCalcular();
}

/*Funcion que delete una palabra a una clase de una etiqueta*/

async function cerrarFormularioCalcular(){
	/*Cierra la pantalla*/
	this.ligthBox().classList.remove('show');
}


/*Funcion mostrar el html*/
function mostrarCalcular(){
	var xhr=new XMLHttpRequest();
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
async function anadir(id,device){
	//electrodomestico de prueba
	var electrodomestico={id:id, tipo:device,tiempo:"24",cantidad:"0"}; 

	//nombre de la tabla html
	var nombreTabla=document.getElementById("tablaConsumo");

	//llama al método datosTabla la cual inserta los datos en la tabla
	datosTabla(electrodomestico,nombreTabla);

}

//Método que inserta los datos en la tabla
function datosTabla(electrodomestico,nombreTabla){		

	//se añade una fila a la tabla
	var fila=nombreTabla.insertRow(-1);
	var array_electrodomestico=document.getElementsByName("producto[]");
	// le asigna al objeto cell 3
	var cell=[fila.insertCell(0),fila.insertCell(1),fila.insertCell(2),fila.insertCell(3)];	
	console.log(array_electrodomestico.length);
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
	var obtener_fila=	r.parentNode.parentNode.rowIndex;
	/*elimina fila*/
	document.getElementById("tablaConsumo").deleteRow(obtener_fila);

}
function obtenerAllDateTable(){
	var array_descripcion=document.getElementsByName("descripcion-producto[]");
	var array_id=document.getElementsByName("producto[]");
	var array_tiempo=document.getElementsByName("tiempo[]");
	var array_cantidad=document.getElementsByName("cantidad[]");			
	var json ={
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

	console.log(json)
	enviarDatosPost(json);
	cerrarFormularioCalcular();
	
}
/*Funcion mostrar el html*/
function enviarDatosPost(json){	
	var xhr=new XMLHttpRequest();
	const url="/consumo/";
	xhr.open("POST",url,true);
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var sendJson = JSON.parse(xhr.responseText);	
			document.getElementById("valor_consumo").innerHTML=sendJson.total + " W";
			document.getElementById("consumoDiario").value=sendJson.total;
			console.log(document.getElementById("consumoDiario").value);
		}
	};	
	
	xhr.send(JSON.stringify(json));				
}
