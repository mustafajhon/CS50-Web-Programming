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


function toggle (value){

  
  if (value == true){
      return false;
  }
  else if( value == false){
      return true;
  }
  else{
      return null;
  }

}

function btnMarkText (value){
  if (value == false){
    return 'Mark As Read';
  }
  else{
    return 'Unmark As Read';
  }

}

function btnArchiveText (value){
  if (value == false){
    return ' Mark as archived';
  }
  else{
    return 'Unmark as archved';
  }

}




function add_header(){
  const email = document.createElement('div');
  email.className = 'email';
  email.innerHTML = `
    <div class="sender"><b>Sender</b></div>
    <div class="subject"><b>Subject</b></div>
    <div class="timestamp"><b>Timestamp</b></div>
  `;
  // Add email
  document.querySelector("#emails-view").append(email);
  
}

function add_email(contents){
  const email = document.createElement('div');
  email.className = 'email';
  email.innerHTML = `
      <div class="sender">${contents.sender}</div>
      <div class="subject">${contents.subject}</div>
      <div class="timestamp">${contents.timestamp}</div>
  `;
  if(contents.read == false){
    email.style.fontWeight="bold";
  }
  else{
    email.style.fontWeight="normal";
  }
  // Add email
  email.onclick = function(){
    
    emailsView = document.querySelector("#emails-view");
    while (emailsView.firstChild){
      emailsView.removeChild(emailsView.firstChild);
    }

    fetch("emails/" + contents.id,{method:"GET"})
    .then(response =>response.json())
    .then(show_email(contents))
  }
  document.querySelector("#emails-view").append(email);


  
}

function show_email(contents){
  
  // if e-mail was clicked - mark as read
  fetch('/emails/' + contents.id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // create main HTML e-mail elements 
  const email = document.createElement('div');
  const emailHeader= document.createElement('div');
  const emailText = document.createElement('div');
  email.className = 'singleEmail';
    
  // get all recipents 
  let recipents ='';
  contents.recipients.forEach(recipent =>{
    if (recipents !=""){
      recipents=recipents+", "+recipent;
    }
    else{
      recipents = recipent;
    }
  })

  // assign e-mail Header
  emailHeader.style.fontWeight="bold";

  const emailHeaderSender= document.createElement('div');
  const emailHeaderRecipents = document.createElement('div');
  const emailHeaderSubject = document.createElement('div');
  const emailHeaderTimestamp = document.createElement('div');

  emailHeaderSender.innerHTML = `From: ${contents.sender}`;
  emailHeaderRecipents.innerHTML = `To: ${contents.recipents}`;
  emailHeaderSubject.innerHTML = `Subject: ${contents.subject}`;
  emailHeaderTimestamp.innerHTML = `Timestamp: ${contents.timestamp}`;
  
  emailHeader.appendChild(emailHeaderSender,emailHeaderRecipents,emailHeaderSubject,emailHeaderTimestamp);

  // emailHeader.innerHTML =
  //     `<div><b>From: </b> ${contents.sender} </div>
  //     <div><b>To: </b>  ${recipents}</div>
  //     <div><b>Subject: </b>${contents.subject}</div>
  //     <div><b>Timestamp: </b>${contents.timestamp}</div>`;
  // assign e-mail text
  emailText.innerHTML=
  `<textarea class ="singleEmailTextArea" disabled> ${contents.body} </textarea>`
  
  console.log("I'm here2");
  // assign html code to e-mail class 
  email.innerHTML=
  emailHeader.innerHTML+ 
  `<div>
  <button class="btn btn-sm btn-outline-primary" id ="btn-Reply"> Reply </button>
  <button class="btn btn-sm btn-outline-primary" id ="btn-Mark"> ${btnMarkText(contents.read)} </button>
  <button class="btn btn-sm btn-outline-primary" id ="btn-Archive"> ${btnArchiveText(contents.archived)} </button>
  </div>`+
  emailText.innerHTML;
  document.querySelector("#emails-view").append(email);

  // 
  btnReply = document.querySelector("#btn-Reply");
  btnMark = document.querySelector("#btn-Mark");
  btnArchive = document.querySelector("#btn-Archive");
  

  console.log("I'm here");

  btnReply.onclick = function(){
    compose_email()
    // find all whitespaces in header except new line 
    const regex = /(?<=\n)(\s{2,})(?!\s)/g;
    const headerText =  emailHeader.innerText;
    let headerTextRegex = headerText.replaceAll(regex, "");
    // copy previous e-mails data: 
    document.querySelector('#compose-recipients').value = contents.sender;
    document.querySelector('#compose-subject').value = 'RE:' + contents.subject;
    document.querySelector('#compose-body').value = 
    "\r\n______________________________ \r\n"+
    headerTextRegex +"\n\n"  + emailText.innerText;
  }
  
  btnMark.onclick = function(){
    fetch('/emails/' + contents.id, {
      method: 'PUT',
      body: JSON.stringify({
          read: toggle(contents.read)
      })
    })
    load_mailbox('inbox');
  }

  btnArchive.onclick = function(){
    fetch('/emails/' + contents.id, {
      method: 'PUT',
      body: JSON.stringify({
         archived: toggle(contents.archived)
      })
    })
    load_mailbox('archive');
  }

}


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
    try{
      if (result.error) {
        console.log(result["error"]);
      }
    }
    catch{
      return 1;
    }

  })   



}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch("emails/" + mailbox,{method:"GET"})
  .then(
    response =>
      response.json()
    )
  .then(data =>{
    add_header();
    data.forEach(element => {
        add_email(element);
    });
  })

}