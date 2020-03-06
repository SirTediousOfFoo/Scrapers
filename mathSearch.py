import re
import requests
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from bs4 import BeautifulSoup

#this one is copy-pasted from somewhere, god only remembers where from
def pdf_to_text(pdfname):
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'iso 8859-2' #unless it's some special encoding you can go without it
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text #return an entire PDF as a string


def getContentURLsFrom(url): #returns a list of links found on a given URL
    page = requests.get(url).content #get html of a page
    soup = BeautifulSoup(page, 'html.parser') #turn it into soup
    tableLinks = soup.find_all('a', {"title": re.compile(".sred.|.SS.|.ss.")})
    #get all anchor elements with the attribute title containing either "sred", "SS" or "ss"
    #this is a RegEx search so change the stuff under re.compile to match whatever you want

    if len(tableLinks) is not 0:
        return tableLinks #if we didn't find anything matching our criteria just return None
    else:
        return None

#this one downloads all files with URLs found in above function
def getFilesFrom(links, baseURL="http://www.matematika.hr"):
    for link in links:
        print("Downloaded: " + link['title'] + " from:", (baseURL + link['href']))
        open(link['title'], "wb").write(requests.get(baseURL + link['href']).content)


def searchPDFs(keywords=None): #do a RegEx search for an expression specified with keywords
    if keywords is None:
        keywords = ["."]
    cnt = 0 #count out all files that had a hit
    dir = os.fsencode(".") #search the same directory as the script
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):
            search = re.search(keywords, pdf_to_text(os.fsdecode(file))) #convert and search pdf
        if search is not None:
            os.rename(filename, "Found/" + filename) #move it to the "Found" directory
            print(file)
            search = None
            cnt += 1
    print(cnt)

#search the website by year and download all files matching our criteria
for year in range(2006, 2020):
    contentLinks = getContentURLsFrom("http://www.matematika.hr/natjecanja/domaca/{}/".format(str(year)))
    if contentLinks is not None:
        getFilesFrom(contentLinks)

searchPDFs(".[Mm]aks.|.[Mm]inim.|[Ee]kstr.|[Vv]rijednost* funkcij[ae]")#search and we're done
