from rules import CITIZEN_RULES
from collections import defaultdict
from pprint import pprint as print


class Occurance:
    def __init__(self, citizen_rules):
        self.citizen_rules = citizen_rules
        self.occurances = dict()
        self.all_rules = set()
        self.probability = dict()
        self.total_length = sum(len(list(rule.antecedent())) for rule in self.citizen_rules)
        self.consequents = set()
        self.type_counts = defaultdict(int)
        self.questions_to_ask = []
        
        self.fullFill()
        self.findConsequents()
        self.findTypes()
        self.calculateProbability()
        self.calculateEffectivness()
        self.findBestCharacteristics()


    def findConsequents(self):
        for rule in self.citizen_rules:
            self.consequents.add(list(rule.consequent())[0])
        self.all_rules -= self.consequents
    
    
    def clear(self):
        self.occurances = {rule: None for rule, _ in self.occurances.items()}


    def fullFill(self):
        for rule in self.citizen_rules:
            self.all_rules |= set(list(rule.antecedent()))
        
        self.occurances = {rule: None for rule in self.all_rules}
    
    
    def setOccured(self, element):
        self.occurances[element] = True


    def setNeedless(self, element):
        self.occurances[element] = False

    
    def calculateProbability(self):
        for rule in self.all_rules:
            
            rule_probability_counter = sum(
                1 for citizen_rule in self.citizen_rules 
                if rule in citizen_rule.antecedent())
            
            self.probability[rule] = self.findPercent(rule_probability_counter)
            
        
    def findPercent(self, occurancy_times):
        return round(occurancy_times / self.total_length, 3)


    def findTypes(self):
        for rule in self.all_rules:
           characteristic_type = rule.split()[-1]
           self.type_counts[characteristic_type] += 1
            
        for key, value in self.type_counts.items():
            self.type_counts[key] = round(value / len(self.all_rules) / 10, 3)
    
    
    def calculateEffectivness(self):
        for key, value in self.probability.items():
            last_word = key.split()[-1]
            self.probability[key] = round(value + self.type_counts.get(last_word, 0), 3)

                    
    
    def findBestCharacteristics(self):
        self.questions_to_ask = []
        max_value = max(self.probability.values())
        max_rules = [k for k, v in self.probability.items() if v == max_value]
    
        max_key = max((k.split()[-1], k) for k in max_rules)[1].split()[-1]
    
        self.questions_to_ask = [rule for rule in max_rules if max_key in rule]
        
        print(self.questions_to_ask)                
        

if __name__ == "__main__":
    occ = Occurance(CITIZEN_RULES)
    # for key, value in occ.probability.items():
    #     print(key, value)
        