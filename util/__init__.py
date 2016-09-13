
# read the some config data, should be global accessible
with open("./config.key", "r") as f:
    bot_token = f.readline().strip()
    db_name   = f.readline().strip()
    db_user   = f.readline().strip()
    db_pwd    = f.readline().strip()