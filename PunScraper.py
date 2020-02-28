import requests
import bs4


page = requests.get("https://onelinefun.com/puns/") #GET the link
soup = bs4.BeautifulSoup(page.content, features="html.parser") #Turn the link into BeautifulSoup object using an html parser
divs = soup.findAll("div", {"class": "o"}) #Find all instances of a specific class of div

with open("puns", "w") as puns: #Open file for writing
    for div in divs:
        puns.write(div.find("p").text+"\n") #Write out each pun contained in the <p> tag into it's own line
    i = 2 #set up a counter for other pages
    while True: #Do the same thing many times
        page = requests.get("https://onelinefun.com/puns/" + str(i) + "/")
        soup = bs4.BeautifulSoup(page.content, features="html.parser")
        divs = soup.findAll("div", {"class": "o"})

        if len(divs) == 0 or page.status_code != 200: #If we overshot the number of pages or went to a bad link quit the loop
            break

        for div in divs:
            puns.write(div.find("p").text+"\n") #Write it all out again
        print("Done with page " + str(i)) #Track how many pages we've done for fun

        i += 1 #Increase page counter
