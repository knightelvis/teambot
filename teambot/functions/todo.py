import datetime as dt
import random

class Task:
    '''The task object'''

    def __init__(self, from_user, from_user_id, owner, content, priority=3):
        self.from_user = from_user
        self.owner = owner
        self.content = content
        self.time = dt.datetime.now()
        self.priority = int(priority)
        self.from_user_id = from_user_id  # this is needed to send callback to the from_user

    def days_to_today(self):
        return abs(dt.datetime.now() - self.time).days

    def to_string(self):
        days = self.days_to_today()
        out = ""
        if days > 1:
            out += "-" + str(days) + " days"
        elif days == 1:
            out += "-" + str(days) + " day"
        elif days == 0:
            out += "today"
        return out + " | from " + self.from_user + " | " + self.content


class TodoList:
    '''A Todo list class'''

    def __init__(self, owner):
        self.owner = owner
        self.tasks = []

    def add_task(self, task):
        '''add a task to this todo list.
            the task should be a string'''

        # insert based on priority
        # the smaller the higher priority
        if self.tasks:
            for i in range(0, len(self.tasks)):
                if self.tasks[i].priority > task.priority:
                    self.tasks.insert(i, task)
                    return
                elif i == len(self.tasks) - 1:
                    self.tasks.append(task)
                    return
        else:
            self.tasks.append(task)
            return
        # heappush(self.tasks, (priority, task))

    def remove_tasks(self, indices):
        '''remove and return the removed tasks in a list'''
        # sort indicies from highest to lowerest
        indices = list(set(indices))
        indices.sort(reverse=True)

        removed = []
        for index in map(int, indices):
            if index >= 1 and index <= len(self.tasks):
                removed.append(self.tasks.pop(index - 1))
        return removed

    def task_List(self):
        '''return a list of tasks added to this todo list'''
        return self.tasks

    def list_tasks_with_priority(self):
        out = "*" + self.owner + "\'s list:" + "*"
        num = 1
        if self.tasks:
            for task in self.tasks:
                out = out + "\n" + "*" + str(num) + "*" + " - " + "_" + \
                    task.to_string().strip() + "_" + ";\n"
                num += 1
        else:
            # remove th e last :
            out = out[:-1] + " is empty! :thumbsup:"

        return out
