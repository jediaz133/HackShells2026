from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langchain.agents import create_agent
import json
import datetime, os


# @tool
def setup(weight, age, height, sex, workoutsPerWeek, workoutTime, extra):
    """
    Desc: First time setup for the user, used for defining key attributes like 
            weight, height, age, sex, number of workouts a week, workout time. 
    
    Parameters: None

    Returns: None (Writes a description file of the user)
    """
    
    userData = {
    "weight": weight,
    "age": age,
    "height": height,
    "sex": sex, # 1 for male 0 for female
    "workoutsPerWeek": workoutsPerWeek,
    "workoutTime": workoutTime,
    "extra": extra,
    }

    jsonData =json.dumps(userData)
    jsonFile = open("static/userdata.json", "w+").write(jsonData)


@tool
def userEdit(detailToEdit: str, newValue: str) -> bool:
    """ 
    Desc: Change user details

    Parameters: 
    * detailToEdit (str): the key detail to edit
    * newValue (str): the new value to set to it

    Example: 
    * userEdit("weight","185")

    Returns (bool): False For success True for error.
    """
    
    jsonFile = open("static/userdata.json", "r+")
    jsonThing = jsonFile.read()
    jsonLoaded = json.loads(jsonThing)
    jsonLoaded[detailToEdit] = newValue
    jsonFile.close()
    jsonData =json.dumps(jsonLoaded)
    jsonFile = open("static/userdata.json", "w+").write(jsonData)
    print(jsonThing)
    return 0

def userRead() -> str:
    """Returns useful information about the user's health details"""
    jsonFile = open("static/userdata.json", "r+")
    jsonThing = jsonFile.read()
    jsonFile.close()
    return "\n"+str(jsonThing)+"\n"



@tool
def getTime() -> str:
    """
    Desc: Get the current date and time
    Returns: The current time
    """
    return "\n"+str(datetime.datetime.now())+"\n"

# @tool
def logDay(date :str, burned: str, consumed: str, workoutTime: str, weight: str, daysActivity: str) -> bool:
    """
    Desc: Log calories burned, consumed on a day
    
    Parameters:
        date (str): the current date. Example "18sep2026" is September 18 2026
        burned (str): the amount of calories burned
        consumed (str): the amount of calories consumed
        workoutTime (str): the time someone worked out
        weight (str): the weight of a person
        daysActivity (str): what the person did as a description
    """
    dayData = {
    "consumed": consumed,
    "burned": burned,
    "workoutTime": workoutTime,
    "weight": weight,
    "daysActivity": daysActivity
    }

    jsonData =json.dumps(dayData)
    jsonFile = open("static/dates/"+date+".json", "w+").write(jsonData)
    return 0


def checkDates(date: str) -> str:
    """
    Desc: Returns if a day has a log
       
       Parameters:
           date (str): the current date. Example "18sep2026" is September 18 2026
    """
    return os.path.isfile("/home/puffle/Documents/schoolll/Hackathons/HackShells 2026/static/dates/"+date+".json")

def getDayData(date: str) -> str:
    """
    Desc: Returns calories burned, consumed, and workout time of a day
       
       Parameters:
           date (str): the current date. Example "18sep2026" is September 18 2026
    """
    try:
        jsonFile = open("static/dates/"+date+".json", "r+")
        jsonThing = jsonFile.read()
        jsonFile.close()
        return "\n"+str(jsonThing)+"\n"
    except Exception as e:
        return "Error, maybe doesnt exist"



def editDay(date: str, typeOfValue: str, newValue: str) -> bool:
    """
    Desc: edit calories (burned or consumed) to a day, !!!can only edit one at a time!!!

    Parameters:
        typeOfValue (str): "workoutTime" to edit workout time, "burned" to edit burned or "consumed" to edit consumed, "weight" to edit weight of the day, "daysActivity" to edit what happened in a day
        newValue (str): what you're changing the value to, !!replaces value does not add or subtract values!!
        date (str): the current date. Example "18sep2026" is September 18 2026
    
    Example: burned 100 calories on September 18 2026
        addToDay("18sep2026", 1, 100)
    """
    jsonFile = open("static/dates/"+date+".json", "r+")
    jsonThing = jsonFile.read()
    jsonLoaded = json.loads(jsonThing)
    jsonLoaded[typeOfValue] = newValue
    jsonFile.close()
    jsonData =json.dumps(jsonLoaded)
    jsonFile = open("static/dates/"+date+".json", "w+").write(jsonData)
    print(jsonThing)
    return 0