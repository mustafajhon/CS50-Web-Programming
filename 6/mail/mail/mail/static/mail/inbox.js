document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#btn-send').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function add_email(contents){
  const email = document.createElement('div');
  email.className = 'email';
  email.innerHTML = `${contents}`;
  // Add email
  document.querySelector("#emails-view").append(email);
  
}

// function send_productId(data){
//   var request = new XMLHttpRequest();
//   request.open('POST', "{% url 'compose' %}", true);
//   request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
//   // const data = {
//   //   recipent: '{{ recipent}}',
//   //   subject:'{{ subject}}',
//   //   body: '{{ body}}',
//   // };
//   request.send(data);
// };

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(){
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients:  document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => {
    if (response.status ===400){
      return response.json();
    }
    else if (response.status ===201){
      load_mailbox('sent');
    }
  })

  .then(result => {
    if (result.error) {
      console.log(result["error"]);
    }
  })   



}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  //parse to json script to avoid XSS attack 
  //const value = JSON.parse(mailbox);
  //construct url 
  //var url = "{% url 'mail::emails' %}";

  fetch("emails/" + mailbox,{method:"GET"})
  .then(response => response.json())
  .then(data =>{
    data.forEach(element => {
      add_email(element);
    });
  })

}