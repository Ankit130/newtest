from flask import Flask,render_template, url_for, flash,redirect,request, jsonify
from functions import *
from forms import Emailpass,TurnOnOff,TimeFrame
#from functions import getitems,delt,additem,getzipgroups,addzip,getloc,setloc,getkeywords,deletekeyword,addkeyword

app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/',methods=['GET','POST'])
def home():
	return render_template('home.html',title='Console Page')


@app.route('/emailpass',methods=['GET','POST'])
def hello():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		print(data)
		if data['action'][0] == 'Submit':
			try:
				email=data['email'][0]
				pas=data['password'][0]
				imap_server=data['imap_url'][0]
				smtp_server=data['smtp_url'][0]
				port=data['port'][0]
				if(email=='' or pas=='' or imap_server=='' or smtp_server=='' or port==''):
					message='Please Provide Every detail'
					flash(message,'error')
				else:	
					setcred(email,pas,imap_server,smtp_server,port)
					chng()
					flash('Credential configuration is  changed','success')
			except:
				message='Please Provide Every detail'
				flash(message,'failure')
	return render_template('emailpass.html',title='change email and password',email_pass=getcurcred())



@app.route('/onoroff',methods=['GET','POST'])
def onoff():
	form=TurnOnOff()
	if form.validate_on_submit():
		flash('Changes Saved','success')
		data=request.form.to_dict(flat=False)
		on=data['on_or_off'][0]
		setonoff(on)
		chng()
	return render_template('onoff.html',title='Automatic ON/OFF', onoff=form,selected=getonof())


@app.route('/timeframe',methods=['GET','POST'])
def timeFrame():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		if data['action'][0]=='Submit':
			try:
				day=data['days'][0]
			except:
				day=''
			try:
				start=data['start_time'][0]
			except:
				start=''
			try:
				end=data['end_time'][0]
			except:
				end=''
			if(day=='' or start=='' or end==''):
				flash('Please provide day, start time and end time please','error')
			else:
				flash('Changes Saved','success')
				settime(day,start,end)
				chng()
		elif data['action'][0]=='Delete':
			try:
				item=data['listitem'][0]
				deltime(item)
				flash('deleted','success')
				chng()
			except:
				flash('Please select from the list')
		elif data['action'][0]=='Click here to accept job always':
			with open('timeframe.txt','w') as f:
				f.write('\n')

		
			
	return render_template('timeFrame.html',title='Change Time Frame',data=gettime(),days=['Monday','Tuesday','Wednesday','Thurshday','Friday','Saturday','Sunday'])	


@app.route('/exclude',methods=['GET','POST'])
def exclude():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		print(data)
		if data['action'][0] == 'del':
			try:
				item=data['listitem'][0]
			except:
				item=''
			delt(item)
			chng()
		if data['action'][0] == 'add':
			additem(data['keyword'][0])
			chng()
	return render_template('exclude.html',title='exclude jobs',data=getitems())

@app.route('/zipgroupadd', methods=['GET','POST'])
def zipgroupadd():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		if data['action'][0] == 'add':
			key=data['localityname'][0]
			zips=','.join(data['zips'][0].split(' '))
			addzip(key+'='+zips+'\n')
			chng()
		
	return render_template('zipadd.html',title='Add New Locality',groups=getzipgroups())

@app.route('/selectzip',methods=['GET','POST'])
def selectzip():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		if data['action'][0] == 'select':
			try:
				item=data['listitem'][0]
			except:
				item=''
			if(item=='None'):
				item=''
			setloc(item)
			chng()
	return render_template('zipselect.html',title='Select locality',data=getzipgroups(),loc=getloc())

@app.route('/emailkeyword',methods=['GET','POST'])
def checkkeyword():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		print(data)
		if data['action'][0] == 'Delete':
			try:
				if(data['listitem'][0]==''):
					flash('please select keyword from list','error')
				else:
					deletekeyword(data['listitem'][0])
					chng()
			except:
				flash('please select keyword from list','error')
			
		if data['action'][0] == 'Add':
			if(data['keyword'][0]==''):
				flash('Please enter some keyword','error')
			else:
				addkeyword(data['keyword'][0])
				chng()
		if data['action'][0] == 'Delete Email':
			try:
				item=data['listitem1'][0]
				delemail(item)
				chng()
			except:
				flash('please select email from list','error')
		if data['action'][0] == 'Add email':
			if(data['email'][0]==''):
				flash('Please enter an email','error')
			else:
				addemail(data['email'][0])
				chng()
			

	return render_template('checkkeyword.html',title='Email subject keywords',data=getkeywords(),email=getemail())


@app.route('/emailalert',methods=['GET','POST'])
def emailalert():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		print(data)
		if data['action'][0] == 'Delete Email':
			try:
				item=data['listitem1'][0]
				item=item.replace('\r\n','')
				delalertemail(item)
				chng()
			except:
				flash('please select email from list','error')
		if data['action'][0] == 'Add email':
			if(data['email'][0]==''):
				flash('Please enter an email','error')
			else:
				addalertemail(data['email'][0])
				chng()
	return render_template('alert.html',title='Add Email to send email',email=getalertemail())

@app.route('/price',methods=['GET','POST'])
def price():
	if request.method=='POST':
		data=request.form.to_dict(flat=False)
		try:
			pri=data['price'][0]
			if(pri==''):
				flash('please enter some threshold amount')
			else:
				setprice(pri)
				flash('Changes saved','success')
		except:
			flash('please enter correct amount')
	return render_template('price.html',title='Price Setting Page',loc=chprice())

if __name__ == "__main__": 
        app.run() 
