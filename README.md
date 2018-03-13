# Instagram-Unfollower
Automatically unfollow users that don't follow you back on Instagram! Runs from the command line so you can set it up as a cron job.

## Use
Depends on `InstagramAPI` module, which you can [find out about here](https://github.com/LevPasha/Instagram-API-python).

Just run the `unfollow.py` script from your terminal with your username and password. Optional arguments `-d` and `-n` can configure the maximum random delay between follows (in seconds) and the maximum number of unfollows to make in one pass.

Example:
```
python unfollow.py 'your_username' 'your_password' -n 50 -d 10
```
