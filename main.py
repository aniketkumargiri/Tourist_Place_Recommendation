# pip install python-Levenshtein
# pip install pandas
# pip install fuzzywuzzy
# pip install collections
# pip install nltk

import pandas as pd
from fuzzywuzzy import process
from collections import Counter
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

df = pd.read_csv("cleansed_data.csv")

with open("cities.txt","r") as f:
    cities = f.read().split("\n")

def getmatches(query,choices,limit=5):
    results= (process.extract(query,choices,limit=limit))
    # print(results)
    cities = []
    # print(results[0][1])
    while results[0][1]!=100:
        print("City not found!")
        print("Closest matches are:")
        for i in results:
                cities.append(i[0])
        print(cities)
        return "Please choose correct name!"
    else:
        return results[0][0]

        
    # print(result[0])
    # print(type(result[0]))
    # city = ""
    # val = ""
    # flag1 = False
    # flag2 = False
    # count = 2
    # for i in result:
    #     if flag2 and i==')':
    #         break
    #     elif flag2 and count :
    #         count-=1 
    #     elif flag2 and not count:
    #         val=val+i
    #     elif i == '\'' and not flag1:
    #         flag1 = True
    #     elif i == '\'' and flag1:
    #         flag2 = True
    #     elif flag1 :
    #         city = city+i
    
    # return [city,val]


inputCity = input("Enter City: \n")
city = (getmatches(inputCity,cities))
while city == "Please choose correct name!":
    inputCity = input("Enter City Again: \n")
    city = (getmatches(inputCity,cities))

print("Entered city: ",city)

tempPlaces = set()
for i in range(0,len(df)-1):
    if df.at[i,'City'] == city:
        tempPlaces.add(df.at[i,'Place'])
places = []
reviews = []
values = []
for i in tempPlaces:
    places.append(i)
    reviews.append([])
    values.append(0)

print("All visting places of given city: ")
# for i in range(0,len(places)-1):
#     print("(",i+1,")\t",places[i])
print(places)
# print(reviews)


for i in range(0,len(df)-1):
    if df.at[i,'City'] == city:
        for j in range(0,len(places)-1):
            if df.at[i,'Place'] == places[j]:
                review = df.at[i,'Review']
                word = ""
                for char in review:
                    if char == " " or char == '.' or char == ',':
                        reviews[j].append(word)
                        word = ""
                    else:
                        word=word+char
                
                # reviews[j] = reviews[j] + ' ' + df.at[i,'Review']
            # reviews.append(df.at[i,'Review'])


word_cnt = []
for list in reviews:
    list_freq= (Counter(list))
    word_cnt.append(list_freq)
    # print(list_freq)
# Finding count of each element


#Printing result of counter
# print(list_freq)

# Printing it using loop
# for key, value in list_freq.items():
#    print(key, " has count ", value)

interests = input("Please enter tags for personalized results: \n")
keywords = []
# print(interests)
# values = []
tokens = word_tokenize(interests)
lemmatizer = WordNetLemmatizer()
for word in tokens:
    lemmas = lemmatizer.lemmatize(word)
    keywords.append(lemmas)
    # print(lemmas)

    # print(type(tokens))
print(keywords)
hasAll = []
for i in range(0,len(places)-1) :
    values[i]= 0
    hasAll.append(True)
# print(hasAll)
# keywords = []
# interest = ""
# for i in interests :
#     # print(i)
#     if i == ',' :
#         keywords.append(interest)
#         interest=""
#     elif i != ',' and i != ' ' :
#         interest = interest + i
# if interest!="":
#     keywords.append(interest)
# print(keywords)
# vals = []
for i in keywords :
    synoset = set()
    # synonyms =  []
    for i in keywords :
        for syn in wordnet.synsets(i) :
            for l in syn.lemmas() :
                synoset.add(l.name())
        # print(synoset)
        for i in range(0,len(word_cnt)-1) :
            count=0
            for keyword in synoset:
                for key, value in word_cnt[i].items() :
                    if hasAll[i] == True and keyword == key :
                        # values[i]+=value
                        count+=value
            if count<=3:
                hasAll[i]=False
                values[i]=0
            else:
                values[i]+=count
            # else:
            #     values[i]+=count
            #     print(count)
                # count+=value

            # print(key, " has count ", value)
        # values[i]+=count
# print(hasAll)
print(values)

values, places = zip(*sorted(zip(values, places)))

print(values)
print(places)


print("Top recommended tourist sites: ")
for i in range(len(places)-1,0,-1):
    if values[i]==0:
        break
    else:
        print("(",len(places)-i,")", places[i])

