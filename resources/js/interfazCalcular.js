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



//declaracion de variables
function anadir(){
		var electrodomestico={tipo:"televisor",tiempo:"70 W",cantidad:"100"}; //datos de prueba
		var nombreTabla=document.getElementById("tablaConsumo");//nombre de la tabla html
		datosTabla(electrodomestico,nombreTabla);

}


//insertar datos a tabla
function datosTabla(electrodomestico,nombreTabla){		
		var fila=nombreTabla.insertRow(0+1);
		var cell=[fila.insertCell(0),fila.insertCell(1),fila.insertCell(2),fila.insertCell(3)]
		cell[0].innerHTML='<td> '+electrodomestico.tipo+'<input type="hidden" name="producto[]" value="Producto"></td>';
		cell[1].innerHTML='<td><input type="text" value="'+electrodomestico.tiempo+'" name="tiempo[]"></td>';
		cell[2].innerHTML='<td><input type="text" value="'+electrodomestico.cantidad+'" name="cantidad[]"></td>';
		cell[3].innerHTML='<td><input type="button" value="Eliminar" name="eliminar[]"  id="eliminar" onclick="eliminarFila()"></td>';
}


//Eiminar
//

/*function eliminarFila(){
	alert("hola");
	//$(this).parent().parent().fadeOut("slow",function(){$(this).remove});
	var pre=getRowSelected(this);
	console.log(pre);

}
*/

/*
function getRowSelected(objectPressed){
	var a=objectPressed.parentNode.parentNode;
	var electrodomestico=a.getElementsByTagName("td")[0].getElementsByTagName("input")[0].innerHTML;
	var cantidad=a.getElementsByTagName("td")[1].getElementsByTagName("input")[0].innerHTML;
	var tiempo=a.getElementsByTagName("td")[2].getElementsByTagName("input")[0].innerHTML;
	var electrodomesticos=[electrodomestico,cantidad,tiempo];
	return electrodomesticos;

}*/





