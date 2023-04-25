import time
from datetime import date
from newsGetter import newsGetter


start_time = time.time()
qdp_categories = ['vazzola', 'mareno-di-piave', 'santa-lucia-di-piave', 'conegliano']

sites = {

    'qdp': 'https://www.qdpnews.it/',
    'gazzettino': 'https://www.ilgazzettino.it/nordest/treviso/',
    'corriere della sera': 'https://www.corriere.it/',
    'la repubblica': 'https://www.repubblica.it/',
    'il sole 24 ore': 'https://www.ilsole24ore.com/',
    'gazzetta ufficiale': 'https://www.gazzettaufficiale.it/',
    'internazionale': 'https://www.internazionale.it/',
    'ansa': 'https://www.ansa.it/sito/notizie/mondo/mondo.shtml',  # versione mondo
    'euronews': 'https://it.euronews.com/notizie/internazionale',
    'today': 'https://www.today.it/',
    'scholar': 'https://scholar.google.com/'
}


output_file = 'news.md'
open(output_file, 'w').close()

newsGetter = newsGetter()
output = newsGetter.get(sites, qdp_categories)
with open(output_file, 'a') as target:
    target.write(output)

print(time.time() - start_time)
