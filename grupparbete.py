#importera allt som behövs
import pyinputplus as pyip

#skapa alla inputs användaren kommer svara på
tid = pyip.inputMenu(choices = ['1-2 h', '2-3 h'], prompt= 'How much time do you have?\n', numbered=True)

def time_in_minutes(hours: str) -> int: #returnerar max timmar till minuter
    match hours:
        case '1-2 h':
            return 120
        case '2-3 h':
            return 180
        case _:
            raise ValueError('ValueError!') #
          
#läs från csv filen och sortera utifrån användarens inputs
#med hjälp av loopar

#printa ut 3-5 filmer efter sorteringen

val = ["drama", "comedy"]
import pyinputplus  as pyip
svar = pyip.inputMenu(val, prompt=  "Whatcha want?" )
