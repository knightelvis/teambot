import time
import re

from slackclient import SlackClient

from functions.todo import TodoList
from functions.todo import Task
from util import *

class TeamBot:
    '''The TeamBot'''

    def __init__(self, slack_client):
        self.slack_client = slack_client
        self.todos = {}

    def add_todo(self, from_user, from_user_id, owner, content, priority):

        task = Task(from_user, from_user_id, owner, content, priority)
        print(self.todos.get(owner))
        self.todos.setdefault(owner, TodoList(owner)).add_task(task)

    def list_tasks(self, owner):
        return self.todos.get(owner, TodoList(owner)). \
            list_tasks_with_priority()

    def remove_tasks(self, owner, indices):
        return self.todos.get(owner, TodoList(owner)).remove_tasks(indices)

    def convert_user_id_to_name(self, s):
        if s and s.startswith("<@") and s.endswith(">"):
            name = self.slack_client.server.users.find(s[2:-1]).name
            if name:
                return name
        return None

    def cmd_add(self, event):
        '''!add <@U1KFVJMCH> <@U1KFVJMCH> review my codes'''
        msg = event.get("text")
        words = msg.split()
        candidates = []
        owner = event.get("user_name")
        owner_id = event.get("user") # slack unique user id

        # verified
        if words and words.pop(0) == "!add":

            # only the prefixed user names will grab the tasks
            while words:
                name = self.convert_user_id_to_name(words[0])
                if name:
                    candidates.append(name)
                    words.pop(0)
                else:
                    break

            # extract priority
            match = re.fullmatch(r"\[([0-9])\]", words[-1])
            if match:
                priority = match.group(1)
                words.pop()
            else:
                priority = 3  # by default

            # iterate it again in case there are some other names in the msg
            content = ""
            for word in words:
                name = self.convert_user_id_to_name(words[0])
                if name:
                    content += name + " "
                else:
                    content += word + " "

            response = ""

            # add task to the candidates' list; if none, to the owner's list
            if candidates:
                for p in candidates:
                    self.add_todo(owner, owner_id, p, content, priority)
                    response += p + ", "

                # trail the ending ", "
                response[:-2]
            else:
                response += owner
                self.add_todo(owner, owner_id, owner, content, priority)

            response = "*Task:* " + "_" + content.strip() + "_" + \
                " is added for:\n" + response
            self.post_msg(event.get("channel"), response)

    def cmd_list(self, event):
        '''should only be used in the direct message'''
        
        if len(event.get("members")) == 0:
            response = self.list_tasks(event.get("user_name"))
            self.post_msg(event.get("channel"), response)

    def cmd_rm(self, event):
        '''should only be used in the direct message'''

        if len(event.get("members")) == 0:
            words = [x.strip() for x in event.get("text").split()]

            if words and words.pop(0) == "!rm":
                removed = self.remove_tasks(event.get("user_name"), words)
                response = "*Removed tasks:*\n"

                if removed:
                    for task in removed:
                        response += "~" + task.to_string().strip() + "~" + "\n"
                        self.notify_other(task)
                else:
                    response += "None\n"

                response += self.list_tasks(event.get("user_name"))
                self.post_msg(event.get("channel"), response)

    def parse_command(self, msg):
        if msg.startswith("!list"):
            return self.cmd_list
        elif msg.startswith("!add "):
            return self.cmd_add
        elif msg.startswith("!rm "):
            return self.cmd_rm

    def post_msg(self, channel, msg):
        self.slack_client.rtm_send_message(channel, msg)

    def notify_other(self, task):
        
        # if the task is filed by the owner, skip
        if task.owner == task.from_user:
            return

        res = self.slack_client.api_call("im.open", user = task.from_user_id)
        if res.get("ok"):
            direct_id = res.get("channel").get("id")
            response = task.owner + " *has completed task:* \n" + "~" + task.to_string().strip() + "~"
            self.post_msg(direct_id, response)

    def handle_event(self, event):
        type = event.get("type", "")
        subtype = event.get("subtype", "none")

        # only response to message for now
        if type == "message" and subtype == "none":
            user_id = event.get("user", "")
            user_name = self.slack_client.server.users.find(user_id).name
            event["user_name"] = user_name

            raw_msg = event.get("text", "")

            channel_id = event.get("channel", "")
            channel_name = self.slack_client.server.channels. \
                find(channel_id).name
            event["channel_name"] = channel_name

            members = self.slack_client.server.channels. \
                find(channel_id).members
            event["members"] = members

            print("***type:" + type + "\nsubtype:" + subtype +
                  "\nuser_id:" + user_id + "\nuser_name:" + user_name +
                  "\nchannel_id:" + channel_id + "\nchannel_name:" +
                  channel_name + "\nmsg:" + raw_msg + "\nmembers:" + str(len(members)))

            cmd = self.parse_command(event.get("text", "").strip())
            if cmd:
                cmd(event)

    def await(self):
        while True:
            # this returns a list of slack Events?
            events = self.slack_client.rtm_read()

            if len(events) > 0:
                for event in events:
                    print("event:")
                    print(event)
                    self.handle_event(event)

            time.sleep(1)


def main():
    # these variables are imported from util.
    # bot_token 
    # db_name   
    # db_user   
    # db_pwd    

    slack_client = SlackClient(bot_token)

    if slack_client.rtm_connect():
        team_bot = TeamBot(slack_client)
        team_bot.await()
    else:
        print("Connection Failed, invalid token?")

if __name__ == "__main__":
    main()
