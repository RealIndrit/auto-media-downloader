import praw
from prawcore.exceptions import ResponseException
from reddit.reddit import RedditPost
from reddit.reddit_helper import download_reddit_assets
from utils.text_processor import pre_process_text
from utils import settings

CONFIG = "config.json"

def example():
   # Authenticate Praw
   try:
      reddit = praw.Reddit(
         client_id=settings.config["reddit"]["credentials"]["client_id"],
         client_secret=settings.config["reddit"]["credentials"]["client_secret"],
         user_agent="Accessing Reddit threads",
         check_for_async=False
      )
   except ResponseException as e:
      match e.response.status_code:
         case 401:
            print("Invalid credentials - please check them in config.json")
   except:
      print("Something went wrong...")


   # Fetch specified post or exit program if no post id specified
   if settings.config["reddit"]["post_id"]:
      submission = reddit.submission(
            id=settings.config["reddit"]["post_id"])
   else:
      print("No post id found, aborting!")
      exit()

   reddit_post = RedditPost(submission)
   download_reddit_assets(reddit_post=reddit_post, path="downloaded", tts=True, text_file=True, screenshot=True, comments=20, pre_process_func=pre_process_text)

if __name__ == "__main__":
    try:
        settings.load_config(CONFIG)
        example()
        settings.save_config(CONFIG)
    except Exception as e:
        print("Error!", e)
