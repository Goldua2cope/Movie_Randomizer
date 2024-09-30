import pandas as pd
import pyinputplus as pyip

df = pd.read_csv('movies.csv') #läser csv filen och skapar en df liknar med excels spreadsheet

# kolumnen genre innehåller mer än element som upprepas i vissa råd
# därför behöver vi en set 
genres: set = set() #liknar med list men använder {} och kan inte innehålla en element mer än en gång(unika)
for genre_list in df['genre']: #df['genre'] betyder i kolumnen genre
    for genre in genre_list.split(', '): #komma och mellanslag#delar upp strängen i en lista(metod)
        genres.add(genre) # add metod som tillhör till set() och lägga till element till set()
genre_list: list = sorted(list(genres)) #omvandlar set() till list() och sorterar element alphabetiskt

genre_list.append('Does not matter') #lägga till slutet av listan elementet 'Does not matter'

#kolumnen director får också ha en list som innehåller en director bara en gång
director_list: list = sorted(df['director'].unique().tolist())  #unique() samma som set() #.tolist() omvandlar unique till lista #pandas metoder
director_list.append('Does not matter') #lägga till slutet av listan elementet 'Does not matter'


#jings def som omvandlar hours to minutes
def time_in_minutes(hours: str) -> int:
    match hours:
        case '1-2 h':
            return 120
        case '2-3 h':
            return 180
        case 'Does not matter':
            return 200  
        case _:
            raise ValueError('Invalid value!')
#time_limit: int = time_in_minutes(time_choice)

#en def som funkar som Jings men för året nu som returnerar två integers t ex år 0 och år 1999       
def year_filter(year_choice: str) -> tuple[int, int]: #två integers först är det minsta och andra den största
    match year_choice:
        case 'Older than 2000':
            return (0, 1999) #year_range[0] = 0 och year_range[1] = 1999
        case 'Newer than 2000':
            return (2000, 2025) #year_range[0] = 2000 och year_range[1] = 2025
        case 'Does not matter':
            return (0, 2025)  
        case _:
            raise ValueError('Invalid value!')
#year_range = year_filter(year_choice)

# en class för movies 
class Movies:
    def __init__(self,original_title= None ,year = None, genre = None,duration = None, director = None) -> None:
        self.original_title: str= original_title
        self.year : int = year
        self.genre : str = genre
        self.duration : int = duration
        self.director : str = director

    def __str__(self) -> str :   
        return f'''Title: {self.original_title}\n
                   Year: {self.year}\n
                   Genre: {self.genre}\n
                   Duration: {self.duration} minutes.\n
                   Director: {self.director}'''
    
# en class som filtrerar movies och använder df
class Movies_Filter:
    def __init__(self,df):
        self.df = df

    def filter_duration(self, time_limit):
        return self.df[self.df['duration'] <= time_limit] #df i kolumnen duration mindre eller lika med time_limit # return True(alltså alla movies som har duration <= time_limit) #om duration är storre  False
    
    
    def filter_year(self,df,year_range):
        return df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])] #& liknar med AND # båda får vara True
    
    def filter_genre(self,df,genre_choice):
        if genre_choice != 'Does not matter':  #om genre_choice == False fortsätter programmet till nästa kriteria
            return df[df['genre'].str.contains(genre_choice, case=False, na=False)]   #.str.contains(pandas metod) för att råd i kolumnen genre innehåller flera variabler t ex Drama, Action
        return df
    
    def filter_director(self,df,director_choice):
        if director_choice != 'Does not matter': 
             return df[df['director'] == director_choice]
        return df


# en tredje klass som innehåller andra klassen och def som ska köras för att programmet executeras

class Movie_program:
    def __init__(self,df):
        self.df = df
        self.movies_filter = Movies_Filter(df)
    
    def main_program_runs(self):
        
        #jings input
        time_choice = pyip.inputMenu(choices=['1-2 h', '2-3 h', 'Does not matter'], 
                             prompt='How much time do you have?\n', numbered=True)
        time_limit = time_in_minutes(time_choice)
        
        genre_choice = pyip.inputMenu(choices=genre_list, prompt='Which genre do you prefer?\n', numbered=True)
        # nathalies input och jag har lagt till en variable som anropar def funktionen
        year_choice = pyip.inputMenu(choices=['Older than 2000', 'Newer than 2000', 'Does not matter'],
                             prompt='You wanna see an older or newer movie?\n', numbered=True)
        year_range = year_filter(year_choice)
        # my input
        director_choice = pyip.inputMenu(choices=director_list, prompt='Do you have any favorite director?\n', numbered=True)

        # funktioner - metoder från klass Movies_Filter anropas här och får som argument inputs 
        filtered_df = self.movies_filter.filter_duration(time_limit)
        filtered_df = self.movies_filter.filter_year(filtered_df, year_range)
        filtered_df = self.movies_filter.filter_genre(filtered_df, genre_choice)
        filtered_df = self.movies_filter.filter_director(filtered_df,director_choice)

        # fick hjälp från jings kod här
        # kollar om df är tömt eller inte
        # har lagt till en extra variable lucky_choice om användaren känna sig lucky får han 3 movies utan kriterier
        if not filtered_df.empty:
            num_movies = min(3, len(filtered_df))  
            selected_movies = filtered_df.sample(n=num_movies) #.sample # pandas metod som väljer random ett råd från df  # om jag vill flera random movies får skriva sample(n=2 eller flera
            for idx, movie in selected_movies.iterrows():
                print(f"Movies matching your criteria: \n")
                print(f"Title: {movie['original_title']}")
                print(f"Year: {movie['year']}")
                print(f"Genre: {movie['genre']}")
                print(f"Duration: {movie['duration']} minutes")
                print(f"Director: {movie['director']}")
        else:
            print("Cannot find a film for you today.")
            lucky_choice = pyip.inputYesNo(prompt='Feel you lucky today? (yes/no)\n')

            if lucky_choice == 'yes':
                num_movies = min(3, len(self.df))
                selected_movies = self.df.sample(n=num_movies)

                
                for index, movie in selected_movies.iterrows():
                    print(f"\nTitle: {movie['original_title']}")
                    print(f"Year: {movie['year']}")
                    print(f"Genre: {movie['genre']}")
                    print(f"Duration: {movie['duration']} minutes")
                    print(f"Director: {movie['director']}")
            else:
                print("Thank you!")


program = Movie_program(df) # en variable som anropar class Movie_program
program.main_program_runs() #jag anropar metoden för att programmet executeras
