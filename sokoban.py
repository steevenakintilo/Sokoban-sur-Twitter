#!/usr/bin/env python3

import curses
from curses import wrapper
from random import randint  
import os
import sys
from os import system

import datetime
import tweepy
import logging
import time
import re

from main import *
from PIL import Image

def random_str(n1,n2):
    x = randint(n1,n2)
    return (x)

def random_line(files,n1,n2):
    lines = []
    rand_line = []
    with open(files) as f:
        lines = f.readlines()
        return(lines[random_str(n1,n2)])

def write_id(path,x):  
    f = open(path, "w")
    f.write(str(x))    
    f.close

def write_ids(path,x):  
    f = open(path, "a")
    f.write(str(x))    
    f.close  

def count_the_line(path):
    strs = print_file(path)
    line = 0
    for i in range(len(strs)):
        if strs[i] == "\n":
            line = line + 1
    return(line)

def print_file(path):
    f = open(path, 'r')
    content = f.read()
    return(content)
    f.close()

def get_pos(w,path):
    for i in range(char_nbr(path)):
        if w[i] == "🤠":
            write_id("pos",i)
            break

def get_posw(w,path):
    count = []
    for i in range(char_nbr(path)):
        if w[i] == "📦":
            count.append(i)
    return(count)

def get_line(w,path):
    for i in range(char_nbr(path)):
        if w[i] == "\n":
            return (i)
            break
def count_box(w,char,path):
    count = 0
    for i in range(char_nbr(path)):
        if w[i] == char:
            count = count + 1
    return (count)

def pos_hole(w,path):
    count = []
    for i in range(char_nbr(path)):
        if w[i] == "🟩":
            count.append(i)
    return (count)

def pos_box(w,path):
    count = []
    for i in range(char_nbr(path)):
        if w[i] == "📦":
            count.append(i)
    return (count)

def char_nbr(path):
    file = open(path, "r")
    data = file.read()
    num = len(data)
    return(num)

def split(word):
    return [char for char in word]

def print_corner(w,lenght):
    count = []
    for i in range(char_nbr(path)):
        if w[i] == "🟧" and w[i + 1] == "🟧" and w[i + lenght] == "🟧" and w[i + lenght + 1] == "📦":
            return (1)

def get_path_lvl(lvl):
    path = "map/level"+str(lvl)+".txt"
    return (path)

def uptade_map(path,w):
    map_p = ""
    for i in range(char_nbr(path)):
        map_p = map_p + w[i]
        get_pos(w,path)
    return(map_p)

def check_loose(path,w,lenght,hole_pos):
    for i in range(char_nbr(path)):
        if w[i] == "📦":
            if w[i-1] == "🟧" and w[i-lenght] == "🟧" and w[i-lenght+1] == "🟧" and w[i] not in hole_pos:
                return (1)
            if w[i-1] == "🟧" and w[i-lenght] == "🟧" and w[i-lenght-1] == "🟧" and w[i] not in hole_pos:
                return (1)
            if w[i+1] == "🟧" and w[i-lenght] == "🟧" and w[i-lenght+1] == "🟧" and w[i] not in hole_pos:
                return (1)
            if w[i-1] == "🟧" and w[i+lenght] == "🟧" and w[i+lenght+1] == "🟧" and w[i] not in hole_pos:
                return (1)
            if w[i+1] == "📦" and w[i-lenght] == "📦" and w[i-lenght-1] == "📦" and w[i] not in hole_pos:
                return (1)

def main(lvl,life,pause):
    highscore = print_file("highscore.txt")
    path = get_path_lvl(lvl)
    touch = 0
    open('box_pos', 'w').close()
    open('player_pos', 'w').close()
    #system("clear")
    word = print_file(path)
    w = split(word)
    ws = split(word)
    hole_pos = pos_hole(ws,path)
    write_id("hoole",hole_pos)
    l = get_line(w,path)
    lenght = int(l) + 1
    win = 0
    tries = 0
    reset_map = 1
    w_nbr = count_box(w,"📦",path)
    map_p = ""
    map_len_file = ""
    condition_once = 0
    tweet_once = 0
    first_move = 0
    saved_lvl = print_file("lvl.txt")
    saved_lvl = int(saved_lvl)
    SLEEP_TIME = 60
    end_level = 2
    while True:
        print("Inside")
        
        if first_move == 0:
            last_tweet = "go"
            first_move = 1
        else:
            last_tweet_pos = make_pos()
        
        if pause == 0:
            last_tweet_pos = "go"
            pause = 1
        map_len_file = print_file("map_len.txt")
        map_len = int(map_len_file)
        for i in range(char_nbr(path)):
            if len(map_p) != map_len and condition_once == 1:
                map_p = map_p + w[i]
                get_pos(w,path)
            else:
                if condition_once == 0:
                    map_p = map_p + w[i]
                    get_pos(w,path)
                else:
                    get_pos(w,path)
        saved_map = map_p
        write_id("save_map.txt",map_p)
        write_id("level.txt",lvl)
        psx = print_file("pos")
        pos = int(psx)
        box_pos = pos_box(w,path)
        posw = get_posw(w,path)
        write_id("hole",box_pos)
        for i in range(w_nbr):
            if condition_once == 0:
                write_id("map_len.txt",str(len(map_p)))
                condition_once = 1
        if last_tweet_pos == "up":
            touch = 0
            if w[pos] == "🤠" and w[pos - lenght] == "⬜":
                w[pos - lenght] = "🤠"
                w[pos] = "⬜"
                new_map = uptade_map(path,w)
                tries = tries + 1
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
            if w[pos] == "🤠" and w[pos - lenght] == "📦" and w[pos - lenght - lenght] != "🟧" and w[pos - lenght - lenght] != "📦":
                w[pos - lenght] = "🤠"
                w[pos - lenght - lenght] = "📦"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
            if w[pos] == "🤠" and w[pos - lenght] == "🟩" and w[pos - lenght - lenght] != "🟧":
                w[pos - lenght] = "🤠"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
            if pos in hole_pos and w[pos - lenght] != "🟧" and w[pos - lenght] != "📦":
                w[pos] = "🟩"
                w[pos - lenght] = "🤠"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
        
        if last_tweet_pos == "down":
            touch = 0
            if w[pos] == "🤠" and w[pos + lenght] == "⬜":
                w[pos + lenght] = "🤠"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
            if w[pos] == "🤠" and w[pos + lenght] == "📦" and w[pos + lenght + lenght] != "🟧" and w[pos + lenght + lenght] != "📦":
                w[pos + lenght] = "🤠"
                w[pos + lenght + lenght] = "📦"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""    
            if w[pos] == "🤠" and w[pos + lenght] == "🟩" and w[pos + lenght + lenght] != "🟧":
                w[pos + lenght] = "🤠"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_id("save_map.txt",new_map)
                write_ids("player_pos",str(pos) + "\n")
                map_p = ""
            if pos in hole_pos and w[pos + lenght] != "🟧" and w[pos + lenght] != "📦":
                w[pos + lenght] = "🤠"
                w[pos] = "🟩"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
    
        if last_tweet_pos == "left":
            touch = 0
            if first_move == 1:
                if w[pos] == "🤠" and w[pos - 1] == "⬜":
                    w[pos - 1] = "🤠"
                    w[pos] = "⬜"
                    tries = tries + 1
                    new_map = uptade_map(path,w)
                    write_ids("player_pos",str(pos) + "\n")
                    write_id("save_map.txt",new_map)
                    map_p = ""
        
                if w[pos] == "🤠" and w[pos - 1] == "📦" and w[pos -2] != "🟧" and w[pos - 2] != "📦":
                    w[pos - 1] = "🤠"
                    w[pos - 2] = "📦"
                    w[pos] = "⬜"
                    tries = tries + 1
                    new_map = uptade_map(path,w)
                    write_ids("box_pos",str(box_pos) + "\n")
                    write_ids("player_pos",str(pos) + "\n")
                    write_id("save_map.txt",new_map)
                    map_p = ""
        
                if w[pos] == "🤠" and w[pos - 1] == "🟩" and w[pos - 2] != "🟧":
                    w[pos - 1] = "🤠"
                    w[pos] = "⬜"
                    tries = tries + 1
                    new_map = uptade_map(path,w)
                    write_ids("player_pos",str(pos) + "\n")
                    write_id("save_map.txt",new_map)
                    map_p = ""
        
                if pos in hole_pos and w[pos - 1] != "🟧" and w[pos - 1] != "📦":
                    w[pos - 1] = "🤠"
                    w[pos] = "🟩"
                    tries = tries + 1
                    new_map = uptade_map(path,w)
                    write_ids("player_pos",str(pos) + "\n")
                    write_id("save_map.txt",new_map)
                    map_p = ""


        if last_tweet_pos == "right":
            touch = 0
            if w[pos] == "🤠" and w[pos + 1] == "⬜":
                w[pos + 1] = "🤠"
                w[pos] = "⬜"
                new_map = uptade_map(path,w)
                tries = tries + 1
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
    
            if w[pos] == "🤠" and w[pos + 1] == "📦" and w[pos + 2] != "🟧" and w[pos + 2] != "📦":
                w[pos + 1] = "🤠"
                w[pos + 2] = "📦"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
    
            if w[pos] == "🤠" and w[pos + 1] == "🟩" and w[pos + 2] != "🟧":
                w[pos + 1] = "🤠"
                w[pos] = "⬜"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
        
            if pos in hole_pos and w[pos + 1] != "🟧" and w[pos + 1] != "📦":
                w[pos + 1] = "🤠"
                w[pos] = "🟩"
                tries = tries + 1
                new_map = uptade_map(path,w)
                write_ids("box_pos",str(box_pos) + "\n")
                write_ids("player_pos",str(pos) + "\n")
                write_id("save_map.txt",new_map)
                map_p = ""
        if last_tweet_pos == "go":
            write_id("save_map.txt",map_p)
        if check_loose(path,w,lenght,hole_pos) == 1:
            win = 2
            if life == 1:
                end_level = 0
                saved_map = print_file("save_map.txt")
            else:
                new_map = uptade_map(path,w)
                write_id("save_map.txt",new_map)
                saved_map = print_file("save_map.txt")
                end_level = -1
        if count_box(w,"🟩",path) == 0 and pos not in hole_pos:
            win = 1
            lvl = lvl + 1
            new_map = uptade_map(path,w)
            write_id("save_map.txt",new_map)
            saved_map = print_file("save_map.txt")
            end_level = 1
            
        saved_map = print_file("save_map.txt")
        print(saved_map)
        #print(last_tweet_pos)
        #print(end_level)
        #time.sleep(345678)
        if end_level == 0:
            print("game overrrrrrrr")        
            try:
                make_tweet(saved_map,lvl,highscore,life)
                time.sleep(5)
                end_level_tweet(0,lvl,highscore,life)
                time.sleep(SLEEP_TIME)
            except:
                time.sleep(600)
            main(1,3,0)
            
        if end_level == 1:
            print("wiiiiiiiiin")
            try:
                make_tweet(saved_map,lvl,highscore,life)
                time.sleep(5)
                end_level_tweet(1,lvl,highscore,life)
                time.sleep(SLEEP_TIME)
            except:
                time.sleep(600)
            main(lvl,life,0)    
                    
        if end_level == -1:
            print("loooooooooooose")
            try:
                make_tweet(saved_map,lvl,highscore,life)
                time.sleep(5)
                end_level_tweet(-1,lvl,highscore,life)
                time.sleep(SLEEP_TIME)
            except:
                time.sleep(600)
            main(lvl,life - 1,0)    
        
        try:
            print("cococo")
            make_tweet(saved_map,lvl,highscore,life)
            if end_level == 2:
                time.sleep(SLEEP_TIME)
        except:
            time.sleep(10)
        
        #time.sleep(SLEEP_TIME)

main(1,3,0)
