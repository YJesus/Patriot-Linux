import tkinter as tk
import tkinter.messagebox as tkmb
import psutil
import os
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL
import filecmp
import re
import time
import threading
import datetime
import re

debian = '/etc/debian_version'
redhat = '/etc/redhat-release'

def PrintaLog(texto):
	
	t = time.time()
	logtime= time.ctime(t)
	
	stringprint = "%s %s\n" % (logtime, texto)
	
	f = open("/var/log/patriot", "a")
	f.write(stringprint)
	f.flush()
	f.close()

def PrintaMSG(texto):

	command = 'python3 alertiqt.py "'+texto+'"' 
					
	processalert = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)

def TestIntegrity(File):
	
	if os.path.exists(redhat) : 
	
		command = 'rpm -Vf "'+File+'"' 
					
		processrpm = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
		outputrpm = processrpm.communicate()[0]
					
		if outputrpm :
						
			return(1)
								
		
		else:
			
			return(0)

	else :	
		
		commandDPKG = 'dpkg -S "'+File+'"'
						
						
		processdpkg = subprocess.Popen([commandDPKG], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)
		outputdpkg = processdpkg.communicate()[0]
						
		if processdpkg.returncode == 1:
							
			#dpkg is buggy to find package files 
							
			fixdpkgbug= re.sub('/usr',  '',    File)
							
			commandDPKG2 = 'dpkg -S "'+fixdpkgbug+'"'
						
			processdpkg2 = subprocess.Popen([commandDPKG2], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)
			outputdpkg2 = processdpkg2.communicate()[0]
							
			outputdpkg = outputdpkg2
							
			if processdpkg2.returncode == 1:
							
				return(1)
								
				
		packagename = outputdpkg.split(":")
						
		commandDEBSUM = 'dpkg --verify "'+packagename[0]+'"'
						
							
		processdebsum = subprocess.Popen([commandDEBSUM], stdout=subprocess.PIPE,shell=True)
		outputdebsum = processdebsum.communicate()[0]
		
		print (outputdebsum)
						
		if outputdebsum :
			
			return(1)
						
		else:
			return(0)


def ScanUnsigned():
	
	pidsinicial = psutil.pids()

	while True:
	
		pidsshots = psutil.pids()
	
		s = set(pidsinicial)
		newpids = [x for x in pidsshots if x not in s]
	
		if newpids:
	
			#print(newpids)
		
			for i in newpids:
			
				#print(i)
				try:
					p = psutil.Process(pid=i)
					with p.oneshot():
			
						integrity= TestIntegrity(p.exe())
			
						#print (integrity)
						
						pidproceso = p.pid
						exeproceso = p.exe()
						
						evadeau = bool(re.match(exeproceso, "/usr/sbin/ausearch"))
						
						if integrity == 1 and evadeau == 0:
						
							stringprint = "New process that not belongs to any package or package was modified: %i %s" % (pidproceso, exeproceso)
						
							x = threading.Thread(target=PrintaMSG, args=(stringprint,))
							x.setDaemon(True)
							x.start()
							
							PrintaLog(stringprint)
						
				except Exception as e:
					print (e)
	
		pidsinicial = pidsshots
	
		time.sleep(2)
		

def ScanConnections():
	
	initialcon =psutil.net_connections()

	netprocess =[]

	for i in initialcon:
	
		#print (i.pid)
	
		p = psutil.Process(pid=i.pid)
	
		with p.oneshot():
		
			#print (p.exe())
		
			netprocess.append(p.exe())
		
	#print (netprocess)
	
	while True:
		
		runcon =psutil.net_connections()

		netprocessrun =[]

		for e in runcon:
	
			#print (e.pid)
	
			p = psutil.Process(pid=e.pid)
	
			with p.oneshot():
		
				#print (p.exe())
		
				netprocessrun.append(p.exe())
		
		#print (netprocessrun)
		
		s = set(netprocess)
		newpconprogs = [x for x in netprocessrun if x not in s]
		
		if newpconprogs:
	
			#print(newpconprogs)
		
			for h in newpconprogs:
				
				stringprint = "New Process initiating TCP/IP connection: %s" % h
						
				x = threading.Thread(target=PrintaMSG, args=(stringprint,))
				x.setDaemon(True)
				x.start()
				
				PrintaLog(stringprint)
				
				netprocess.append(h)
		
				
		time.sleep(2)

def AuSearch():
	
	auparams = {"modules": "New module loaded in Kernel","code_injection": "DLL Inject","register_injection": "DLL Inject"}
	
	while True:
	
		tomo = datetime.datetime.now() - datetime.timedelta(minutes=2)

		timeraw = str(tomo.time().replace(second=0, microsecond=0))

		for key in auparams.keys():
			#print(key)
	
			command = 'ausearch -k "'+key+'" --start "'+timeraw+'"' 
					
			processausearch = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)
			outputausearch = processausearch.communicate()[0]
	
			if outputausearch:
			
				stringprint = "Audit Alert: %s" % auparams[key]
						
				x = threading.Thread(target=PrintaMSG, args=(stringprint,))
				x.setDaemon(True)
				x.start()
			
				PrintaLog(stringprint)
	
		time.sleep(115)

def KeyBoardSearch():
	
	command = "xinput --list" 
	
	keyfirstcommand = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
	outputkeysearch= keyfirstcommand.communicate()[0]
	
	while True:
		
		keyruncommand = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
		outputkeyrunsearch= keyruncommand.communicate()[0]
		
		if outputkeyrunsearch != outputkeysearch:
			
			stringprint = "New keyboard detected"
			
			x = threading.Thread(target=PrintaMSG, args=(stringprint,))
			x.setDaemon(True)
			x.start()
			
			PrintaLog(stringprint)
			
			outputkeysearch = outputkeyrunsearch
			
		time.sleep(60)
			
	
s = threading.Thread(target=KeyBoardSearch)
s.setDaemon(True)
s.start()	

x = threading.Thread(target=ScanUnsigned)
x.setDaemon(True)
x.start()

y = threading.Thread(target=ScanConnections)
y.setDaemon(True)
y.start()

z = threading.Thread(target=AuSearch)
z.setDaemon(True)
z.start()

while True:
	
	time.sleep(100)
