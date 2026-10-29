import requests
import json

http_reviews = requests.get("https://apis.codante.io/api/reviews-api/reviews")
dict_reviews = json.loads(http_reviews.content.decode("utf-8"))
list_review = []

for review in dict_reviews["data"]:
  list_review.append(review["description"])

#Desenvolva, a partir daqui, um chain para um agente que avalia se as revisões recebidas são positivas ou negativas.
#Utilize todos os componentes do LangChain que trabalhamos até este momento para isso.

