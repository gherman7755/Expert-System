from rules import CITIZEN_RULES, CITIZEN_DATA
from production import run_conditions, backward_chain, setFacts


if __name__=='__main__':
    print(run_conditions(CITIZEN_RULES, CITIZEN_DATA))
    al = setFacts(CITIZEN_RULES, "nurlan is Loonie!")
    print(*(el for el in al), sep='\n')