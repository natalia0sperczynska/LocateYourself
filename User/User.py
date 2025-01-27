
class User:
    """
       Represents a user and their personal health and lifestyle data.

       Attributes:
           name (str): The name of the user.
           age (int): The age of the user in years.
           sleep_efficiency (float): The user's sleep efficiency as a percentage (e.g., 85.5 for 85.5%).
           smoking_status (bool): Whether the user is a smoker (True for smoker, False for non-smoker).
           exercise (int): The frequency of exercise per week (e.g., 0 for no exercise, 3 for three times a week).
           coffein_consumption (float): The user's daily caffeine consumption in milligrams.
           waking_up_during_night (int): The number of times the user wakes up during the night.
           sex (str): The user's gender ('Male' or 'Female').

       Methods:
           None
       """
    def __init__(self, name, age, sleep_efficiency, smoking_status, sex, exercise=0, coffein_consumption=0, waking_up_during_night=0):
        """
               Initializes a User object with health and lifestyle data.

               Args:
                   name (str): The name of the user.
                   age (int): The age of the user in years.
                   sleep_efficiency (float): The user's sleep efficiency as a percentage.
                   smoking_status (bool): True if the user is a smoker, False otherwise.
                   exercise (int): The number of times the user exercises per week,default=0.
                   coffein_consumption (float): The daily caffeine consumption in milligrams,default=0.
                   waking_up_during_night (int): The number of times the user wakes up during the night,default=0.
                   sex (str): The user's gender ('Male' or 'Female').
               """
        self.name = name
        self.age = age
        self.sleep_efficiency=sleep_efficiency
        self.smoking_status = smoking_status
        self.exercise = exercise
        self.coffein_consumption = coffein_consumption
        self.waking_up_during_night = waking_up_during_night
        self.sex=sex
