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
        self.probability = dict()
        for rule in self.all_rules:
            if self.occurances[rule] is False:
                self.probability[rule] = 0
                continue
            rule_probability_counter = sum(
                1 for citizen_rule in self.citizen_rules 
                if rule in citizen_rule.antecedent())
            
            self.probability[rule] = self.findPercent(rule_probability_counter)

            
    def findPercent(self, occurancy_times):
        return round(occurancy_times / self.total_length, 3)


    def findTypes(self):
        for rule in self.all_rules:
            if self.occurances[rule] == False:
                continue
            characteristic_type = rule.split()[-1]
            self.type_counts[characteristic_type] += 1
            
        for key, value in self.type_counts.items():
            self.type_counts[key] = round(value / len(self.all_rules) / 10, 3)
    
    
    def calculateEffectivness(self):
        for key, value in self.probability.items():
            last_word = key.split()[-1]
            if self.occurances[key] == False:
                continue
            self.probability[key] = round(value + self.type_counts.get(last_word, 0), 3)

    
    def findBestCharacteristics(self):
        self.questions_to_ask = []
        max_value = max(self.probability.values())
        max_rules = [k for k, v in self.probability.items() if v == max_value and self.occurances[k] is not True]
    
        max_key = max((k.split()[-1], k) for k in max_rules)[1].split()[-1]
    
        self.questions_to_ask = [rule for rule in max_rules if max_key in rule]
        

    def makeQuestion(self):
        # questions = [questions[0]]
        output_strings = {
            "title":"",
            "question": "", 
            "variants_of_answers": "",
            "type":"",
        }
        
        if len(self.questions_to_ask) == 1:
            output_strings["title"] = "Answer yes or no:"
            output_strings["question"] = self.questions_to_ask[0]
            output_strings["type"] = "s"

        else:
            output_strings["title"] = "Choose one: "
            output_strings["variants_of_answers"] = []
            output_strings["type"] = "m"
            for question in self.questions_to_ask:
                output_strings["variants_of_answers"].append(question)
            output_strings["variants_of_answers"].append("I don't know")

        return output_strings


    def askQuestion(self, output, name):
        yeses = ["y", "ye", "yeah", "yep", "YES", "Y", "yes"]
        nos = ["n", "no", "NO", "N", "NOPE", "nope"]

        from production import populate

        print(output.get("title"))

        if output["type"] == "s":
            question = "Does " + populate(output["question"], {"x":name}) + "?"
            answer = input(f"{question}\n")
            
            if answer in yeses:
                self.setOccured(output["question"])
            elif answer in nos:
                self.setNeedless(output["question"])

        else:
            question = [f"{i + 1}. Does " + populate(e, {"x":name}) + "?" for i, e in enumerate(output["variants_of_answers"])]
            answer = int(input("\n".join(question)))
            
            if answer == len(output['variants_of_answers']):
                for element in output["variants_of_answers"]:
                    self.setNeedless(element)
            
            for element in output["variants_of_answers"]:
                if element != output["variants_of_answers"][answer - 1]:
                    self.setNeedless(element)
                else:
                    self.setOccured(element)
        
        # print(self.probability)


    def doSomething(self):
        pass


if __name__ == "__main__":
    occ = Occurance(CITIZEN_RULES)
    # for key, value in occ.probability.items():
    #     print(key, value)
    while True:
        # occ.askQuestion(occ.makeQuestion(), "mark")
        occ.findTypes()
        occ.calculateProbability()
        occ.calculateEffectivness()
        occ.findBestCharacteristics()
        occ.askQuestion(occ.makeQuestion(), "mark")
        print(occ.occurances)
    