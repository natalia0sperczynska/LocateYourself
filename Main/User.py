
class User:
    def __init__(self, name, age, total_sleep, total_minutes_in_bed,smoking_status,exercise, coffein_consumption,waking_up_during_night):
        self.name = name
        self.age = age
        self.total_sleep = total_sleep
        self.total_minutes_in_bed = total_minutes_in_bed
        self.smoking_status = smoking_status
        self.exercise = exercise
        self.coffein_consumption = coffein_consumption
        self.waking_up_during_night = waking_up_during_night
        #dużo tego tu będzie ale no trudno

    def sleep_efficiency_calculator(self):
        return self.total_sleep/self.total_minutes_in_bed*100

    def exercise_frequency_calculator(self):
        return self.total_minutes_in_bed/self.exercise