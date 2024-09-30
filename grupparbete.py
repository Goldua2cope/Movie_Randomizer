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

###director_set = set(df['director']) #samma som ovanpå men istället för pandas unique() använder set direct till kolumn df['director']
####director_list = sorted(list(director_set))
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

#en def som funkar som Jings men för året nu som returnerar två integers t ex år 0 och år 1999       
# ändrade parameter years_choice  till years för att inte vara samma med argument när jag anropar funktionen
def year_filter(years: str) -> tuple[int, int]: #två integers först är det minsta och andra den största
    match years:
        case 'Older than 2000':
            return (0, 1999) #year_range[0] = 0 och year_range[1] = 1999
        case 'Newer than 2000':
            return (2000, 2025) #year_range[0] = 2000 och year_range[1] = 2025
        case 'Does not matter':
            return (0, 2025)  
        case _:
            raise ValueError('Invalid value!')

# en class för movies 
class Movies:
    def __init__(self,original_title= None ,year = None, genre = None,duration = None, director = None) -> None:
        self.original_title: str= original_title
        self.year : int = year
        self.genre : str = genre
        self.duration : int = duration
        self.director : str = director

    def __str__(self) -> str :   #strukurer #hur kommer filmer att skrivas ut
        return (f"Title: {self.original_title}\n"
                f"Year: {self.year}\n"
                f"Genre: {self.genre}\n"
                f"Duration: {self.duration} minutes\n"
                f"Director: {self.director}\n")
    
# en class som filtrerar movies och använder df
class Movies_Filter:
    def __init__(self,df):  #df är df = pd.read_csv('movies.csv') alltså alla filmer från filen
        self.df = df
    
    ##första def filtrerar df som innehåller alla filmer
    def filter_duration(self, time_limit):
        return self.df[self.df['duration'] <= time_limit] #df i kolumnen duration mindre eller lika med time_limit # return True(alltså alla movies som har duration <= time_limit) #om duration är storre  False
    #  self.df = df definieras efter return  och blir en ny df med filtrerade movies
    
    # andra def filtrerar nya df som uppstår efter varje def 
    # därför skriver jag df[(df['year'] ... och inte self.df som första råden
    def filter_year(self,df,year_range):
        return df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])] #& liknar med AND # båda får vara True
    
    def filter_genre(self,df,genre_choice):
        if genre_choice != 'Does not matter':  #om genre_choice == False fortsätter programmet till nästa kriteria
            return df[df['genre'].str.contains(genre_choice, case=False, na=False)]   #.str.contains(pandas metod) för att råd i kolumnen genre innehåller flera variabler t ex Drama, Action
        return df          # returnerar df som filtrerades av föregående def

    
    def filter_director(self,df,director_choice):
        if director_choice != 'Does not matter': 
             return df[df['director'] == director_choice]
        return df


# en tredje klass som innehåller andra klassen och def som ska köras för att programmet executeras

class Movie_program:
    def __init__(self,df):
        self.df = df
        self.movies_filter = Movies_Filter(df) #jag skapar attributet inne i klasset# innehåller def metoder från Movies_Filter #filtrerar inputs och ger möjligheten att använda def från det klasset(i slutet av det här klasset)
    
    def main_program_runs(self):
        #ändrade inputs namn för att de inte ha samma namn med metoder från class Movies_Filter
        #de kan ändå ha samma namn för att de inte tillhör i samma scop men ville undika förvirring
        #jings input
        time_choice = pyip.inputMenu(choices=['1-2 h', '2-3 h', 'Does not matter'], 
                             prompt='How much time do you have?\n', numbered=True)
        time_limit_input = time_in_minutes(time_choice)
        
        genre_choice_input = pyip.inputMenu(choices=genre_list, prompt='Which genre do you prefer?\n', numbered=True)
        
        # nathalies input och jag har lagt till en variable som anropar def funktionen
        year_choice = pyip.inputMenu(choices=['Older than 2000', 'Newer than 2000', 'Does not matter'],
                             prompt='You wanna see an older or newer movie?\n', numbered=True)
        year_range_input = year_filter(year_choice)
        # my input
        director_choice_input = pyip.inputMenu(choices=director_list, prompt='Do you have any favorite director?\n', numbered=True)

        # funktioner - metoder från klass Movies_Filter anropas här och får som argument inputs 
        filtered_df = self.movies_filter.filter_duration(time_limit_input)
        filtered_df = self.movies_filter.filter_year(filtered_df, year_range_input)
        filtered_df = self.movies_filter.filter_genre(filtered_df, genre_choice_input)
        filtered_df = self.movies_filter.filter_director(filtered_df,director_choice_input)

        # fick hjälp från jings kod här
        # kollar om df är tömt eller inte
        # har lagt till en extra variable lucky_choice om användaren känna sig lucky får han 3 movies utan kriterier
        if not filtered_df.empty:
            num_movies = min(3, len(filtered_df))  
            selected_movies = filtered_df.sample(n=num_movies) #.sample # pandas metod som väljer random ett råd från df  # om jag vill flera random movies får skriva sample(n=2 eller flera
            for index, movie_row in selected_movies.iterrows():
                movie = Movies(
                    original_title=movie_row['original_title'], 
                    year=movie_row['year'], 
                    genre=movie_row['genre'], 
                    duration=movie_row['duration'], 
                    director=movie_row['director']
               )
                print(f"Movies matching your criteria:\n{movie}")
        else:
            print("Cannot find a film for you today.")
            lucky_choice = pyip.inputYesNo(prompt='Feel you lucky today? (yes/no)\n')

            if lucky_choice == 'yes':
                num_movies = min(3, len(self.df))
                selected_movies = self.df.sample(n=num_movies)

                
                for index, movie_row in selected_movies.iterrows():
                    print(f"\nTitle: {movie['original_title']}")
                    print(f"Year: {movie['year']}")
                    print(f"Genre: {movie['genre']}")
                    print(f"Duration: {movie['duration']} minutes")
                    print(f"Director: {movie['director']}")
            else:
                print("Thank you!")


program = Movie_program(df) # en variable som anropar class Movie_program
program.main_program_runs() #jag anropar metoden för att programmet executeras
