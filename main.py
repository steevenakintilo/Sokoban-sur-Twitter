#!/usr/bin/env python3

import tweepy
import logging
from os import system
import sys
import time

class token_id:
    BEAR_KEY= "xxxx"
    API_KEY = "xxxx"                                
    API_SECRET = "xxxx"    
    ACCESS_TOKEN = "xxxx"  
    ACCESS_TOKEN_SECRET = "xxxx"

def write_id(path,x):  
    f = open(path, "w")
    f.write(str(x))    
    f.close  

def print_file(path):
    f = open(path, 'r')
    content = f.read()
    return(content)
    f.close()

def transfo_tweet(last_tweet):
    str_tweet=""
    num_list = []
    better_list = []
    for i in range(len(last_tweet)):
        #print(last_tweet[i])
        str_tweet = str_tweet + str(last_tweet[i])
    str_tweet = str_tweet.split("options=")
    new_str = str_tweet[1]
    new_str = new_str.split(" ")
    for i in range(len(new_str)):
        #print(new_str[i])
        if "votes" in new_str[i]:
            num_list.append(new_str[i + 1])
    for i in range(len(num_list)):
        better_list.append(get_num(num_list[i]))
    return(better_list)

def get_num(s):
    num = "0123456789"
    nb = ""
    for i in range(len(s)):
        if s[i] in num:
            nb = nb + s[i]
    return(nb)

def get_last_tweet_id(api):
    username = "Sokoban_GameBot"
    tweets = api.user_timeline(screen_name=username,count=200,include_rts = False,tweet_mode = 'extended')
    all_tweets = []
    all_tweets.extend(tweets) 
    a = all_tweets[0].full_text
    idd = all_tweets[0].id
    
    b = all_tweets[1].full_text
    idd2 = all_tweets[1].id
    #print(a,b)
    for i in range(len(all_tweets)):
        if '🤠' in all_tweets[i].full_text and '🟧' in all_tweets[i].full_text and '⬜' in all_tweets[i].full_text and '🟩' in all_tweets[i].full_text and '📦' in all_tweets[i].full_text:
            return (all_tweets[i].id)
        elif '🤠' in all_tweets[i].full_text and '🟧' in all_tweets[i].full_text and '⬜' and '📦' in all_tweets[i].full_text:
            return (all_tweets[i].id)

def return_next_move(get_result,ok):
    #print(get_result)
    pos = ["left","right","down","up"]
    zipped_lists = zip(get_result,pos)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    if ok == "ok":
        if len(set(list1)) == 1:
            print("no vote")
            return("go")
        else:
            return(list2[3])
    else:
        return("go")
    
def append_string(level,space,highscore,life):
    description_text = ""
    niv = "Niveau: "
    rec = "Record: "
    vie = "Nombre de vie: "
    for i in range(len(vie)):
        description_text = description_text + str(vie[i])
    for i in range(len(life)):
        description_text = description_text + str(life[i])
    description_text = description_text + " "
    for i in range(len(niv)):
        description_text = description_text + str(niv[i])
    for i in range(len(level)):
        description_text = description_text + str(level[i])
    for i in range(len(space)):
        description_text = description_text + space[i]
    for i in range(len(rec)):
        description_text = description_text + str(rec[i])
    for i in range(len(highscore)):
        description_text = description_text + str(highscore[i])
    return (description_text)
    
def make_tweet(game_map,level,highscore,life):
    space = "\n"
    token = token_id()
    auth = tweepy.OAuthHandler(token.API_KEY, token.API_SECRET)
    auth.set_access_token(token.ACCESS_TOKEN, token.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    c = tweepy.Client(token.BEAR_KEY,token.API_KEY,token.API_SECRET,token.ACCESS_TOKEN,token.ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
    user_id=1491722004738854913
    button = ["⬅️","➡️","⬇️","⬆️"]
    description_text = append_string(str(level),space,str(highscore),str(life))
    c.create_tweet(text=game_map,poll_duration_minutes=15,poll_options=button)
    api.update_profile(description=description_text)
    
def end_level_tweet(win,level,highscore,life):
    highscore = print_file("highscore.txt")
    high = int(highscore)
    if (level > high):
        write_id("highscore.txt",str(level))
    space = "\n"
    token = token_id()
    auth = tweepy.OAuthHandler(token.API_KEY, token.API_SECRET)
    auth.set_access_token(token.ACCESS_TOKEN, token.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    c = tweepy.Client(token.BEAR_KEY,token.API_KEY,token.API_SECRET,token.ACCESS_TOKEN,token.ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
    user_id=1491722004738854913
    button = ["⬅️","➡️","⬇️","⬆️"]
    w = "Le niveau est gagné ✅"
    l = "Le niveau est perdu ❌"
    g = "Tu n'as plus de vie retour au niveau 1 ☠️"
    if win == -1 or win == 0:
        life = life - 1
    if win == 1:
        txt = w
    if win == -1:
        txt = l
    if win == 0:
        txt = g
    description_text = append_string(str(level),space,str(highscore),str(life))
    print(get_last_tweet_id(api))
    c.create_tweet(text=txt,in_reply_to_tweet_id=get_last_tweet_id(api))
    api.update_profile(description=description_text)

def make_pos():
    token = token_id()
    auth = tweepy.OAuthHandler(token.API_KEY, token.API_SECRET)
    auth.set_access_token(token.ACCESS_TOKEN, token.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    c = tweepy.Client(token.BEAR_KEY,token.API_KEY,token.API_SECRET,token.ACCESS_TOKEN,token.ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
    button = ["⬅️","➡️","⬇️","⬆️"]
    idd = get_last_tweet_id(api)
    user_id=1491722004738854913
    empty_list = ["go","go","go","go"]
    last_tweet = c.get_tweet(id=idd,expansions=["attachments.poll_ids"])
    try:
        get_result = transfo_tweet(last_tweet)
        next_move = return_next_move(get_result,"ok")
    except:
        next_move = return_next_move(empty_list,"go")    
    return(next_move)