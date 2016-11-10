import datetime as dt
import random
import functions.models as models


def is_valid_task_index(task_num, indices):
    return all((index >= 1) and 
            (index <= task_num) 
            for index in indices)

def creat_task(from_user, from_user_id, 
                owner, content, priority=3):
    '''
    Create a task with given params.
    '''
    models.database.connect()
    db_task =  models.Task.create(from_user = from_user,
                from_user_id = from_user_id,
                owner_first_name = owner,
                content = content,
                create_time = dt.datetime.now(),
                priority = int(priority),
                status = 0) # 0 -> todo
    models.database.close()
    return db_task

def complete_task(task_id):
    '''
    Mark tasks as completed in the db.
    '''
    models.database.connect()
    for task_id in task_ids:
        temp_task = models.Task.select().where(
                Task.id == task_id)
        temp_task.status = 2; # deleted
        temp_task.save()
        deleted.append(temp_task)
    
    models.database.close()
    pass

def list_task(owner):
    '''
    list active tasks for the given owner in the 
    orcer of priority

    owner: slack_username
    '''
    models.database.connect()
    try: 
        tasks = models.Task.select().where(
            (Task.owner_slack_username == owner) & 
            (Task.status == 0)
            ).order_by(Task.priority)

        return tasks
    except:
        print("Unexpected error:", sys.exc_info()[0])

    finally:
        models.database.close()

def convert_tasks_to_string(owner, tasks):
    '''
    Order the given list in priority order.
    owner: the user's name
    takss: list of tasks

    return a ready-to-display string
    '''
    out = "*" + owner + "\'s list:" + "*"
    num = 1
    if tasks:
        for task in tasks:
            out = out + "\n" + "*" + str(num) + "*" + " - " + "_" + \
                to_string(task).strip() + "_" + ";\n"
            num += 1
    else:
        # remove the last :
        out = out[:-1] + " is empty! :thumbsup:"

    return out

def days_to_today(db_task):
    return (abs(dt.datetime.now() - 
                db_task.create_time).days)


def to_string(db_task):
    days = days_to_today(db_task)
    out = ""
    if days > 1:
        out += "-" + str(days) + " days"
    elif days == 1:
        out += "-" + str(days) + " day"
    elif days == 0:
        out += "today"
    return (out + " | from " + db_task.from_user + 
                " | " + db_task.content)


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


    def list_tasks(self, owner):
        try: 
            models.database.connect()
            tasks = models.Task.select().where(
                (Task.owner_slack_username == owner) & (Task.status == 0)
                ).order_by(Task.due_time)

            return tasks
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
