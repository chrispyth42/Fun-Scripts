function getImg(){
    //Declares Array of file paths to images
    arr = ["./img/chikorita.png","./img/cyndaquil.png","./img/totodile.png"]

    //Selects a random path from the array
    image = arr[Math.floor(Math.random()*arr.length)];

    //Returns it to html div 'ib'
    document.getElementById('ib').innerHTML = ("<img src='" + image + "'>");
}