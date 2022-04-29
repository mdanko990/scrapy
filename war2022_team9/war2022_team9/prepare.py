import codecs
import json
import os


if __name__ == "__main__":
    json_path = os.path.dirname(os.path.realpath(__file__))+"\\"
    json_file = "svoboda_articles.json"
    json_data=[]
    os.mkdir(json_path+"sas_ready_txt")
    with open(json_path+json_file) as json_fileopen:
        json_data = json.load(json_fileopen)
    for article in json_data:
        article_text = ""
        if len(article['article_title']) > 0:
            article_text = article['article_title'][0].replace("\n", "")+"\n\n"+article['article_text'].replace("\xa0"," ")
        else:
            article_text = ""
        article_uuid = article['article_uuid']
        with codecs.open(json_path+"sas_ready_txt/" + article_uuid + ".txt", "w", "utf-8-sig") as temp:
            temp.write(article_text)

