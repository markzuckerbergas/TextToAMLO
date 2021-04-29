import mechanicalsoup
import requests
import os

browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
base_url = "https://lopezobrador.org.mx/secciones/comunicados/"

if not os.path.exists('conference_audio'):
    os.makedirs('conference_audio')

def extract_audio(url):
    global browser

    print("Searching titles in", url)
    r = browser.open(url)

    if not r.ok:
        print("URL not found", "EXITING PROGRAM")        
        exit()
        
    entries = browser.page.select('.entry-title a')

    print("Entries found in page:", len(entries), "\n")

    for entry in entries:
        print("Searching url:", entry['href'])   
        browser.follow_link(entry)

        try:            
            audio_url = browser.page.select(".wp-block-audio audio")[0]['src']
        except:
            print("Audio file not found in entry. Skipping...\n")
            continue

        print("Downloading audio file:", audio_url)
        file_name = audio_url.split('/')[-1]

        if os.path.isfile('conference_audio/'+file_name):
            print("File already exists","\n")            
            continue

        response = requests.get(audio_url)        

        if response.ok:
            with open('conference_audio/'+file_name, 'wb') as file:
                file.write(response.content)
                print("Successfuly saved as:", file_name, "\n")                    
        else:
            print("Unable to download\n")    

print("Crawling pages until url not found\n")
print("Crawling page 1")
extract_audio(base_url)

page = 2
while True:
    print("Crawling page", page)
    extract_audio(base_url+'page/'+str(page))
    n += 1

