import pandas as pd
import numpy as np
import random
import math
from numpy.random import choice

def preprocessing(df): #delete every response and tweets containing an internet link
    index_to_drop=[]
    for k in df.index:
        s=df.at[k,"Tweet"]
        if ("@" in s) or ("http" in s):
            index_to_drop.append(k)

    df=df.drop(index_to_drop)
    df=df.drop(columns="Unnamed: 0")
    return(df)

def split_tweets(df): #df : tweets DataFrame 
    words=[] #contains every words from every tweet on the training set

    for tweet in df["Tweet"]:
        for x in tweet.split():
            if "https" not in x: #we delete every link to websites
                words.append(x)
    
    return(words)

def get_weight():
    df=pd.DataFrame(columns = ['l1+l2','next','l1+l2+next','freq'],dtype=object)
    #l1+l2 : all the words and its following on the training sample 
    #follow : df.at[i,'next'] is the word following df.at[i,'l1+l2'] in the training sample
    #freq : the frequency with which "next" follow l1+l2 
    return(df)


def get_columns(words,df): #df : DataFrame as returned by get_weight, words, list as returned by split_tweets
    wordsl1l2=[]

    #l1+l2 :
    for k in range(1,len(words)):
        wordsl1l2.append(words[k-1]+' '+words[k])
    
    wordsl1l2.append(words[0]+' '+words[-1])
    df['l1+l2']=wordsl1l2

    #next :
    df['next'] = words[2:]+[words[0]]+[words[1]]

    #l1+l2+next : 
    wordsl1l2next=[]

    for k in range (2,len(words)):
        wordsl1l2next.append(words[k-2]+' '+words[k-1]+' '+words[k])
    
    wordsl1l2next.append(words[len(words)-2]+' '+words[len(words)-1]+' '+words[0])
    wordsl1l2next.append(words[len(words)-1]+' '+words[0]+' '+words[1])

    df['l1+l2+next']=wordsl1l2next

    #freq :
    freq = df["l1+l2+next"].value_counts() 

    M=[]

    df = df.drop_duplicates() #on supprime les doublons dans notre table 

    for k in df["l1+l2+next"]:
        M.append(freq[k])
        
    df["freq"]=M

    return(df)

def get_end_words(L): #L : string.split() 
    # return every words at the end of a sentence in the train set
    end_words=[]
    
    for word in L:
        
        if word!= "" and word[-1] in ['.','!','?'] and word != '.':
            end_words.append(word)
        
    return(end_words)

def get_first_words(df,end_words): #df : tweets dataframe 
                                   #end_words : list as returned by get_end_words
                                   
    first_words=[] #contains every serie word 1 + word 2 beginning a tweet in the trainig sample
    
    for tw in df["Tweet"]:

        t=tw.split()

        if len(t)>2:

            if "https" not in t[0] and "https" not in t[1]:

                first_words.append(t[0]+" "+t[1])

            for k in range (2,len(t)-1):

                if t[k]!="" and t[k-1] in end_words:

                    if "https" not in t[k] and "https" not in t[k+1]:

                        first_words.append (t[k]+" "+t[k+1])
    return(first_words)


def get_pivot(df):
#pivot_df.at['follow','l1+l2] gives the number of times the two words "l1+l2" have been followed by "next" in the training set
    pivot_df = df.pivot(index = 'next', columns= 'l1+l2', values='freq')
    pivot_df= pivot_df.fillna(0)
    sum_words = pivot_df.sum() #sum_words vector containing the sum of each column of pivot_df

    for col in pivot_df.columns:
        pivot_df[col]=pivot_df[col].apply(lambda x:x/sum_words[col])


    return(pivot_df)
    

def make_a_sentence(start,pivot_df,end_words):
    wordl1l2= start
    sentence=wordl1l2.split()
    
    while len(sentence) < 40:
        
        wordl1l2=sentence[-2]+' '+sentence[-1]
        print(len(words))
        print(len(list(pivot_df[wordl1l2])))
        next_word = choice(a = pivot_df.index, p = list(pivot_df[wordl1l2])) #random choice in the column weighted by the probabilities
       
        if next_word in end_words:
            
        
            if len(sentence) > 2:    
                
                sentence.append(next_word)
                break
            else :
                continue
        else :
            
            sentence.append(next_word)
        word=sentence[-1]+' '+next_word
    sentence = ' '.join(sentence)
    return sentence