import time
def getitems():
	with open('exclude.txt','r') as f:
		data=f.read().split('|||')
	return data

def delt(key):
	data=getitems()
	data1=[]
	for d in data:
		if(d==key):
			continue
		else:
			data1.append(d)
	data1='|||'.join(data1)
	with open('exclude.txt','w') as f:
		f.write(data1)
	return True

def additem(key):
	data=getitems()
	data.append(key)
	data='|||'.join(data)
	with open('exclude.txt','w') as f:
		f.write(data)
	return True

def getzipgroups():
	groups={}
	with open('zipsgroup.txt','r') as f:
		data=f.readlines()
	for d in data:
		key=d.split('=')[0]
		vals=d.replace('\n','').split('=')[1]
		groups[key]=vals
	return groups

def addzip(val):
	with open('zipsgroup.txt','a') as f:
		f.write(val)

def getloc():
	with open('selectedlocal.txt','r') as f:
		d=f.read()
	return d

def setloc(val):
	with open('selectedlocal.txt','w') as f:
		f.write(val)

def getkeywords():
	with open('keywords.txt','r') as f:
		data=f.read().split('|||')
	if(data==['']):
		return []
	return data

def deletekeyword(key):
	data=getkeywords()
	data1=[]
	for d in data:
		if(d==key):
			continue
		else:
			data1.append(d)
	data1='|||'.join(data1)
	with open('keywords.txt','w') as f:
		f.write(data1)
	return True

def addkeyword(key):
	data=getkeywords()
	data.append(key)
	data='|||'.join(data)
	if(data==''):
		return 
	with open('keywords.txt','w') as f:
		f.write(data)
	return True

def getcurcred():
	with open('email.txt','r') as f:
		data=f.read()
	email=data.split('|||')[0]
	pas=data.split('|||')[1]
	imap_url=data.split('|||')[2]
	smtp_url=data.split('|||')[3]
	port=data.split('|||')[4]
	return {'email':email,'pass':pas,'imap_url':imap_url,'smtp_url':smtp_url,'port':port}

def setcred(email,pas,imap_url,smtp_url,port):
	with open('email.txt','w') as f:
		f.write(email.strip()+'|||'+pas.strip()+'|||'+imap_url.strip()+'|||'+smtp_url.strip()+'|||'+port)

def setonoff(val):
	with open('onoff.txt','w') as f:
		f.write(val)

def getonof():
	with open('onoff.txt','r') as f:
		d=f.read()
	if(d=='1'):
		return 'ON'
	if(d=='0'):
		return 'OFF'
	else:
		return 'ON Selected time'

def settime(day,time1,time2):
	with open('timeframe.txt','a') as f:
		f.write(day+'='+time1+'='+time2+'\n')

def gettime():
	with open('timeframe.txt','r') as f:
		data=f.readlines()
	times=[]
	for d in data:
		try:
			day=d.split('=')[0]
			start=d.split('=')[1]
			end=d.split('=')[2]
			times.append([day,start,end])
		except:
			continue
	return times

def deltime(day):
	data=gettime()
	print(day)
	with open('timeframe.txt','w') as f:
		for d in data:
			print(d)
			if(str(d)==day):
				continue
			else:
				f.write('='.join(d))

def addemail(email):
	with open('jobemail.txt','a') as f:
		f.write(email+'\n')

def getemail():
	with open('jobemail.txt','r') as f:
		data=f.readlines()
	return data

def delemail(email):
	data=getemail()
	with open('jobemail.txt','w') as f:
		for d in data:
			if(email.strip()==d.strip()):
				continue
			else:
				f.write(d)

def addalertemail(email):
	with open('alertemail.txt','a') as f:
		f.write(email+'\n')

def getalertemail():
	with open('alertemail.txt','r') as f:
		data=f.readlines()
	return data

def delalertemail(email):
	data=getalertemail()
	with open('alertemail.txt','w') as f:
		for d in data:
			print(email,d)
			if(email.strip()==d.strip()):
				continue
			else:
				f.write(d)


def totalemail():
	with open('total.txt','r') as f:
		d=f.read().strip()
	return d

def settot(num):
	with open('total.txt','w') as f:
		f.write(str(num))

def chng():
	try:
		with open('change.txt','w') as f:
			f.write('1')
	except:
		time.sleep(1)
		chng()

def chprice():
	with open('price.txt','r') as f:
		d=f.read().strip()
	return d

def setprice(price):
	with open('price.txt','w') as f:
		f.write(price)
	
def ischng():
	try:
		with open('change.txt','r') as f:
			d=f.read().strip()

		if(d=='1'):
			with open('change.txt','w') as f:
				f.write('0')
			return True
		else:
			return False
	except:
		time.sleep(1)
		return ischng()

