#Experimental Playground for Algo 

    Main aim
        create a fronted which displays questions and takes input answer
        create a backend (or pseudo backend) which implements the algo

    Current implementation
        Jinja and flask
    
    To run
        python main.py

# TODO
> Repeated questions should not come (adding ques_id to questions)
> Algo
> Filter

# Algo
> How to distinguish between varieties of questions student should know of same Level and Type
> starting question of the quiz should be based on student's previous performance
> randomize the question list while sending the question

- Review below conditions which are implemented

## termination condition: 
- maximum number of questions reached
- 2 or 3 questions of highest level done successfully (tentative)

## Conditions:
- if max no of tries at a particular energy level reached, throw at the next type's easiest level
- if questions not available and max tries not reached, continue with flow. (reflect towards ceiling for the floor)

type|Level|Img|Question|A|B|C|D|Answer|sub-topics|Prerequisite|image_path