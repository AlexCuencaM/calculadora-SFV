document.getElementById("consumo").addEventListener("click",function(){
	calcular()});

	function calcular(){
		var xhr=new XMLHttpRequest();
		const url="../View/BotonCalcular.html";
		xhr.onreadystatechange=function(){			//mapear el estado de la solicitud
			if(this.readyState==4 && this.status==200)//4.respuesta a finalizado y response is ready 200ok(XMLHttpRequestObject)
			{
				console.log(this.responseText);
				document.getElementById("pestanas").innerHTML=this.responseText;
			}
		};
		// Open especifica la solicitud		
					xhr.open("GET",url,true);
					xhr.send();			
	}



//Método que llama a la función datos tabla para su posterior  inserción
function anadir(){
		//electrodomestico de prueba
		var electrodomestico={tipo:"televisor",tiempo:"70 W",cantidad:"100"}; 

		//nombre de la tabla html
		var nombreTabla=document.getElementById("tablaConsumo");

		//llama al método datosTabla la cual inserta los datos en la tabla
		datosTabla(electrodomestico,nombreTabla);

}


//Método que inserta los datos en la tabla
function datosTabla(electrodomestico,nombreTabla){		

		//se añade una fila a la tabla
		var fila=nombreTabla.insertRow(0+1);

		// le asigna al objeto cell 3
		var cell=[fila.insertCell(0),fila.insertCell(1),fila.insertCell(2),fila.insertCell(3)]

		//inserta en cada celda los atributos del objeto
		cell[0].innerHTML='<td> '+electrodomestico.tipo+'<input type="hidden" name="producto[]" value="Producto" id="tv"></td>';
		cell[1].innerHTML='<td><input type="text" value="'+electrodomestico.tiempo+'" name="tiempo[]"></td>';
		cell[2].innerHTML='<td><input type="text" value="'+electrodomestico.cantidad+'" name="cantidad[]"></td>';
		cell[3].innerHTML='<td><input type="button" value="Eliminar" name="eliminar[]"  id="eliminar" onclick="eliminarFila()"></td>';
}


//Método de eliminar fila de la tabla

function eliminarFila(){
	var fila_obt=getRowSelected();

	//Elimina el objecto la cual contiene toda la fila
	fila_obt.remove();

}


//Método de obtener fila de la tabla

function getRowSelected(){

	//Obtiene toda la fila 
	var obtener_fila=	document.getElementById("eliminar").parentNode.parentNode;

	return obtener_fila;
}





