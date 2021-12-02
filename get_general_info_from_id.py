import requests
import os
import json
import csv
import time as ntime

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAANNQVAEAAAAA6NM%2BmUWeRRkLkEH58q3TYvcm5yY%3DvN8CbuK8mQDGRuT1hOf2FcpVIVYAn9ifvN45ORsjWrr4QTKHUf'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAA9RVAEAAAAAkqH3rjfzTAWLzq9yw6rvViC6cG8%3DIl8jZNyBShpZoKiixP9LkSGuHRZelFJpwjuAGy06YUcRxStkVS'

general_term = ['USA', 'America', 'United States']
states_short = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',\
                'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',\
                'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
states_long = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',\
               'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',\
               'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',\
               'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New hampshire', 'New jersey', 'New mexico', 'New York',\
               'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode island',\
               'South carolina', 'South dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',\
               'West Virginia', 'Wisconsin', 'Wyoming']
total_term = general_term + states_short + states_long

token_list = [0 for _ in range(3)]
token_list[0] = 'AAAAAAAAAAAAAAAAAAAAANhQVAEAAAAA4n4o%2FcuIN6qeVQuNtWqxArgqLmA%3Dng3Pkt0gZFAAKkn0pswTHoOd77MpiS7tMeVKGQlO4edu2CFqqH'
token_list[1] = 'AAAAAAAAAAAAAAAAAAAAANNQVAEAAAAA6NM%2BmUWeRRkLkEH58q3TYvcm5yY%3DvN8CbuK8mQDGRuT1hOf2FcpVIVYAn9ifvN45ORsjWrr4QTKHUf'
token_list[2] = 'AAAAAAAAAAAAAAAAAAAAAA9RVAEAAAAAkqH3rjfzTAWLzq9yw6rvViC6cG8%3DIl8jZNyBShpZoKiixP9LkSGuHRZelFJpwjuAGy06YUcRxStkVS'
bearer_token = token_list[0]
time = 0
token_idx = 0
# 1.AAAAAAAAAAAAAAAAAAAAANhQVAEAAAAA4n4o%2FcuIN6qeVQuNtWqxArgqLmA%3Dng3Pkt0gZFAAKkn0pswTHoOd77MpiS7tMeVKGQlO4edu2CFqqH
# 2.AAAAAAAAAAAAAAAAAAAAANNQVAEAAAAA6NM%2BmUWeRRkLkEH58q3TYvcm5yY%3DvN8CbuK8mQDGRuT1hOf2FcpVIVYAn9ifvN45ORsjWrr4QTKHUf
# 3.AAAAAAAAAAAAAAAAAAAAAA9RVAEAAAAAkqH3rjfzTAWLzq9yw6rvViC6cG8%3DIl8jZNyBShpZoKiixP9LkSGuHRZelFJpwjuAGy06YUcRxStkVS
# rate limit: 300 query / 15minutes
def create_url_tweet(id_list):
    tweet_fields = "tweet.fields=lang,geo,author_id"
    place_fields = "place.fields=country,geo"
    expansions = "expansions=geo.place_id"''
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = 'ids='
    for i, id in enumerate(id_list):
        if i == len(id_list) - 1:
            ids = ids + id
        else:
            ids = ids + id + ','
    # print(ids)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}&{}&{}".format(ids, expansions, tweet_fields, place_fields)
    return url

# rate limit: 300 query / 15minutes
def create_url_user(id_list):
    user_fields = "user.fields=location"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = 'ids='
    for i, id in enumerate(id_list):
        if i == len(id_list) - 1:
            ids = ids + id
        else:
            ids = ids + id + ','
    # print(ids)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/users?{}&{}".format(ids, user_fields)
    return url

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def onehour(str_in, str_out):
    # f1 = open('coronavirus-tweet-id-2020-08-01-00.txt', 'r')
    # csvfile = open('output.csv', 'wt', newline='')
    global bearer_token, time, token_idx, token_list
    f1 = open(str_in, 'r')
    csvfile = open(str_out, 'wt', newline='')
    writer = csv.writer(csvfile, delimiter=",")
    total_len = 0
    csvcol_real_1 = []
    csvcol_real_2 = []
    csvcol_real_3 = []
    while True:
        csvcol1 = []
        csvcol2 = []
        csvcol3 = []
        id_list = []
        time += 1
        if time % 100 == 0:
            print(time)
        if time % 300 == 0:
            token_idx += 1
            if token_idx == 3:
                token_idx = 0
                ntime.sleep(150)
            bearer_token = token_list[token_idx]
            print(token_idx)
            print(bearer_token)
        for j in range(100):
            line = f1.readline().strip()
            id_list.append(line)
        url = create_url_tweet(id_list)
        json_response = connect_to_endpoint(url)
        if 'data' in json_response.keys():
            for json_response in json_response['data']:
                if json_response['lang'] == 'en':
                    csvcol1.append(json_response['id'])
                    csvcol2.append(json_response['text'].replace('\n', ' '))
                    csvcol3.append(json_response['author_id'])
        url = create_url_user(csvcol3)
        json_response = connect_to_endpoint(url)
        for j in range(len(json_response['data'])):
            if 'location' in json_response['data'][j]:
                location_str = json_response['data'][j]['location']
                flag = False
                for term in total_term:
                    if term in location_str:
                        flag = True
                        break
                if flag:
                    csvcol_real_1.append(csvcol1[j])
                    csvcol_real_2.append(csvcol2[j])
                    csvcol_real_3.append(location_str)
                    total_len += 1
                    if total_len == 1500:
                        writer.writerows(zip(csvcol_real_1, csvcol_real_2, csvcol_real_3))
                        csvfile.close()
                        f1.close()
                        return


if __name__ == "__main__":
    bearer_token = token_list[0]
    # 8月31天
    # 一次处理5天吧
    # 已经处理
    #
    for day in range(1, 32):
        # 每天24h
        for hour in range(0, 24):
            # if day == 15 and hour == 22:
            #     continue
            if day < 10:
                day_str = '0' + str(day)
            else:
                day_str = str(day)
            if hour < 10:
                hour_str = '0' + str(hour)
            else:
                hour_str = str(hour)
            str_in = '2020-07/coronavirus-tweet-id-2020-07-' + day_str + '-' + hour_str + '.txt'
            str_out = '2020-07-output/coronavirus-tweet-id-2020-07-' + day_str + '-' + hour_str + '.csv'
            if os.path.exists(str_out):
                out_line = len(open(str_out, 'r').readlines())
                if out_line >= 1500:
                    continue
            print(str_in)
            print(str_out)
            print(ntime.strftime("%Y-%m-%d %H:%M:%S", ntime.localtime()))
            onehour(str_in, str_out)
    # str_in = '2020-08/coronavirus-tweet-id-2020-08-01-00.txt'
    # str_out = '2020-08-output/tweet-data-2020-08-01-00.csv'
    # onehour(str_in, str_out)
    # url = create_url(['1289350107960193025'])
    # json_response = connect_to_endpoint(url)
    # print(json_response)