var btn=document.querySelector('#i1')
var sidenav=document.querySelector('.sidenav')
var closebtn=document.querySelector('.i3')




btn.addEventListener('click',()=>{
   sidenav.style.width="250px";
   console.log("clocked");
})

closebtn.addEventListener('click',()=>{
    sidenav.style.width="0px";
    console.log("dfwd");
})


