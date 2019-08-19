from bs4 import BeautifulSoup
import requests

def parseGroup(group):
  groupString = group.replace(' – ', ' ').strip()
  return groupString.split(",")

def parseVaccinationsToTravelAbroadHtmlPage():
  page = requests.get("https://www.isramedia.net/content/vaccinations-to-travel-abroad")
  soup = BeautifulSoup(page.content, 'html.parser')

  contentArticle = soup.find('div', class_='content-article')

  countryElements = contentArticle.select('h2')[4:] 

  vaccinesByCountry = []
  for country in countryElements:
    # skip continent headers
    if repr(country.nextSibling.nextSibling).startswith('<h2>'):
      continue

    countryName = country.text.strip('\n').strip(':')    

    nextSibling = country.nextSibling
    while repr(nextSibling).startswith('<h2>') == False and nextSibling is not None:
      if hasattr(nextSibling, 'contents') and len(nextSibling.contents) > 2:
        group = nextSibling.contents[1].text
        if group == 'קבוצה 1:':
          group1 = parseGroup(nextSibling.contents[2])
        elif group == 'קבוצה 2:':
          group2 = parseGroup(nextSibling.contents[2])
        elif group == 'קבוצה 3:':
          group3 = parseGroup(nextSibling.contents[2])

      nextSibling = nextSibling.nextSibling

    vaccinesByCountry.append({
      "country": countryName,
      "group1": group1,
      "group2": group2,
      "group3": group3,
    })
  
  return vaccinesByCountry