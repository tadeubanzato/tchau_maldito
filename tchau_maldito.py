#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tchau_madito.py

'LOAD COMMON LIBRARIES'
import tweepy
import logging
import time
import os
import random
import pandas as pd
import sys
import os.path
from csv import writer
import pandas as pd

'IMPORT CREDENTIALS'
from credentials.credentials import *
from modules.gdrive import *

'LOAD LOGGIN'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Create PID number for verification
pid = str(os.getpid())
pidfile = "/tmp/maldito.pid"
if os.path.isfile(pidfile):
    print ("%s already exists, exiting" % pidfile)
    sys.exit()
# Caso contrário abre e salva o arquivo no diretório definido
f = open(pidfile, "w")
f.write(pid)

try:
    def get_gif(list_gif):
        res = os.listdir(list_gif)
        return f'{list_gif}{random.choice(res)}'

    def create_api():
        # Authenticate to Twitter
        logger.info("Authenticating API")
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        try:
            api.verify_credentials()
            logger.info("Authentication Successful")
        except:
            logger.info("Authentication Error")

        return api

    def check_mentions(api, keywords, since_id):
        # keywords =  ['Tchau Maldito', '#tchaumaldito']
        logger.info("Retrieving mentions")
        new_since_id = since_id

        names = []
        count = 0

        df_replies = pd.DataFrame(columns=['tweetID','screename','intweet'])
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
            file_name = 'replied/replied_maldito.csv'

            saved_list = pd.read_csv(file_name, on_bad_lines='skip')['tweetID'].drop_duplicates().tolist() #Open file

            # print(f'\nTWEET ID TADEU: {tweet.id}')
            # print(f'REPLY ID ORIGINAL: {tweet.in_reply_to_status_id}')
            # print(f'TWEET TEXT: {tweet.text}')
            #
            # print(f'Screen name: {tweet.user.screen_name}')
            # print(f'In Reply name: {tweet.in_reply_to_screen_name}')

            # df_replies = pd.read_csv('replied/replied_maldito.csv')
            names = [f'@{tweet.user.screen_name}',f'@{tweet.in_reply_to_screen_name}']
            list = [tweet.id,tweet.user.screen_name,tweet.in_reply_to_screen_name]
            # df_list = pd.read_csv(file_name)['tweetID'].tolist()
            # saved_df = pd.read_csv(file_name, on_bad_lines='skip')['tweetID'].drop_duplicates().tolist() #Open file

            if 'choraosonaro' in tweet.user.screen_name or tweet.id in saved_list:
                # logger.info(f'Already replied')
                continue
            elif '@choraosonaro' in tweet.text and any(keyword.lower() in tweet.text.lower() for keyword in keywords):
                # print('Reply')
                logger.info(f'Rplying to @{tweet.user.screen_name}')
                try:
                    if 'gado' in tweet.text.lower():
                        filename = get_gif('gifs/gado/')
                        frases = ['só podia ser GADO 🐮!', 'não tem como não ser GADO 🐮 né!?', 'GADO 🐮 é pouco né!', 'GADO 🐮 maldito', 'insuportavelmente gado 🐮', 'em GADO 🐮 we trust', 'nunca enganou 🐮', 'esse aí apertou 17 certeza 🐮', 'esse ai vai apertar 22 certeza 🐮']
                    else:
                        filename = get_gif('gifs/malditos/')
                        frases = ['tchau Bolsonaro seu Maldito!', 'esse Bolsonaro tem que ir logo. Tchau Maldito!', 'os bolsonaristas estão ficando desesperado. Tchau Maldito!', 'esse Bolsonaro é realmente um MALDITO!', 'tchau Bozo, seu Maldito']

                    media = api.media_upload(filename)

                    # api.update_status('@' + mention.user.screen_name + " Here's your Quote", mention.id, media_ids=[media.media_id])
                    # api.update_status(status=f'Ae, {" ".join(names)} Tchau Maldito!', in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)
                    emojis = ['✌️', '👋', '👍','✊','🤜','💀','😏','😷','😎','🤬','🥹','🙂','🤟']
                    intro = ['Ae', 'Salve', 'Valeu', 'TMJ', 'Firmeza', 'Qualé', 'E aí']
                    hashtags = ['#ForaBolsonaro', '#BolsonaroGenocida', '#BolsonaroVagabundo', '#BolsonaroLadrao', '#BolsonaroCorrupto', '#BolsonaroFacista', '#BolsonaroMentiroso']
                    status = f'{random.choice(intro)} {random.choice(emojis)}, {" e ".join(names)} {random.choice(frases)} {" ".join(random.sample(hashtags, 2))}'
                    api.update_status(status=status, in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)

                    df_replies.loc[len(df_replies.index)] = {'tweetID':tweet.id, 'screename':tweet.user.screen_name, 'intweet':tweet.in_reply_to_screen_name}

                    saved_df = pd.read_csv(file_name, on_bad_lines='skip').drop_duplicates() #Open file
                    frames = [df_replies, saved_df]
                    df_final = pd.concat(frames)
                    df_final.to_csv(file_name, encoding='utf-8-sig',index=False)

                    logger.info(f'Uploading updates to Gdrive')
                    file = drive.CreateFile({'title': 'replied_maldito.csv','id': '1yKqHm2B3IVayojiMHEZH435A0KMDrcol'})
                    file.SetContentFile('replied/replied_maldito.csv')
                    file.Upload()
                    f = None
                except:
                    print('Already Replied to this one')

            else:
                continue

        return new_since_id

    def main():
        api = create_api()
        since_id = 1
        while True:
            try:
                keywords = ['Maldito', '#tchaumaldito', 'lula', 'gado', 'boi']
                since_id = check_mentions(api, keywords, since_id)
                logger.info('Waiting')
                time.sleep(60*2)
            except:
                logger.info(f'WAITING FOR TIME OUT')
                time.sleep(60)

    if __name__ == '__main__':
        file_name = 'replied/replied_maldito.csv'
        if os.path.exists(file_name):
            os.remove(file_name)
        file = drive.CreateFile({'id': '1yKqHm2B3IVayojiMHEZH435A0KMDrcol'})
        file.GetContentFile(file_name) # Download file as 'catlove.png'
        main()

finally:
    # Finaliza o arquivo PID
    os.unlink(pidfile)
