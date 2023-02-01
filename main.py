from rules import CITIZEN_RULES, CITIZEN_DATA
from production import run_conditions, backward_chain


if __name__=='__main__':
    # print(run_conditions(CITIZEN_RULES, CITIZEN_DATA))
    backward_chain(CITIZEN_RULES, "nurlan is Loonie!")