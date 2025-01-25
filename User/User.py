
class User:
    def __init__(self, name, age, sleep_efficeincy,smoking_status,exercise, coffein_consumption,waking_up_during_night,sex):
        self.name = name
        self.age = age
        self.sleep_efficeincy=sleep_efficeincy
        self.smoking_status = smoking_status
        self.exercise = exercise
        self.coffein_consumption = coffein_consumption
        self.waking_up_during_night = waking_up_during_night
        self.sex=sex

    # def sleep_efficiency_calculator(self):
    #     return self.total_sleep/self.total_minutes_in_bed*100
