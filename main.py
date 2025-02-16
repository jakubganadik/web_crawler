import os
import requests

api_key = 'b7925a3e-1988-4740-a654-6f8f00657aad'
output_directory = 'animal_articles'
os.makedirs(output_directory, exist_ok=True)


def list_articles():
    endpoint_url = 'https://syndication.api.eb.com/production/articles'
    parameters = {
        'articleTypeId': '1',
        'categoryId': '9',
        'page': '2'
    }
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    response = requests.get(endpoint_url, params=parameters, headers=headers)
    if response.status_code == 200:
        data = response.json()
        xml_file_counter = 0
        flag = False
        for article in data.get('articles', []):
            article_id = article.get('articleId')
            if flag:
                get_article_info(article_id)
                xml_file_counter += 1
                if xml_file_counter >= 5000:
                    print("Maximum limit of 5000 XML files reached.")
                    return  # Stop fetching more XML files
                if article_id == 41085:
                    flag = True
    else:
        print('status code is not 200')


def get_article_info(article_id):
    endpoint_url = f'https://syndication.api.eb.com/production/article/{article_id}/xml'
    headers = {
        'x-api-key': api_key
    }

    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        xml_content = response.text
        file_name = os.path.join(output_directory, f'article_{article_id}.xml')
        with open(file_name, 'wb') as xml_file:
            xml_file.write(xml_content.encode('utf-8'))
        print(f'Saved XML with article ID {article_id}')
    else:
        print('status code is not 200')


list_articles()
