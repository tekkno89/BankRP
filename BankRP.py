import mechanize, odbc, datetime
from BeautifulSoup import BeautifulSoup


def getPage(ID,SSN):
	ID = ID
	SSN = SSN
	print ID
	br = mechanize.Browser()
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.addheaders = [('USER_AGENT', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')]
	try:
		br.open('https://*************')
	except:
		print 'Error Loading Page'
		getPage(ID, SSN)
	br.select_form(nr=0)
	
	br['loginid'] = '******'
	br['passwd'] = '******'
	if ID == 0:
		br['client'] = 'ACS BankRP Program'
	else:
		note = 'ACS %s' % ID
		br['client'] = note
	br.submit()

	
	lnk = br.find_link(text='BankRP Case Locator')# First Page
	br.follow_link(link=lnk)
	
	br.select_form(nr=0)# Search Page
	br['ssn'] = SSN
	br.submit()
	page = br.response().read()
	return page
	
	
	
	
def pageResults(page):
	soup = BeautifulSoup(page)
	searchResults = soup.find(id='status').string
	
	if searchResults != 'No Records Found':
		return soup.find(id='details')
	else:
		return False
		
		
		

def resultsVals(details):
	soup = BeautifulSoup(details)
	results = soup.findAll('tr')[1:]
	resultsList = []
	
	for row in results:
		column = row.findAll('td')
		nameRes = column[0].string
		courtRes = column[1].string
		caseRes = column[2].a.string
		chapterRes = column[3].string
		dateFiledRes = column[4].string
		dateClosedRes = column[5].string
		dispostionRes = column[6].string
		
		rowList = [nameRes,courtRes,caseRes,chapterRes,dateFiledRes,dateClosedRes,dispostionRes]
		resultsList.append(rowList)
		
	return resultsList
	
	
	
	
def checkDates(bkpDate, DM, debtID):
	con = odbc.odbc('%s/DM/TURBODELTA' % DM)
	cur = con.cursor()
	query = "SELECT serv_date FROM debt401_view WHERE debt_id = %d" % debtID
	cur.execute()
	results = cur.fetchone()
	dmDate = results[0]
	
	convertDate = bkpDate.split('/')
	bkpDate = datetime.date(convertDate[2],convertDate[0],convertDate[1])
	
	if bkpDate > dmDate:
		return True
	else:
		return False
	