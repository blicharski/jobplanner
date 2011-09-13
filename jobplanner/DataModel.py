

class TaskModel:
    data = {}

    def __setattr__(self, name, value):
        self.data[name] = value

    def __getattr__(self, name):
        return self.data[name]

    def __str__(self):
        string = "Date: " + self.data["date"]
        string += " Task finished: " + str(self.data["finished"])
        string += " Task name: " + self.data["name"]
        string += " Hour from: " + self.data["hour_from"] + " Hour to: " + self.data["hour_to"]
        string += " Hours count: " + self.data["hours_count"]
        
        return str(string)

class Day:
    tasks = []

    def __add_task(self, new_task):
        tasks.append(new_task)
