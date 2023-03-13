// let counter = 0;
if (!localStorage.getItem('counter')){
    localStorage.setItem('counter',0);    
}

var counter = Number(localStorage.getItem('counter'));

function count(){

    //counter++;
    counter = counter + 1;
    document.querySelector('h1').innerHTML = counter;
    // if (counter % 10 === 0){
    //     alert(`Count is now ${counter}`);
    // }
    localStorage.setItem('counter',counter); 
}

document.addEventListener('DOMContentLoaded',function(){
    document.querySelector('h1').innerHTML = counter;
    document.querySelector('button').onclick = count;    
    setInterval(count,1000);

});