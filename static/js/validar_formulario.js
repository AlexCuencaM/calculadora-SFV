function validar(e){	
	const array=datosformulario();		
	const validar = array.every(value => value !== "");		
	if(!validar){
		e.preventDefault();
		alert("Todos los campos son obligatorios");
	}	
}
const descripcion = () =>{
	const resumen = "Soporta un perfil de carga";
	const otroResumen = "hasta una carga pico de";
	const resumenBattery = "Tiene una energía acumulada de";
	const consejo= "por lo que este banco son las necesarias para un sistema de 48V"
	return{
		bateria:{	
			id: "info-bateria",		
			descripcion:["NA",`${resumenBattery} 1500Wh`,`${resumenBattery} 3000Wh`,
			`${resumenBattery} 6000Wh, ${consejo}`]
		},

		inversor:{	
			id: "info-inversor",		
			descripcion:[
				`${resumen} pico de hasta 3kW`,
				`${resumen} mínimo de 3kW ${otroResumen} 5 kW.`,
				`${resumen} de 5.5 kW ${otroResumen} 10 kW`,
			]
		},
	}
}

async function mostrarFormulario(url,id) {				
	fetch(url, initParams())
		.then(response => response.text())		
		.catch(error => alert('Error:' + error))
		.then(response =>{
			document.getElementById(id).innerHTML = response;			
		});
}

function form(){			
	const form = document.querySelector('#impl');	
	const objeto = descripcion();
	form.addEventListener('submit',validar);
	buttons();

	$('[data-toggle="popover"]').popover();
	initPopover(objeto.inversor,"inversor");
	initPopover(objeto.bateria,"voltaje");
}
function initPopover(objeto,nombre){	
	const info = document.querySelector(`#${objeto.id}`);
	const select = document.getElementById(`${nombre}`);
	
	select.addEventListener("change",()=>{
		let title = select.value;
		if(nombre ==="voltaje")
		{
			title = `Batería de ${select.value}V 100Ah`
			if(select.value==48)
				title = `Batería de ${select.value}V 400Ah`
			if(select.value==0)
				title= "NA"
		}
		$(`#${objeto.id}`).attr("data-original-title",title );
		$(`#${objeto.id}`).attr("data-content",objeto.descripcion[select.selectedIndex]);		
	});	
}
function buttons(){
	const buttons = document.getElementsByClassName("preven");	
	for(let i=0; i<buttons.length; i++)
		buttons[i].addEventListener("click",(e) => e.preventDefault());
}

function datosformulario(){	
	return [
		document.getElementById("consumoDiario").value,		
		document.getElementById("autonomiaDias").value,
		document.getElementById("capacidad").value,
		document.getElementById("potenciadepanel").value,
	];
}