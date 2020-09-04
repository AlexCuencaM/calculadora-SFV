for(let i = 0; i < 5; i++)
	document.getElementById(`pestana${i + 1}`).addEventListener("click", () => {
		pestanasTodas(i);
	});
const initParams = () => {
    return {
        method: "get",
        headers: new Headers(),
        mode: "cors",
        cache: "default",
    };
};
const request = (id = 0) => {
    const base = "/home";
    const url = [
        `${base}/slider`,
        `${base}/info`,
        `${base}/implementacion`,
        `${base}/imagenes`,
        `${base}/contact`,
    ];

    return new Request(url[id], initParams());
};

const pestanasTodas = (id = 0) => {
    
    fetch(request(id))
        .then((response) => response.text())
        .then((response) =>{
            document.getElementById("pestanas").innerHTML = response;
            if(id === 2) form();
            if(id===3) setInterval(nextCambiar,5000);          
        });    
};
pestanasTodas();
