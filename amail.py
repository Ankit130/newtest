import imaplib, email

user = 'test@nextdoorlocksmith.com'
password = 'Ab123456'
imap_url = 'secure.emailsrvr.com'
port=993

def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True) 

def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data

def get_emails(result_bytes): 
    msgs = [] # all the email data are pushed inside an array 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        msgs.append(data) 
  
    return msgs 

con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)
con.select('Inbox')
msgs = get_emails(search('FROM', 'ankitmaheshwari130@gmail.com', con))

for msg in msgs[::-1]:  
    for sent in msg: 
        if type(sent) is tuple:  
  
            # encoding set as utf-8 
            content = str(sent[1], 'utf-8')  
            data = str(content) 
  
            # Handling errors related to unicodenecode 
            try:  
                indexstart = data.find("ltr") 
                data2 = data[indexstart + 5: len(data)] 
                indexend = data2.find("</div>") 
  
                # printtng the required content which we need 
                # to extract from our email i.e our body 
                print(data2)
                print('-----------------------------')
            except UnicodeEncodeError as e: 
                pass

for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
for response in data:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode()
            # email sender
            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    print(body)
            if content_type == "text/html":
                # if it's HTML, create a new HTML file and open it in browser
                if not os.path.isdir('htmls'):
                    # make a folder for this email (named after the subject)
                    os.mkdir('htmls')
                filename = f"{subject[:50].replace(':','')}.html"
                filepath = os.path.join('htmls', filename)
                # write the file
                open(filepath, "w").write(body)
                # open in the default browser
                
            print("="*100)
imap.close()
imap.logout()