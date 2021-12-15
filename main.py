from instabot import Bot
from dotenv import load_dotenv
from pathlib import Path
import os


def import_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    login=os.environ.get('Login')
    password=os.environ.get('Password')
    return login, password




# bot = Bot()
#
# bot.login(username = "user_name",
# 		password = "user_password")
#
# # Recommended to put the photo
# # you want to upload in the same
# # directory where this Python code
# # is located else you will have
# # to provide full path for the photo
# bot.upload_photo("Technical-Scripter-2019.jpg",
# 				caption ="Technical Scripter Event 2019")



if __name__ == "__main__":
    print ("Executed when invoked directly")
    user_name, user_password = import_env()
    print(user_name, user_password)

else:
    print ("Executed when imported")
