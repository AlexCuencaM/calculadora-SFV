document.getElementById("pestana1").addEventListener("click",() => {pestanasTodas("0")});
document.getElementById("pestana2").addEventListener("click",function(){
	pestanasTodas("1");
});
document.getElementById("pestana3").addEventListener("click",function(){
	pestanasTodas("2");
});
document.getElementById("pestana4").addEventListener("click",function(){
	pestanasTodas("3");
});
document.getElementById("pestana5").addEventListener("click",function(){
	pestanasTodas("4");
});
const initParams = (methodtype) => {
return {
	method: methodtype,
	headers: new Headers(),
	mode: "cors",
	cache: "default"
}};
const request = (id = 0) =>{
	const base= "/home";
	const url=[`${base}/slider`, `${base}/info`,`${base}/implementacion`,
		`${base}/imagenes`,`${base}/contact`];

	return new Request(url[id],initParams("get"));
} 

const pestanasTodas = (id = 0) =>{
	fetch(request(id))
	.then((response) => response.text())	
	.then((response) => document.getElementById("pestanas").innerHTML=response)
}
pestanasTodas();