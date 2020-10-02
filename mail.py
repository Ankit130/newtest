import imaplib
import email
from functions import *
import time
from email.header import decode_header
from bs4 import BeautifulSoup as soup
import requests
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from datetime import datetime

def getcurtime():
    day=datetime.today().strftime('%A')
    ctime=datetime.datetime.now()
    return day,ctime
    
def acceptjob(link):
    r=requests.get(link)
    Soup=soup(r.text,'html.parser')
    txt=Soup.find('h1')
    if(txt):
        if(txt.text.strip()=='Job Accepted'):
            return True
        else:
            return False
    return False

def sendemail():
    cred=getcurcred()
    SMTP_USER = cred['email']
    SMTP_PASS = cred['pass']
    SMTP_HOST = cred['smtp_url']
    SMTP_SSL_PORT=cred['port']
    from_email=SMTP_USER
    emails=getalertemail()
    to_emails=[]
    for em in emails:
        to_emails.append(em.strip())
    #to_emails = ['infoankit130@gmail.com','ankitmaheshwari130@gmail.com']
    body = "Job is accepted by bot"
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n" 
    headers += f"Subject: Hello\r\n"
    email_message = headers + "\r\n" + body
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)  # Show SMTP server interactions
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.sendmail(from_email, to_emails, email_message)
    smtp_server.quit()

def getsub_from(data,keywords,emails,email):
        for response in data:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    zips,service,price,link='','','',''
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    from_ = msg.get("From")
                    flag=0
                    for keyword in keywords:
                        if(keyword.strip() in subject):
                                flag=1
                    for emai in emails:
                        if(emai.strip() in from_):
                                flag=1
                    if('FW:' in subject or 'Re:' in subject):
                        flag=0
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                    if content_type == "text/html":
                        Soup=soup(body,'html.parser')
                        div=Soup.find('div',attrs={'style':'font-size:23pt;line-height:27pt;text-align:center'}) 
                        if(div):
                                srvs=div.text.strip()
                                service,price=srvs.split("You'll Earn: $")[0].strip(),srvs.split("You'll Earn: $")[-1].strip()
                        else:
                                service,price='',''
                        zips=subject.split(',')[-1]
                        zips=zips.split('-')[0].strip()
                        link=Soup.find('a',attrs={'style':'color:#30383a'})
                        if(link):
                                link=link.get('href')
                        #if not os.path.isdir('htmls'):
                        #    os.mkdir('htmls')
                        #filename = f"{subject[:50].replace(':','')}.html"
                        #filepath = os.path.join('htmls', filename)
                        #open(filepath, "w").write(body)
                        
                    print("="*100)
                if(flag):
                        return (True,subject,from_,zips,service,price,link)
                else:
                        return (False,subject,from_,zips,service,price,link)
            
def log():
    print('loging in')
    cred=getcurcred()
    user=cred['email']
    password=cred['pass']
    imap_url = cred['imap_url']
    cou=totalemail()
    print('Total email '+cou)

    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user, password)
    return cou,con

def getall():
    exkey=getitems()
    onoff=getonof()
    term=gettime()
    cred=getcurcred()
    loc=getloc()
    zips=getzipgroups()
    if(loc==''):
        zips=[]
    else:
        zips=zips[loc]
    emkeys=getkeywords()
    gtemail=getemail()
    price=chprice()
    emails=getalertemail()
    return [exkey,onoff,term,cred,loc,zips,emkeys,gtemail,price,emails]
cpu,con=log()
count=1
stopflag=0
config=getall()
print(config)
while count!=2:
    if(ischng()):
        print('configuration changed')
        stopflag=0
        cou,con=log()
        config=getall()
        print(config)
    else:
        onoff=config[1]
        if(onoff=='OFF'):
            continue
        if(onoff=='ON Selected time'):
            times=config[2]
            cday,ctime=getcurtime()
            for t in times:
                day=t[0]
                stime=datetime.datetime.strptime(t[1],'%H:%M')
                etime=datetime.datetime.strptime(t[2].strip(),'%H:%M')
                if((stime.time() < ctime.time()) and (etime.time() > ctime.time()) and (day==cday)):
                    stopflag=0
                    break
                else:
                    stopflag=1

        if(stopflag):
            continue
        try:     
            data=con.select('Inbox')
        except:
            cou,con=log()
            config=getall()
            data=con.select('Inbox')
        curemail=data[-1][0]
        print(curemail)
        if(curemail.decode("utf-8")==cou):
                time.sleep(1)
        else:
                try:
                    tmp, da = con.fetch(data[-1][0], '(RFC822)')
                except:
                    cou,con=log()
                    config=getall()
                    data=con.select('Inbox')
                    tmp, da = con.fetch(data[-1][0], '(RFC822)')
                print('New Email')
                settot(str(int(curemail.decode("utf-8"))))
                flag,subject,from_,zips,service,price,link=getsub_from(da,getkeywords(),getemail(),email)
                count=count+1
                if(flag and link):
                    try:
                        price=float(price)
                    except:
                        price=0
                    tprice=float(config[-2].strip())
                    if((price>=tprice) and acceptjob(link)):
                        print('Job accepted')
                        #sendemail()
                    else:
                        print('Job not accepted')
                else:
                    print('This is not job oppurtunity email')
                cou=str(int(curemail.decode("utf-8")))
        #tmp, data = imap.search(None, 'ALL')

con.close()
con.logout()
