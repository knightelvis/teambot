import datetime as dt
import random
import functions.models as models

class Task:
    '''
    The task object; this is a representation on top of the 
    db task object (models.Task).
    '''

    def __init__(self, from_user, from_user_id, owner, content, priority=3):
        self.from_user = from_user
        self.owner = owner
        self.content = content
        self.time = dt.datetime.now()
        self.priority = int(priority)
        
        # this is needed to send callback to the from_user
        self.from_user_id = from_user_id

        self.db_task =  models.Task.create(from_user = from_user, 
                           from_user_id = from_user_id,
                           owner_first_name = owner,
                           content = content,
                           create_time = dt.datetime.now(),
                           priority = int(priority),
                           status = 0) # 0 -> todo
        self.uid = self.db_task.id

    def days_to_today(self):
        return abs(dt.datetime.now() - self.db_task.create_time).days

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
    '''
    A Todo list class; this class provides functions to compose the tasks
    into a list.
    '''

    def __init__(self, owner):
        self.owner = owner
        self.tasks = []

    def add_task(self, task):
        '''add a task to this todo list.
            the task should be a string'''
        
        # add to Task table
        models.database.connect()
        models.Task.create(from_user = task.from_user, 
                           from_user_id = task.from_user_id,
                           owner_first_name = task.owner,
                           content = task.content,
                           create_time = task.time,
                           priority = task.priority,
                           status = 0)

        models.database.close()

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

        self.remove_tasks_in_db(removed)

        return removed



    def remove_tasks_in_db(self, tasks):
        '''
        Remove the tasks.
        The input are the todo.Task
        '''        
        models.database.connect()

        for task_id in task_ids:
            temp_task = models.Task.select().where(Task.id == task_id)
            temp_task.status = 2; # deleted
            temp_task.save()
            deleted.append(temp_task)
        
        models.database.close()

        return 

    def task_List(self):
        '''return a list of tasks added to this todo list'''
        return self.tasks

    def list_tasks(self, owner):
        try: 
            models.database.connect()
            models.Task.select()
        except:
            print("Unexpected error:", sys.exc_info()[0])

        finally:
            models.database.close()


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
