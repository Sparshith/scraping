import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import os


def ensure_dir(f):			# function to create directories for storing data
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#headers to be sent to url which has the results.

headers = {
	'Accept ':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control':'max-age=1000000000',
    'Cookie':'PHPSESSID=37b9f16874c03d7c07789c4c5238a641; mypets=0c; __utma=50120421.130946855.1435211323.1435312969.1435635572.3;    __utmb=50120421.2.10.1435635572; __utmc=50120421; __utmz=50120421.1435211323.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Connection':'keep-alive',
   'Host': 'www.rvce.edu.in',
   'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}

# headers to be sent to base_url.

headers_base={
'Host': 'www.rvce.edu.in',
'Connection': 'keep-alive',
'Content-Length': '25',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Origin': 'http://www.rvce.edu.in',
'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'http://www.rvce.edu.in/results/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.8',
'Cookie': 'PHPSESSID=37b9f16874c03d7c07789c4c5238a641; mypets=0c; __utmt=1; __utma=50120421.130946855.1435211323.1435887704.1435890820.12; __utmb=50120421.4.10.1435890820; __utmc=50120421; __utmz=50120421.1435211323.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
}

cur_acad_year= 14                                 #last two digits of the current academic year


#getting a list of departments and their id's.
depts=[]
base_url= "http://www.rvce.edu.in/results/"
q= requests.get(base_url)
soup= BeautifulSoup( q.text, "lxml")
rows= soup.findAll("tr")
options= rows[3].findAll("option")
a=0
for option in options:
	if(a>0):                                                  # First option tag just contains header
		depts.append([option['value'],option.string])
	else:
		a= a+1

test=0

for department in depts:
	sem_value = 2                                          #Change this value to 1 if odd sem, 2 if even sem
	department_name= department[1].strip()

	if(test != 0):
		break
	print "Downloading data for the department "+ department_name+ "...."
	for w in range(0,4):
		value= str(department[0])
		s= requests.post(base_url, data={'branch':value, 'sem': sem_value ,'Submit':'go'},headers= headers_base)
		print "Accessing data from usn: "+s.url+ "....."


		url= s.url
		html= urlopen(url). read()
		soup = BeautifulSoup(html, "lxml")
	
	
		"""
		method to access elements using bs4
		
		table= soup.findAll("table") 
		row= table[0].findAll("tr")
		cell= row[3].findAll("td")
		branch= cell[1].string
		"""	

		sem = sem_value
		# for writing in to csv files
		cur_dir= os.path.dirname(os.path.abspath(__file__))
		project_name= "RVCE_Results_Anaysis"
		dir_parent= department_name
		dir_child= department_name+"_"+str(sem)
		filename= department_name+"_"+str(sem)+"_sem.csv"
		f= cur_dir+ "/"+ project_name+ "/" + dir_parent+ "/"+ dir_child+ "/"+ filename
		ensure_dir(f)
		
		
		
		#Headers of csv: USN,Name,Branch, [Subject ID's], SGPA
		csv_headers= ['USN', 'Name', 'Branch']
		table= soup.findAll("table")
		rows= table[1].findAll("tr")
		for row in rows:
		     cells= row.findAll("td")
		     if(len(cells)==2):
		     	csv_headers.append(cells[0].string)
	
		ofile  = open(f, "wb")
		writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow(csv_headers)
	
	
		#Generating USN's
		if( department_name == "Information Science"):
			branch_code= "IS"
		elif( department_name == "Instrumentation Technology"):
			branch_code= "IT"
		elif( department_name == "Bio Technology"):
			branch_code= "BT"
		elif(department_name == "B. Arch"):
			branch_code= "AT"
		usn= "1RV"
		if( sem%2 ==0 ):                           #even sem
			year= cur_acad_year- (sem/2) +1
			
			
		elif( sem_value%2 ==1):
			year = cur_acad_year- (sem/2)
		usn= usn + str(year)+ branch_code
		for j in range(1, 70):
			if(j<10):
				cur_usn = usn +"00"+ str(j) # can also use cur_usn.zfill(3)
			elif(j>9 and j<100):
				cur_usn = usn +"0"+ str(j)
			else:
				usn = usn + str(j)
			args= {'usn': cur_usn}
	
	
		# Getting results	
			csv_rows=[]
			r = requests.post( url , data=args, headers=headers)
			soup= BeautifulSoup( r.text, "lxml")
		
			#extracting names of students
			divisions= soup.findAll("div")
			name= divisions[2].string
			try:
				name = name.replace(u'\xa0', u' ').replace('Name','').strip().replace(':', '').strip().title()	
			
			except AttributeError:
				print "No student at USN: ",
				print cur_usn
				continue
			
			print "Entering Data for " +name+ " with USN "+ cur_usn+ "..." 		
			csv_rows.extend([cur_usn, name, department_name])
		
			tables= soup.findAll("table")
			rows= tables[1].findAll("tr")
			for row  in rows:
				cells= row.findAll("td")
		     		if(len(cells)==3):
			     		csv_rows.append(cells[2].string.strip())
			     	elif(len(cells)==2):
			     		csv_rows.append(cells[1].findAll("strong")[0].string)
			     		
			writer.writerow(csv_rows)
			
		sem_value= sem_value + 2

print "Finishem"	
ofile.close()

	
	
