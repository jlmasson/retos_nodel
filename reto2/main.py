import time
import requests as http
import json
import datetime

tiempo_unix_actual = int(time.time())
maximo = int(datetime.datetime(2019,12,1,23,59,59).timestamp())
minimo = int(datetime.datetime(2019,10,1,0,0,0).timestamp())

print(minimo, maximo)

BASE_URL = "https://www.instagram.com/"
HASHTAG = "pubg"
QUERY_HASH = "bd33792e9f52a56ae8fa0985521d141d"
data_procesada = []

params = {
    'query_hash': 'bd33792e9f52a56ae8fa0985521d141d',
    'variables': json.dumps({
        "tag_name": HASHTAG,
        "first":1,
        "after":"QVFBUy1nQkphZm03Y0lQMElxYWQ1SG90eHJzd0J1U29QbmFtUzA0eDE2cHV1Y1F5ME14T2Z3UXZSVVRaSzFHa3RoVHJ5YVVWWTl4UGFwUGdlVnd5eE01Nw=="
    })
}

# Aquí va el lazo while infinito
salir = False
end_cursor = ''

f_csv = open('resultados_reto2.csv', 'w', encoding='utf8')

while not(salir):

    # https://www.instagram.com/graphql/query/?query_hash=bd33792e9f52a56ae8fa0985521d141d&variables=%7B%22tag_name%22%3A%22pubg%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFDdHptV1VkRTRRNDFpSjV0cVEzek1qOU5KY215b0N5N1BFV1JZeGYwTk14dW05MHlhZ1AzTHdKN0Jia280NDhMSWVJMlZtU0Z6THktaS1iSUhMTllhTw%3D%3D%22%7D

    # url_info = "{}explore/tags/{}/?__a=1&max_id={}".format(BASE_URL, HASHTAG, end_cursor)
    # print(url_info)
    url_info = "{}graphql/query".format(BASE_URL)
    response = http.get(url_info, params=params)
    print(response.url)

    print(response)

    # Código OK
    if response.status_code == 200:
        data = response.json()


        info_posts_recientes = data['data']['hashtag']['edge_hashtag_to_media']
        info_siguiente = info_posts_recientes['page_info']
        posts_peticion = info_posts_recientes['edges']

        data_procesada = []
        BASE_URL_POST = 'https://instagram.com/p/'

        for info_post in posts_peticion:
            nodo = info_post['node']
            captions = nodo['edge_media_to_caption']['edges']
            nodo_comentarios = nodo['edge_media_to_comment']
            nodo_likes = nodo['edge_liked_by']
            nodo_usuario = nodo['owner']

            shortcode_url = nodo['shortcode']
            content_post = captions[0]['node']['text']
            content_post = content_post.strip().replace('\n', ' ').replace(',', ' ')
            comment_post = nodo_comentarios['count']
            likes_post = nodo_likes['count']
            user_id_post = nodo_usuario['id']
            text_post = captions[0]['node']['text']
            timestamp_post = nodo['taken_at_timestamp']

            fecha_encuentra = datetime.datetime.utcfromtimestamp(timestamp_post).strftime('%Y-%m-%dT%H:%M:%SZ')
            print(fecha_encuentra)

            if (timestamp_post >= minimo):
                if (timestamp_post <= maximo):
                    timestamp_post = datetime.datetime.utcfromtimestamp(timestamp_post).strftime('%Y-%m-%dT%H:%M:%SZ')
                    info_procesada = {
                        'LinkPost': '{}{}'.format(BASE_URL_POST, shortcode_url),
                        'Fecha': timestamp_post,
                        'Content': content_post,
                        'Likes': likes_post,
                        'Comments': comment_post,
                        'UserId': user_id_post
                    }
                    data_procesada.append(info_procesada)
                    linea = "{},{},\"{}\",{},{},{}\n".format(info_procesada['LinkPost'], info_procesada['Fecha'], info_procesada['Content'], info_procesada['Likes'], info_procesada['Comments'], info_procesada['UserId'])
                    f_csv.write(linea)
            else:
                salir = True
                break

        if info_siguiente['has_next_page']:
            end_cursor = info_siguiente['end_cursor']
            params['variables'] = json.loads(params['variables'])
            params['variables']['first'] = 10
            params['variables']['after'] = end_cursor
            params['variables'] = json.dumps(params['variables'])
        else:
            salir = True
        time.sleep(5)
        print()
        
f_csv.close()

    # f = open('prueba.json', 'w', encoding='utf8')
    # json.dump(data, f, ensure_ascii=False)
    # f.close()