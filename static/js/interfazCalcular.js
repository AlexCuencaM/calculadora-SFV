/*document.getElementById("consumo").addEventListener("click",function(){
	calcular()});*/

/*Obtiene el selector*/	

function ligthBox(){
	var lightbox=document.querySelector(".gallery-lightbox")
	return lightbox
}


/*Funcion que add una palabra a una clase de una etiqueta*/

function mostrarFormularioCalcular(){

	/*Le agrega a la etiqueta ligtbox show*/
	this.ligthBox().classList.add('show');

	/*Llama al metodo que muestra la pagina html BotonCalcular.html*/
	this.mostrarCalcular();
}

/*Funcion que delete una palabra a una clase de una etiqueta*/

function cerrarFormularioCalcular(){
	/*Cierra la pantalla*/
	this.ligthBox().classList.remove('show');
}


/*Funcion mostrar el html*/
function mostrarCalcular(){
	var xhr=new XMLHttpRequest();
	const url="/calcular/";
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
function anadir(id,device){
	//electrodomestico de prueba
	var electrodomestico={id:id, tipo:device,tiempo:"70",cantidad:"100"}; 

	//nombre de la tabla html
	var nombreTabla=document.getElementById("tablaConsumo");

	//llama al método datosTabla la cual inserta los datos en la tabla
	datosTabla(electrodomestico,nombreTabla);

}

//Método que inserta los datos en la tabla
function datosTabla(electrodomestico,nombreTabla){		

	//se añade una fila a la tabla
	var fila=nombreTabla.insertRow(1);
	var array_electrodomestico=document.getElementsByName("producto[]");
	// le asigna al objeto cell 3
	var cell=[fila.insertCell(0),fila.insertCell(1),fila.insertCell(2),fila.insertCell(3)];	
	console.log(array_electrodomestico.length);
	/*registro de practica*/
	if(array_electrodomestico.length%2==0){
	//inserta en cada celda los atributos del objeto
	cell[0].innerHTML='<td><label> '+electrodomestico.tipo+'<input type="hidden" name="producto[]" value="'+electrodomestico.id+'" id="tv"></label></td>';
	cell[1].innerHTML='<td><input type="text" value="'+electrodomestico.tiempo+'" name="tiempo[]"></td>';
	cell[2].innerHTML='<td><input type="text" value="'+electrodomestico.cantidad+'" name="cantidad[]"></td>';
	cell[3].innerHTML='<td><input type="button" value="Eliminar" name="eliminar[]"  id="eliminar" onclick="eliminarFila(this)"></td>';
	}
	else{
		cell[0].innerHTML='<td><label> '+electrodomestico.tipo+'<input type="hidden" name="producto[]" value="'+electrodomestico.id+'" id="tv"></label></td>';
	cell[1].innerHTML='<td><input type="text" value="'+'20'+'" name="tiempo[]"></td>';
	cell[2].innerHTML='<td><input type="text" value="'+'30'+'" name="cantidad[]"></td>';
	cell[3].innerHTML='<td><input type="button" value="Eliminar" name="eliminar[]"  id="eliminar" onclick="eliminarFila(this)"></td>';
	}

}


//Método de eliminar fila de la tabla
function eliminarFila(r){
	/*Obtiene la fila que se va a eliminar*/
	var obtener_fila=	r.parentNode.parentNode.rowIndex;
	/*elimina fila*/
	document.getElementById("tablaConsumo").deleteRow(obtener_fila);

}


function obtenerAllDateTable(){
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
			horas:array_tiempo[i].value,
			watts:array_cantidad[i].value
		})
	}	

	console.log(json)
	enviarDatosPost(json);
	cerrarFormularioCalcular();
	
}
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

/*Funcion mostrar el html*/
function enviarDatosPost(json){
	var csrftoken = getCookie('csrftoken');	
	var xsrfHeaderName = getCookie("X-CSRFToken")
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
