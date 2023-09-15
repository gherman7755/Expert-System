from rules import CITIZEN_RULES
from collections import defaultdict
# from pprint import pprint as print


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
        self.antecedents = set()
        
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
    

    def findAntecedents(self):
        for rule in self.citizen_rules:
            self.antecedents.add(list(rule.antecedent())[0])
            
    
    
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
            if self.occurances[rule] is False or self.occurances[rule] is True:
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
    
    
    def updateOccurance(self):
        for rule, res in self.occurances.items():
            if res is True:
                for key, value in self.occurances.items():
                    if value is None and key.split()[-1] == rule.split()[-1]:
                        self.occurances[key] = False
                    
    
    def calculateEffectivness(self):
        for key, value in self.probability.items():
            last_word = key.split()[-1]
            if self.occurances[key] == False or self.occurances[key] == True:
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

        return output_strings


    def askQuestion(self, output, name):
        yeses = ["y", "ye", "yeah", "yep", "YES", "Y", "yes"]
        nos = ["n", "no", "NO", "N", "NOPE", "nope"]

        from production import populate

        if output["type"] == "s":
            print("Answer yes/no:\n")
            question = "Does " + populate(output["question"], {"x":name}) + "?"
            answer = input(f"{question}\nYour answer is: ")
            
            if answer in yeses:
                self.setOccured(output["question"])
            elif answer in nos:
                self.setNeedless(output["question"])

        else:
            print("Answer with number of variant:\n")
            question = [f"{i + 1}. Does " + populate(e, {"x":name}) + "?" for i, e in enumerate(output["variants_of_answers"])]
            
            try:
                answer = int(input("\n".join(question) + "\nYour answer is: "))
                
                for element in output["variants_of_answers"]:
                    if element != output["variants_of_answers"][answer - 1]:
                        self.setNeedless(element)
                    else:
                        self.setOccured(element)
                    self.probability.pop(element)
            except ValueError:
                for element in output["variants_of_answers"]:
                    self.setNeedless(element)
                    self.probability.pop(element)
            
            # for element in output["variants_of_answers"]:
            #     if element != output["variants_of_answers"][answer - 1]:
            #         self.setNeedless(element)
            #     else:
            #         self.setOccured(element)
        
        # print(self.probability)

    
    def start(self, name):
        from production import run_conditions, instantiate, match
        
        result = ()
        answer_is_found = False
        rules_forward = set()
        
        self.fullFill()
        self.findConsequents()
        self.findAntecedents()
        
        while True:
            self.findTypes()
            self.calculateProbability()
            self.calculateEffectivness()
            self.findBestCharacteristics()
            print(30*"-")
            self.askQuestion(self.makeQuestion(), name)
            self.updateOccurance()
            
            for fact in self.occurances:
                if self.occurances[fact] is True:
                    rules_forward.add(instantiate(fact, {"x":name}))
            result = run_conditions(CITIZEN_RULES, rules_forward)
            
            # print(result)
            
            for element in result:
                if element.replace(name, "(?x)") not in self.antecedents and element.replace(name, "(?x)") in self.consequents:
                    print("Match found: " + instantiate(element, {"x":name}) + "!!!!!")
                    answer_is_found = True
                    break
            
            if answer_is_found:
                break
            

    def doSomething(self):
        pass


if __name__ == "__main__":
    occ = Occurance(CITIZEN_RULES)
    occ.start("mark")
    # for key, value in occ.probability.items():
    #     print(key, value)
    # occ.askQuestion(occ.makeQuestion(), "mark")
    # print(occ.occurances)
    