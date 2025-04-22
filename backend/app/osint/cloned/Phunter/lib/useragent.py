import os 
current_dir = os.path.dirname(os.path.abspath(__file__))
useragent_File =  os.path.join(current_dir, '../', 'useragents.txt')
user_agent = []
with open(useragent_File, "r") as user:
    user_agent = user.read().split('\n')