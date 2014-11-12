from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.danforthart.org/"

def make_soup(url): 
        html = urlopen(url).read()
        return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
        soup = make_soup(section_url)
        nav = soup.find('div', {'id': 'Stripe'}) #find all links from navigation stripe
        tdList = []
        for td in nav.findAll('td'):
            if td.a is not None:
                tdList.append(td.a['href'])
        return tdList
        
#From exhibitions page, find all side subnav links
def get_subnav_links(exhibits_url):
        soup = make_soup(exhibits_url)
        subnav = soup.find('div', {'id': 'Menu'})
        urls = []
        for li in subnav.findAll('li'):
                urls.append(li.a['href'])
        return urls


# From all exhibition links, find current events and exhibitions
def get_link_events(link_url): 
        soup = make_soup(link_url)
        events = []
        content = soup.find('div', {'id':'Content'}) # find content to search
        for div in content.findAll('div'):
                if div.a is not None:
                        link = BASE_URL + div.a['href']
                        if link not in events:
                                events.append(link)
        
        return events


# From current exhibition links, get relevant dates and information
def get_event_info(event_url): 
        soup = make_soup(event_url)
        content = soup.find('div', {'id':'Content'}) # find content tag 

        #GET NAME
        name = "" 
        h1 = content.find('h1') # find title tag
        name = h1.text

        
        #GET DATE AND LOC
        date = ""
        loc = ""
        dateloc = content.find('p', {'class': 'caption'}) # look for date after image
        date = dateloc.find_next('h2').getText().strip()
        

       # GET DESCRIPTION
        text = ""
        textloc = content.find('hr')
        newcontent = textloc.find_next_siblings('p')
        for p in newcontent:
            text += p.getText().strip()

        
        # GET IMAGES URL
        image = ""
        image_path = content.find('img')['src']
        image = (BASE_URL + image_path).strip() 

        
        return name, date, image, loc, text



###############################
#### Get information from Danforth webexhibits.htmlsite 
#### Currently, information gotten includes for each current exhibit, its title, date, image, and text 

def scrape(): 
        
        currentExhibitions = [] #list for event links
        allEvents = []

        links = get_nav_links(BASE_URL) #get all navigation links from main page
        for link in links: 
                if re.match('(.*)exhibits', link, re.I): #find all links with exhibitions 
                        url = link #all current event links 
        sublinks = get_subnav_links(url)
        for sublink in sublinks:
                if re.match('exhibits.html', sublink, re.I):
                        currentExhibitions.extend(get_link_events(BASE_URL + sublink))
                if re.match('upcomingExhibits.html', sublink, re.I):
                        currentExhibitions.extend(get_link_events(BASE_URL + sublink))

        
        for exh in currentExhibitions: #iterate through to get to each exhibition link
                #For each distinctive link: return dictionary with url, dates, description, image, and name labels
                info = {}       
                name,date,image,loc,text = get_event_info(exh) # get info 
                info['url'] = exh; # add value for 'url' key 
                info['dates'] = date
                info['description'] = text
                info['image'] = image
                info['name'] = name 
                info['location'] = loc
                allEvents.append(info)  

        return allEvents
    
print scrape()
