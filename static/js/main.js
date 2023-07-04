let close =document.querySelector(".flash span");
let eye1=document.querySelector(".eye1");
let eye2=document.querySelector(".eye2");
let passwordField=document.querySelector("#password");

try{
    eye1.addEventListener('click',()=>{
        passwordField.type='password';
        eye1.style.visibility='hidden';
        eye2.style.visibility='visible';
    })
    eye2.addEventListener('click',()=>{
        passwordField.type='text';
        eye2.style.visibility='hidden';
        eye1.style.visibility='visible';
    })
}catch(err){

}

setTimeout(() => {
    try{
    document.querySelector('.flash').style.display='none';
    }catch(err){
        
    }
}, 5000);

try{
close.addEventListener('click',()=>{
    let flash=document.querySelector('.flash');
    flash.style.display='none';
})
}catch(err){

    
}