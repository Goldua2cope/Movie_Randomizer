import pandas as pd
import pyinputplus as pyip
import csv 

file_path = 'movies.csv'  
movies_df = pd.read_csv(file_path)
    
### All input statements (and relevent functions)

#Input time
time_choice = pyip.inputMenu(choices = ['1-2 h', '2-3 h', 'Does not matter'], prompt= 'How much time do you have?\n', numbered=True)

#Converting max hours to minutes
def time_in_minutes(hours: str) -> int:
    match hours:
        case '1-2 h':
            return 120
        case '2-3 h':
            return 180
        case 'Does not matter':
            return 200
        case _:
            raise ValueError('ValueError!')

#Input years preference
year_choice =pyip.inputMenu(choices = ['Older than 2000', 'Newer than 2000', 'Does not matter'], prompt= 'You wanna see an older or newer movie?\n', numbered=True)

#Input director preference
director_set = set() #behövde en lista som inte innehåller samma direktör två eller flera gånger (https://www.digitalocean.com/community/tutorials/python-remove-duplicates-from-list)

with open(file='movies.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file) # csv.DictReader(exampleFile)(kapitel16) eftersom movies.csv har titel i första rådet(tex original_title osv)
    
    for row in reader: #kapitel16
        director_set.add(row['director']) # vill lägga director till regissörer_set

director_list = sorted(list(director_set)) #sorted för att listan presenteras fint till användaren 

director_choice = pyip.inputMenu(choices=director_list, prompt= 'Do you have any favorite director? \n', numbered=True)

### Data extraction from csv file according to user inputs 
desired_genre = 'Drama' #
desired_duration = time_in_minutes(time_choice)

# Data frame that contains matched objects
filtered_movies = movies_df[
    (movies_df['genre'].str.contains(desired_genre, case=False, na=False)) & 
    (movies_df['duration'] <= desired_duration) 
]

# prints the first 5 movies (This needs to be randomized!)
if not filtered_movies.empty:
    print("Movies matching your criteria:\n")
    for index, row in filtered_movies.iterrows():
        print(f"Title: {row['original_title']}")
        print(f"Genre: {row['genre']}")
        print(f"Duration: {row['duration']} minutes")
        print(f"Year: {row['year']}")
        print(f"Director: {row['director']}\n")
else:
    print("No movies found matching your criteria.")
