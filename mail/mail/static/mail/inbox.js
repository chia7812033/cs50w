document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // When click send button, then send the mail
  document.querySelector('#compose-form').onsubmit = () => {
    send();
    load_mailbox('sent');
    return false;
  };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  get_mail(mailbox);
}

function send() {

  // Get the info from compose page
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // POST a request to send the mail
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });
}

function get_mail(mailbox) {

  // Get mails 
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      for (let i = 0; i < emails.length; i++) {

        // Create new div for each mail
        const top = document.createElement('div');
        top.classList.add("d-flex");
        top.style.border = "solid";

        const sender = document.createElement('div');
        sender.innerHTML = emails[i].sender;
        sender.setAttribute('id', 'email-sender');
        top.append(sender)

        const subject = document.createElement('div');
        subject.innerHTML = emails[i].subject;
        subject.setAttribute('id', 'email-subject');
        top.append(subject);

        const timestamp = document.createElement('div');
        timestamp.innerHTML = emails[i].timestamp;
        timestamp.setAttribute('id', 'email-time');
        top.append(timestamp)

        if (emails[i].read) {
          top.style.background = "gray";
        }
      
        document.querySelector('#emails-view').append(top);
      }

    });

}