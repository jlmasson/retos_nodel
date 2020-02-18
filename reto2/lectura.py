import json
import datetime
import pandas as pd
import csv

f_csv = open("prueba.csv", "w", encoding='utf8')
spamwriter = csv.writer(f_csv, quoting=csv.QUOTE_MINIMAL)
f_csv.write('LinkPost,Fecha,Content,Likes,Comments,UserId\n')
f = open('prueba.json', 'r', encoding='utf8')
data = json.loads(f.read(), encoding='utf8')

maximo = int(datetime.datetime(2019,12,1,23,59,59).timestamp())
minimo = int(datetime.datetime(2019,10,1,0,0,0).timestamp())

info_posts_recientes = data['graphql']['hashtag']['edge_hashtag_to_media']
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

    # if (timestamp_post >= minimo and timestamp_post <= maximo):
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

    if info_siguiente['has_next_page']:
        end_cursor = info_siguiente['end_cursor']

f.close()
f_csv.close()

f2 = open('procesada_prueba.json', 'w', encoding='utf8')
json.dump(data_procesada, f2, ensure_ascii=False, indent=4)
f2.close()

df = pd.read_csv('prueba.csv')
print(df)