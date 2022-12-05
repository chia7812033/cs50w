document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email(sender="", subject="", body="") {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none'

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = body ? sender : "";
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

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
  document.querySelector('#email-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  get_mail(mailbox);
  // history.pushState({'mailbox': mailbox }, "", `${mailbox}`);
}

async function send() {

  // Get the info from compose page
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // POST a request to send the mail
  await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
}

function get_mail(mailbox) {

  // Get mails 
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      for (let i = 0; i < emails.length; i++) {

        // Create new div for each mail
        const top = document.createElement('div');
        top.setAttribute('id', 'cat');
        top.setAttribute('data-id', `${emails[i].id}`);
        top.classList.add("d-flex");
        top.style.border = "solid";
        top.addEventListener('click', event => {

          // Get the element been clicked
          let element = event.target;

          // If click on the archive button 
          if (element.nodeName === 'IMG' || element.nodeName === 'BUTTON') {
            archive(element);
          } else {
            // Go to the detail of the mail 
            check_mail(element);
          }
        });

        // Create section for sender
        const sender = document.createElement('div');
        sender.innerHTML = emails[i].sender;
        sender.setAttribute('id', 'email-sender');
        top.append(sender)

        // Create section for subject
        const subject = document.createElement('div');
        subject.innerHTML = emails[i].subject;
        subject.setAttribute('id', 'email-subject');
        top.append(subject);


        // Create section for timestamp
        const timestamp = document.createElement('div');
        timestamp.innerHTML = emails[i].timestamp;
        timestamp.setAttribute('id', 'email-time');
        top.append(timestamp)

        // If the mail is read then set it bg to gray
        if (emails[i].read) {
          top.style.background = "Gainsboro";
        }

        if (mailbox != 'sent') {
          // Add a archive button 
          const archive_btn = document.createElement('button');
          if (mailbox === 'archive') {
            archive_btn.innerHTML = '<img src="static/mail/unarchive.png" width="23" height="22"/>';
          } else {
            archive_btn.innerHTML = '<img src="static/mail/archive.png" width="30" height="30"/>';
          }
          archive_btn.style.border = 'none';
          top.append(archive_btn);
        }

        document.querySelector('#emails-view').append(top);
      }

    });

}

function check_mail(element) {

  // Get the element's id 
  let id = element.dataset.id;

  // If id is notdefined, means we get the child element
  if (!id) {
    // Get the parent element and its id 
    element = element.parentElement;
    id = element.dataset.id;
  }

  let mail;
  // Get the mail correspond to id 
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // fill each block of info
      mail = email;
      document.querySelector("#detail-subject").innerHTML = email.subject;
      document.querySelector("#detail-sender").innerHTML = email.sender;
      document.querySelector("#detail-timestamp").innerHTML = email.timestamp;
      document.querySelector("#detail-body").innerHTML = email.body;
    });

  // Set the mail to read 
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  // Show the mail's detail and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Handle event for click reply button
  document.querySelector('#detail-reply').addEventListener('click', function () {
    const body_start = "On " + mail.timestamp + " " + mail.sender + " wrote: \n" + mail.body;
    compose_email(mail.sender, "Re: " + mail.subject, body_start);
  })

}

async function archive(element) {

  // Get the parent
  let parent = element.parentElement;

  if (parent.nodeName === 'BUTTON') {
    parent = parent.parentElement;
  }

  // Get the id of the mail
  const id = parent.dataset.id;

  // Check the mail is already archived
  const response = await fetch(`/emails/${id}`)
  const email = await response.json()
  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: email.archived ? false : true
    })
  })
  // Reload to inbox
  load_mailbox('inbox');
}