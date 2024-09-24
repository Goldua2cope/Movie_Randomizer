#importera allt som behövs
import pyinputplus as pyip

#skapa alla inputs användaren kommer svara på
tid = pyip.inputMenu(choices = ['1-2 h', '2-3 h'], prompt= 'How much time do you have?\n', numbered=True)

#läs från csv filen och sortera utifrån användarens inputs
#med hjälp av loopar

#printa ut 3-5 filmer efter sorteringen

val = ["drama", "comedy"]
import pyinputplus  as pyip
svar = pyip.inputMenu(val, prompt=  "Whatcha want?" )
