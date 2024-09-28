import pandas as pd
import pyinputplus as pyip
import csv 

file_path : str = 'movies.csv'

# Class for users movie criteria:
class Movies_Criteria:
    def __init__(self, duration = None, genre = None, year = None, director = None) -> None:
        self.duration : int = duration
        self.genre : str = genre
        self.year_preference : int = year
        self.director : str = director

    def __str__(self) -> str:
        return f'''Current Criteria: 
                    Duration: Up to{self.duration} minutes.
                    Genre: {self.genre}.
                    Year: {self.year_preference}.
                    Director: {self.director}'''
    
    # Method for userinput and storing in class attributes 
    def setting_user_preference(self) -> None:

        self.duration = pyip.inputMenu(choices = ['1-2 h', '2-3 h', 'Does not matter'], 
                                       prompt= 'How much time do you have?\n', 
                                       numbered=True,
                                       postValidateApplyFunc = self.hours_to_minutes)
        #self.genre = 

        self.year_preference = pyip.inputMenu(choices = ['Older than 2000', 'Newer than 2000', 'Does not matter'], 
                                              prompt= 'You wanna see an older or newer movie?\n', 
                                              numbered=True)
        
        self.director = pyip.inputMenu(choices = self.get_all_directors(file_path), 
                                       prompt = 'Do you have any favorite director? \n', 
                                       numbered = True)
    
    # Static methods to convert max hours to minutes
    @staticmethod 
    def hours_to_minutes(hours : str) -> int:
        match hours:
            case '1-2 h':
                return 120
            case '2-3 h':
                return 180
            case 'Does not matter':
                return 200 #Value that will cover all durations
            case _:
                raise ValueError('ValueError!') #In case a non-str is passed
    
    # Static method to extract all directors from CSV file in orderly maner
    @staticmethod
    def get_all_directors(file_path : str) -> list:
        director_set = set()
        with open(file = file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader: 
                director_set.add(row['director']) 

        return sorted(list(director_set))

# Class for handling movie filtering and randomisation
class Movies_Finder:
    def __init__(self, file_path, Movies_Criteria) -> None:
        self.movies_df = pd.read_csv(file_path) # CSV file to Data frame via pandas
        self.instance_criteria = Movies_Criteria # 'pass by object reference' of users preferences

    def __str__(self) -> str:
        return f'We are working with a data frame based on {file_path}'
    
    # Method for filtering movies based on users movie criteria, 
    # returns new data frame
    def Movies_filter(self):
        return self.movies_df[
            (self.movies_df['genre'].str.contains(self.instance_criteria.genre, case=False, na=False)) & 
            (self.movies_df['duration'] <= self.instance_criteria.duration) &
            (self.movies_df['director'] == self.instance_criteria.director)
        ]
    
    # Method to sample out 5 or less random objects from Movies_filter(), 
    # returns new data frame
    def Movies_Randomizer(self):
        try:
            # Sample out 5 movies if there are 5 or more movies
            return self.Movies_filter().sample(n = 5, replace = False)
        except ValueError:
            # empty data frame or data frame with all matches
            return self.Movies_filter()

    # Method to present the result
    def Movies_Presentation(self) -> None:

        # Randomizes the filtered data frame
        Movies_Matches = self.Movies_Randomizer()

        # Counter for numbering the matches
        Counter = 1

        # Loops through and prints out result in pretty format if data frame is not empty
        if not Movies_Matches.empty:
            print("Movies matching your criteria: \n")
            for index, row in Movies_Matches.iterrows():
                print('%s'.center(10, '=') %(Counter))
                print(f"Title: {row['original_title']}")
                print(f"Genre: {row['genre']}")
                print(f"Duration: {row['duration']} minutes")
                print(f"Year: {row['year']}")
                print(f"Director: {row['director']}\n")
            Counter += 1 # Increases num with each iteration
        else:
            print("No movies found matching your criteria.")

# Main function for execution
def main() -> None:

    # Initializing user preferences
    User_Preferences = Movies_Criteria('user', genre = 'drama')
    Movies_Criteria.setting_user_preference(User_Preferences)

    # Filtration, randomisation and display
    Movie_List = Movies_Finder('movies.csv', User_Preferences)
    Movies_Finder.Movies_Presentation(Movie_List)

main()