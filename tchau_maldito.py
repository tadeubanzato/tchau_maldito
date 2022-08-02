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

'IMPORT CREDENTIALS'
from credentials.credentials import *

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
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():

            # print(f'\nTWEET ID TADEU: {tweet.id}')
            # print(f'REPLY ID ORIGINAL: {tweet.in_reply_to_status_id}')
            # print(f'TWEET TEXT: {tweet.text}')
            #
            # print(f'Screen name: {tweet.user.screen_name}')
            # print(f'In Reply name: {tweet.in_reply_to_screen_name}')


            names = [f'@{tweet.user.screen_name}',f'@{tweet.in_reply_to_screen_name}']

            file_name = 'replied/replied_maldito.csv'
            list = [tweet.id,tweet.user.screen_name,tweet.in_reply_to_screen_name]
            df_list = pd.read_csv(file_name)['tweetID'].tolist()

            if 'choraosonaro' in tweet.user.screen_name or tweet.id in df_list:
                continue
            elif '@choraosonaro' in tweet.text and any(keyword.lower() in tweet.text.lower() for keyword in keywords):
                # print('Reply')
                logger.info(f"Rplying to @{tweet.user.screen_name}")

                try:
                    if 'gado' in tweet.text.lower():
                        filename = get_gif('gifs/gado/')
                        frases = ['só podia ser esse GADO!', 'não tem como não se Gado né!?', 'gado é poco né!', 'gado maldito']
                    else:
                        filename = get_gif('gifs/malditos/')
                        frases = ['Tchau Bolsonaro seu Maldito!', 'Esse Bolsonaro tem que ir logo. Tchau Maldito!', 'Os bolsonaristas estão ficando desesperado. Tchau Maldito!', 'Esse Bolsonaro é realmente um MALDITO!', 'Tchau Bozo, seu Maldito']

                    media = api.media_upload(filename)

                    # api.update_status('@' + mention.user.screen_name + " Here's your Quote", mention.id, media_ids=[media.media_id])
                    # api.update_status(status=f'Ae, {" ".join(names)} Tchau Maldito!', in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)
                    intro = ['👍 ae', 'Salve 😅', '🖖 valeu', 'TMJ 🥸', 'Firmeza 👋', 'Qualé 🤜', 'E aí 🤟']
                    hashtags = ['#ForaBolsonaro', '#BolsonaroGenocida', '#BolsonaroVagabundo', '#BolsonaroLadrao', '#BolsonaroCorrupto', '#BolsonaroFacista', '#BolsonaroMentiroso']
                    status = f'{random.choice(intro)}, {" ".join(names)} {random.choice(frases)}\n{" ".join(random.sample(hashtags, 2))}'
                    api.update_status(status=status, in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)

                    with open(file_name, 'a', newline='') as f_object:
                        # Pass the CSV  file object to the writer() function
                        writer_object = writer(f_object)
                        writer_object.writerow(list)
                        f_object.close()

                    # {tweet.user.screen_name}
                    # filename = f'gifs/{get_gif()}'
                    # media = api.media_upload(filename)
                    # api.update_status(status='Tchau Maldito!', in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)

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
        main()

finally:
    # Finaliza o arquivo PID
    os.unlink(pidfile)
