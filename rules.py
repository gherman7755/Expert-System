from production import IF, AND, THEN, OR, DELETE, NOT, FAIL


CITIZEN_RULES = (
    IF( AND("(?x) has strong accent",
            "(?x) has white skin"), 
       THEN("(?x) is from Europe") ),
    IF( AND("(?x) has black hair",
            "(?x) has no accent"), 
       THEN("(?x) is from America") ),
    IF( AND("(?x) has brown eyes",
            "(?x) has yellow skin"), 
       THEN("(?x) is from Asia") ),
    IF( AND("(?x) has blonde hair",
            "(?x) is from Europe"), 
       THEN("(?x) is rich") ),
    IF( AND("(?x) is rich",
            "(?x) has square face"), 
       THEN("(?x) is Norwagian") ),
    IF( AND("(?x) is rich",
            "(?x) has circle face"), 
       THEN("(?x) is Loonie!") ),
    IF( AND("(?x) is from Europe",
            "(?x) has black hair"), 
       THEN("(?x) is Moldavian") ),
    IF( AND("(?x) is from America",
            "(?x) has white skin"), 
       THEN("(?x) is US citizen") ),
    IF( AND("(?x) is from America",
            "(?x) has yellow skin"), 
       THEN("(?x) is Mexican") ),
    IF( AND("(?x) is from Asia", 
            "(?x) has circle face"), 
       THEN("(?x) is Kazakhstan citizen") ),
    IF( AND("(?x) is from Asia",
            "(?x) has square face"), 
       THEN("(?x) is Chinee") ),
)

CITIZEN_DATA = (
    "mark has white skin",
    "mark has strong accent",
    "mark has black hair",
    "mark has square face",
    "amma has no accent",
    "amma has black hair",
    "amma has white skin",
    "jimmy has white skin",
    "jimmy has strong accent",
    "jimmy has blonde hair",
    "jimmy has circle face",
    "claus has black hair",
    "claus has no accent",
    "claus has yellow skin",
    "nurlan has brown eyes",
    "nurlan has yellow skin",
    "nurlan has circle face",
    "jackie has brown eyes",
    "jackie has yellow skin",
    "jackie has square face",
)