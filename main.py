from rules import CITIZEN_RULES, CITIZEN_DATA
from production import run_conditions, backward_chain, setFacts


if __name__=='__main__':
    
    from propsCalculator import Occurance
    
    print("\nWelcome to Detecting Tourist System!")

    while True:
        print(60*"*")
        print("\nWhat I can help you with? Choose by variant of answer:")
        answer = int(input("1. Match tourist by description\n2. Give info about some type of tourist\n\nYour answer is: "))
        print(60*"-")
        
        
        if answer == 1:
            akinator = Occurance(CITIZEN_RULES)
            tourist_name = input("Enter the name of the tourist: ")
            akinator.start(tourist_name)
        
        elif answer == 2:
            tourist_type = input("Enter what type of tourist you want to achieve (ex: mark is Moldavian): ")
            print("\nFacts what should toursist has: \n")
            enciclopedia = setFacts(CITIZEN_RULES, tourist_type)
            print(*(element for element in enciclopedia), sep="\n")
        
        else:
            break
    
    
    