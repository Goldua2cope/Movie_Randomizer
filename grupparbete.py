import pandas as pd
import pyinputplus as pyip
import csv 

file_path = 'movies.csv'  
movies_df = pd.read_csv(file_path)

class Movie:
    def __init__(self, title, year, genre, duration, director):
        self.title = title
        self.year = year
        self.genre = genre
        self.duration = duration
        self.director = director

def matches_criteria(self, time_limit, genre, year, director):
    #här lägger vi in hur användarens inputs matchar med filmerna med if else

    
#skapa alla inputs användaren kommer svara på

tid = pyip.inputMenu(choices = ['1-2 h', '2-3 h', 'Does not matter'], prompt= 'How much time do you have?\n', numbered=True)

regissörer_set = set() #behövde en lista som inte innehåller samma direktör två eller flera gånger (https://www.digitalocean.com/community/tutorials/python-remove-duplicates-from-list)

with open(file='movies.csv', mode='r' ) as file:
    reader = csv.DictReader(file) # csv.DictReader(exampleFile)(kapitel16) eftersom movies.csv har titel i första rådet(tex original_title osv)
    
    for row in reader: #kapitel16
        regissörer_set.add(row['director']) # vill lägga director till regissörer_set

regissör_list = sorted(list(regissörer_set)) #sorted för att listan presenteras fint till användaren 
#print(directors_list) kollar om tar emot lista med directors

director_choice = pyip.inputMenu(choices=regissör_list, prompt= 'Do you have any favorite director? \n', numbered=True)


#läs från csv filen och sortera utifrån användarens inputs
#med hjälp av loopar

#printa ut 3-5 filmer efter sorteringen

'''val = ["drama", "comedy"]
import pyinputplus  as pyip
svar = pyip.inputMenu(val, prompt=  "Whatcha want?" )'''
