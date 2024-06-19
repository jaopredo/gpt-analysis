import requests

page = requests.get("https://www.imdb.com/title/tt2140553/?ref_=tt_urv")


print(page.status_code)