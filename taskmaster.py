import threading

class Agent(threading.Thread):
    def __init__(self, schedule):
        super().__init__()

        self.schedule = tuple(task(self) for task in schedule)
        self.status = "Idle"

    # Start an agent with the start() method
    def run(self):
        for task in self.schedule:
            self.status = task.RUNNING
            result = task.execute()
            if not result:
                self.status = task.FAILED  
                break


class Task:
    def __init__(self, running_msg, failed_msg, function, agent):
        self.RUNNING = running_msg
        self.FAILED = failed_msg

        self.status = "Idle"

        self.function = function
        self.agent = agent

    def execute(self):
        self.status = self.RUNNING
        result = self.function(self.agent)
        self.status = "Completed" if result else self.FAILED
        return result

'''
Construct a new type of Task by decorating a function:

@build_task(running="Custom status", failed="Custom status")
def task_name(agent):
    # Do something with the agent's resources.

Use the new task with many different agents:
task1 = task_name(Agent1)
task2 = task_name(Agent2)
'''
def build_task(running="Running", failed="Failed"):
    def decorator(function):
        def wrapper(agent):
            task = Task(running, failed, function, agent)
            return task
        return wrapper
    return decorator