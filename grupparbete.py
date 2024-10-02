import pandas as pd
import pyinputplus as pyip
import sys
import time

# Data frame stored in variable 'df'
df = pd.read_csv('movies.csv') 

# Class for movies
class Movies:
    def __init__(self, original_title = None ,year = None, genre = None, duration = None, director = None) -> None:
        # Initiate attributes for a movie object 
        self.original_title : str = original_title 
        self.year : int = year
        self.genre : str = genre
        self.duration : int = duration
        self.director : str = director

    def __str__(self) -> str : 
        return (f"Title: {self.original_title}\n"
                f"Year: {self.year}\n"
                f"Genre: {self.genre}\n"
                f"Duration: {self.duration} minutes\n"
                f"Director: {self.director}\n")

# Class that filters movies from 'df'
class Movies_Filter:
    # Initiate data frame
    def __init__(self, df : pd.DataFrame): 
        self.df = df
    
    # methods for filtering data frame according to user input, return new data frames
    def filter_duration(self, time_limit : int) -> pd.DataFrame:
        return self.df[self.df['duration'] <= time_limit] 
    
    def filter_year(self, df : pd.DataFrame, year_range : tuple) -> pd.DataFrame:
        return df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])] 
    
    def filter_genre(self, df : pd.DataFrame, genre_choice : str) -> pd.DataFrame:
        if genre_choice != 'Does not matter': 
            return df[df['genre'].str.contains(genre_choice, case=False, na=False)]  
        return df 
    
    def filter_director(self, df : pd.DataFrame, director_choice : str) -> pd.DataFrame:
        if director_choice != 'Does not matter': 
             return df[df['director'] == director_choice]
        return df

# Class for filtering, randomize and display movies from data frame
class Movie_program:
    # Initiate data frame and Movies_Filter object as attribute
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.movies_filter = Movies_Filter(df) 
    
    # Method to convert max hours to minutes
    @staticmethod
    def time_in_minutes(hours: str) -> int:
        match hours:
            case '1-2 h':
                return 120
            case '2-3 h':
                return 180
            case 'Does not matter':
                return 200  
            case _:
                raise ValueError('Invalid value!') # Handles Value error if for some reason not a str is passed
        
    # Method to convert year preference to tuple
    @staticmethod
    def year_filter(years: str) -> tuple[int, int]: 
        match years:
            case 'Before 2000':
                return (0, 1999) 
            case 'After 2000':
                return (2000, 2025) 
            case 'Does not matter':
                return (0, 2025)  
            case _:
                raise ValueError('Invalid value!') # Handles Value error if for some reason not a str is passed
            
    # Method to create a list of all genres
    @staticmethod
    def make_genre_list() -> list:
        genres: set = set() 
        for genre_list in df['genre']: 
            for genre in genre_list.split(', '): 
                genres.add(genre) 
        genre_list = sorted(list(genres)) 
        genre_list.append('Does not matter')
        return genre_list
    
    # Method to create a list with all directors
    @staticmethod
    def make_director_list() -> list:
        director_list: list = sorted(df['director'].unique().tolist())
        director_list.append('Does not matter') 
        return director_list

    # Method containing the main program logic 
    def main_program_runs(self) -> None:
        # Prompting for User preference
        # pyip.inputXX handels ValueErrors and prompts user until a valid input is given
        time_choice = pyip.inputMenu(choices = ['1-2 h', '2-3 h', 'Does not matter'], 
                             prompt = 'How much time do you have?\n',
                             numbered = True,
                             postValidateApplyFunc = self.time_in_minutes)
        
        genre_choice_input = pyip.inputMenu(choices = self.make_genre_list(), prompt = 'Which genre do you prefer?\n', numbered = True)
        
        year_choice = pyip.inputMenu(choices = ['Before 2000', 'After 2000', 'Does not matter'],
                             prompt = 'You wanna see an older or newer movie?\n', 
                             numbered = True,
                             postValidateApplyFunc = self.year_filter)
    
        director_choice = pyip.inputMenu(choices = self.make_director_list(), prompt = 'Do you have any favorite director?\n', numbered = True)

        # Filtering data frame based on user preference
        filtered_df : pd.DataFrame = self.movies_filter.filter_duration(time_choice)
        filtered_df : pd.DataFrame = self.movies_filter.filter_year(filtered_df, year_choice)
        filtered_df : pd.DataFrame = self.movies_filter.filter_genre(filtered_df, genre_choice_input)
        filtered_df : pd.DataFrame = self.movies_filter.filter_director(filtered_df,director_choice)

        # Display 3 random movies based on the filtered data frame
        if not filtered_df.empty:
            num_movies = min(3, len(filtered_df))  
            selected_movies = filtered_df.sample(n = num_movies) 
            for index, movie_row in selected_movies.iterrows():
                movie = Movies(
                    original_title = movie_row['original_title'], 
                    year = movie_row['year'], 
                    genre = movie_row['genre'], 
                    duration = movie_row['duration'], 
                    director = movie_row['director']
               )
                print(f"Movies matching your criteria:\n{movie}")
        else:
            print("Cannot find a film for you today.")
            
            # Extra option in case no matches are found, prints 3 random movies of all movies
            # pyip.inputYesNo handles ValueErrors and prompts user until a valid input is given
            lucky_choice = pyip.inputYesNo(prompt = 'Would you like to watch a random Movie of our choice? (yes/no)\n')

            if lucky_choice == 'yes':
                num_movies = min(3, len(self.df))
                selected_movies = self.df.sample(n = num_movies)

                for index, movie_row in selected_movies.iterrows():
                    print(f"\nTitle: {movie_row['original_title']}")
                    print(f"Year: {movie_row['year']}")
                    print(f"Genre: {movie_row['genre']}")
                    print(f"Duration: {movie_row['duration']} minutes")
                    print(f"Director: {movie_row['director']}")
            else:
                print("Thank you!")

# Prints a nice introduction to the program
def print_slow(text : str) -> None:
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)

print_slow("Hello! Welcome to my movie randomizer.\n")
print_slow("You probably having trouble choosing a movie today..\n")
print_slow("Don't worry I'll help you!\n ")
print_slow("")

# Main function
def main():
    program = Movie_program(df)
    program.main_program_runs() 

if __name__ == '__main__':
    main()
