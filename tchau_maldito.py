#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tchau_madito.py

from dotenv import load_dotenv

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
import datetime
from datetime import timedelta
import time


# Create PID number for verification
pid = str(os.getpid())
pidfile = "/tmp/maldito.pid"
if os.path.isfile(pidfile):
    print ("%s already exists, exiting" % pidfile)
    sys.exit()
# Save file
f = open(pidfile, "w")
f.write(pid)

try:
    ## Load loggin
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    def get_API():
        logger.info("Authenticating API")
        auth = tweepy.OAuthHandler(os.getenv('api_key'), os.getenv('api_secret_key'))
        auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
        api = tweepy.API(auth)

        try:
            api.verify_credentials()
            logger.info("Authentication Successful")
        except:
            logger.info("Authentication Error")

        return api

    def get_gif(list_gif):
        res = os.listdir(list_gif)
        return f'{list_gif}{random.choice(res)}'


    def faltam():
        today = datetime.date.today()
        future = datetime.date(2022,10,2)
        faltam = future - today
        return faltam.days


    def check_mentions(api, keywords, mentions):
        file_name = 'replied/replied_maldito.csv'
        logger.info("Retrieving mentions")

        ## Open replied DB and convert to list
        df_replies = pd.read_csv(file_name, on_bad_lines='skip')
        replied_list = df_replies['replied_to'].tolist()

        for tweet in mentions:
            ## Check if already replied
            if any(keyword in tweet.text.lower() for keyword in keywords) and tweet.id not in replied_list and tweet.in_reply_to_status_id not in replied_list:
                replied_to = tweet.id if tweet.in_reply_to_status_id is None else tweet.in_reply_to_status_id
                # print(tweet.truncated)
                # print(f'\n{"-"*20} POST INFO {"-"*20}\n')
                # print(f'Truncated: {tweet.truncated}')
                # print(f'Time < 3 hours')
                # print(f'With @choraosonaro')
                # print(f'https://twitter.com/choraosonaro/status/{tweet.id}')
                # print(f'tweet.in_reply_to_status_id_str: {tweet.in_reply_to_status_id_str}')
                # print(f'tweet.in_reply_to_status_id: {tweet.in_reply_to_status_id}')

                # >>>> TEST EACH MENTION <<<<<<
                # tweets = api.mentions_timeline(count = 1)
                # replied_to = x[0].id if x[0].in_reply_to_status_id is None else 'x[0].in_reply_to_status_id'

                if not tweet.user.following:
                    tweet.user.follow()

                logger.info(f"Answering to {tweet.user.name}")

                ## Get screen names
                handlers = [f'@{tweet.user.screen_name}',f'@{tweet.in_reply_to_screen_name}']
                names = " e ".join(handlers) if len(handlers) >= 2 else " ".join(handlers)

                filename = get_gif('gifs/malditos/')
                media = api.media_upload(filename)

                ponome = ['essa é uma corja', 'só tem', 'é muito', 'bolsonarista é tudo', 'é tudo um bando de', 'só é um baita', 'isso é um baita', 'muita gente', 'tudo', 'um bando de']
                adjetivo = ['idiota', 'imbecíl', 'animal', 'trouxa', 'energumeno', 'estúpido', 'fanático', 'extremista', 'facista', 'mal caráter', 'engodo', 'neo liberalista retrogrado']
                despedida = [f'Tchau MADITO falta só {faltam()} dias', 'VTNC seu Maldito', f'Falta só {faltam()} dias pra darmos Adeus a esse Maldito', f'É o fim da linha para esses maltidos, faltam {faltam()} dias', f'Está acabando malditos em {faltam()} nos falamos', f'Hora contada para acabar com esses malditos, mais específico {faltam()} dias', f'Faltam {faltam()} dias pra acabar com esses malditos', 'Esses malditos serão presos', f'É o ultimo respido desses malditos em {faltam()} falamos novamente', f'Esses malditos estão com os dias contados, {faltam()} dias precisamente', f'Espero que em {faltam()} diremos Tchau Maldito para essa corja', f'Estamos torcendo pra que em {faltam()} tudo acabe']
                emojis = ['✌️', '👋', '👍','✊','🤜','💀','😏','😷','😎','🤬','🥹','🙂','🤟']
                intro = ['E aí', 'Salve', 'Tranquilinho', 'Suave', 'De boas', 'TMJ', 'É nóis', 'Coé', 'Ae', 'Qualé', 'Firma', 'Firmeza', 'Sussa', 'Valeu', 'Manda', 'Tranquilo']
                hashtags = ['#ForaBolsonaro', '#BolsonaroGenocida', '#BolsonaroVagabundo', '#BolsonaroLadrao', '#BolsonaroCorrupto', '#BolsonaroFacista', '#BolsonaroMentiroso']

                status = f'{random.choice(intro)} {random.choice(emojis)}, {names} {random.choice(ponome)} {random.choice(adjetivo)}. {random.choice(despedida)} {random.choice(emojis)} {" ".join(random.sample(hashtags, 2))}'
                api.update_status(status=status, in_reply_to_status_id = tweet.id, media_ids=[media.media_id], auto_populate_reply_metadata=True)

                ## Add Replied ID to Validation sheet
                df_replies.loc[len(df_replies.index)] = {'replied_to':replied_to}
                df_replies.to_csv(file_name, encoding='utf-8-sig',index=False)


    if __name__ == "__main__":
        load_dotenv() #load configs from .env
        api = get_API()
        mentions = tweepy.Cursor(api.mentions_timeline).items()
        check_mentions(api, ["maldito", "idiota"], mentions)

finally:
    # Finaliza o arquivo PID
    os.unlink(pidfile)
