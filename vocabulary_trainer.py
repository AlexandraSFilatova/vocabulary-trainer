# -*- coding: utf-8 -*-
"""
Project is in progress.
This code works with .csv files FROM LOCAL DERICTORIES.
Files contain following structure: Date add, Word, Translation, Date of the last training, Training status, Number of training.


Date add - date when a word was added

Word - word in English

Translation - word in Russian

Date of the last training - Date of the last training

Training status - L means "learned", T means "need to train"

Number of training - Number of training. Default number MUST BE 0
"""

from asyncio.windows_events import NULL
import io
import os
from IPython.display import Audio
import gtts
from IPython.display import display
from os import listdir
from os.path import isfile, join, exists
import pandas as pd
import random
from datetime import date
from playsound import playsound


# To play audio text-to-speech during execution
def speak(my_text):
    file_name = my_text + ".mp3"
    full_file_path = os.path.abspath(os.getcwd()) + "\\gtts\\"+file_name
    if not exists(full_file_path):     
        tts = gtts.gTTS(text=my_text, lang='en')
        tts.save(full_file_path)
        
        
    playsound(full_file_path)


#exercise 1 given a word in russian, choose the right variant in english from listed
def ex_1(translation):
    print(translation)
    print("\n")
    options = vocabulary["Word"].sample(n=3).to_list()
    options.append(dic_tw[translation])
    random.shuffle(options)
    print(options)
    print("\n")
    user_variant = str(input())
    if user_variant.strip() == dic_tw[translation].strip():
        return print("Correct!")
    else:
        return print("False, the correct answer is " + dic_tw[translation])

#exercise 2 given a word in english, choose the right variant in russian from listed
def ex_2(word):
    print(word)
    print("\n")
    options = vocabulary["Translation"].sample(n=3).to_list()
    options.append(dic_wt[word])
    random.shuffle(options)
    print(options)
    print("\n")
    user_variant = str(input())
    if user_variant.strip() == dic_wt[word].strip():
        return print("Correct!")
    else:
        return print("False, the correct answer is " + dic_wt[word])

#exercise 3  given a word in russian, compose the word in english from listed letters
def ex_3(translation):
    print(translation)
    print("\n")
    word = list(dic_tw[translation])
    random.shuffle(word)
    print(word)   
    print("\n")
    user_variant = str(input())
    if user_variant.strip() == dic_tw[translation].strip():
        return print("Correct!")
    else:
        return print("False, the correct answer is " + dic_tw[translation])

#exercise 4  given an audio, write the word in english
def ex_4(word):
    speak(word)
    print("\n")
    user_variant = str(input())
    if user_variant.strip() == word.strip():
        return print("Correct!")
    else:
        return print("False, the correct answer is " + word)

#training
def training():
    input("Press Enter to start train")
    print("You will train these words/phrases")

    for word in t_words:
        print(word + " - " + dic_wt[word])
        speak(word)
        input()

    ###exercise 1
    print("Exercise 1. Write the correct variant in english from listed")
    print("\n")
    random.shuffle(t_words)
    for translation in t_translate:
        ex_1(translation)
        print("\n")
    
    ###exercise 2
    print("Exercise 2. Write the correct variant in russian from listed")
    print("\n")
    random.shuffle(t_words)
    for word in t_words:
        ex_2(word)
        print("\n")
    
    ###exercise 3
    print("Exercise3. Write the correct translation in English from letters below")
    print("\n")
    random.shuffle(t_translate)
    for translation in t_translate:
        ex_3(translation)
        print("\n")

    ###exercise 4
    print("Exercise 4. Write the word in English")
    print("\n")
    random.shuffle(t_words)
    for word in t_words:
        ex_4(word)
        print("\n")




def Step6():#Step 6. File rewrite. Rewrite changed status and last training date
    vocabulary.to_csv(os.path.join(folder_path, t_file), 
                    index=False, 
                    encoding="utf-8-sig")







#Step 1. File selection for training.

folder_path = os.path.join(os.path.abspath(os.getcwd()), "Content")
files = [f for f in listdir(folder_path) 
            if isfile(join(folder_path, f))] ##list files in folder
print("Choose the file's number, which you want to train:")
for file in files:
    print(str((files.index(file)+1)) + " - " + file)

file_number = int(input("Enter the number: "))
t_file = files[file_number -1]                                               #file under study
vocabulary = pd.read_csv(os.path.join(folder_path, t_file)) #read file and create DF


#Step 1.1. Checking if any words need to be trained. These words are all words with a status "T". 
# The first 3 trainings will be every day, all next ones will be every 2 days until words` status will change to "L". This part of the code will check words 
# and ask about a repetition of words, if no, then it goes to the main training, if yes, it provides repetition, and then ask about the main training.
try:
    df_sample = vocabulary[(vocabulary["Training status"]=="T")&(vocabulary["Date of the last training"].notnull())].filter(items = ["Word", "Translation","Date of the last training","Number of training"]) 
    df_sample["Date_diff"] = pd.to_numeric((date.today() - pd.to_datetime(df_sample["Date of the last training"]).dt.date).dt.days, downcast='integer')
    df_sample = df_sample[(((df_sample["Number of training"] < 3)&(df_sample["Date_diff"] >= 1) )| ((df_sample["Number of training"] >= 3)&(df_sample["Date_diff"] >= 2)))].sample(n=5)
    #random 5 unlearned words from file under study
except:
    df_sample = vocabulary[(vocabulary["Training status"]=="T")&(vocabulary["Date of the last training"].notnull())].filter(items = ["Word", "Translation","Date of the last training","Number of training"])
    df_sample["Date_diff"] = pd.to_numeric((date.today() - pd.to_datetime(df_sample["Date of the last training"]).dt.date).dt.days, downcast='integer') 
    df_sample = df_sample[(((df_sample["Number of training"] < 3)&(df_sample["Date_diff"] >= 1) )| ((df_sample["Number of training"] >= 3)&(df_sample["Date_diff"] >= 2)))]
    #all unlearned words from file under study, when word`s amount is less than 5
t_words = df_sample["Word"].to_list()                                          #sample to train 
t_translate = df_sample["Translation"].to_list()                                      #translation of sample to train
    
dic_wt = dict(zip(t_words, t_translate)) #dic word:translation
dic_tw = dict(zip(t_translate, t_words)) #dic translation:word

if not t_words:
    print("There are no words to repeat. Go to the main training.")
else:
    print("There are words to repeat. Do you want to repeat them? yes/no")
    user_choice = str(input())
    if user_choice.lower() == "yes":
                    #Step 1.3. Training.
            user_continue = "yes"
            while (user_continue.lower() == "yes"):
                training()
                #Step 1.4-1.5. Ask to repeat training and to change training status.
                print("Do you want to repeat training with these words? yes/no")
                user_continue = str(input())
                print("\n")
                
            print("Have you learned any of these words? yes/no")
                ##chosen words won`t be participate in futher trainings
            print("\n")
            for word in t_words:
                vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Date of the last training"] = date.today()
                vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Number of training"] += 1
                print(word)
                print("\n")
                user_choice = str(input())
                print("\n")
                if user_choice.lower() == "yes":
                    vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Training status"] = "L"
                elif user_choice == "no":
                    print("The word will be trained in further training")
                else:
                    print("Incorrect choice. Please write yes or no")
            print("Repeating is over. Do you want to Lear new words?yes/no")
            user_choice = str(input())
            if user_choice.lower() == "no":
                Step6() #rewrite changes in file 
                quit()


#Step 2. Sample formation.
try:
    df_sample = vocabulary[(vocabulary["Training status"]=="T")&(vocabulary["Date of the last training"].isnull())].filter(items = ["Word", "Translation"]).sample(n=5) 
    #random 5 unlearned words from file under study
except:
    df_sample = vocabulary[(vocabulary["Training status"]=="T")&(vocabulary["Date of the last training"].isnull())].filter(items = ["Word", "Translation"]) 
    #all unlearned words from file under study, when word`s amount is less than 5
t_words = df_sample["Word"].to_list()                                          #sample to train 
t_translate = df_sample["Translation"].to_list()                                      #translation of sample to train
    
dic_wt = dict(zip(t_words, t_translate)) #dic word:translation
dic_tw = dict(zip(t_translate, t_words)) #dic translation:word

#Step 3. Training.
user_continue = "yes"
while (user_continue.lower() == "yes"):
    training()
    #Step 4-5. Ask to repeat training and to change training status.
    print("Do you want to repeat training with these words? yes/no")
    user_continue = str(input())
    print("\n")
    
print("Have you learned any of these words? yes/no")
    ##chosen words won`t be participate in futher trainings
print("\n")
for word in t_words:
    vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Date of the last training"] = date.today()
    vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Number of training"] += 1
    print(word)
    print("\n")
    user_choice = str(input())
    print("\n")
    while user_choice.lower() !=  "yes" and user_choice.lower() != "no":
        print("Incorrect choice. Please write yes or no.")
        user_choice = str(input())
    if user_choice.lower() == "yes":
        vocabulary.loc[vocabulary[vocabulary["Word"] == word].index, "Training status"] = "L"
    elif user_choice == "no":
        print("The word will be trained in further training")
        
print("Training is over.")


Step6()

