(function(){
  const form = document.querySelector('form');
  if(!form) return;

  form.addEventListener('submit', function(e){
    const prazoExp = document.getElementById('prazo_expiracao');
    const numero = document.getElementById('numero');
    const erros = [];

    if(prazoExp && prazoExp.value){
      const re = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/(\d{4})$/;
      if(!re.test(prazoExp.value)){
        erros.push('Prazo para expiração precisa estar no formato DD/MM/AAAA.');
      }
    }

    if(numero && numero.value && !/^\d+$/.test(numero.value)){
      erros.push('Número deve conter apenas dígitos.');
    }

    if(erros.length){
      e.preventDefault();
      alert(erros.join('\n'));
    }
  });
})();


