from InstagramAPI import InstagramAPI
import time
import random
import argparse
import sys

def GetAllFollowing(bot, user_id):
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowings(user_id, maxid=next_max_id)
        following.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    following = set([_['pk'] for _ in following])
    return following

def GetAllFollowers(bot, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    followers = set([_['pk'] for _ in followers])
    return followers

if __name__ == '__main__':

    # parse cmd line args
    parser = argparse.ArgumentParser(description='Unfollow instagram users that don\'t follow you back!.')
    parser.add_argument('username', help='your instagram username')
    parser.add_argument('password', help='your instagram password')

    parser.add_argument('-n', '--num_unfollows', type=int, default=50,
                        help='Max number of users to unfollow in session')
    parser.add_argument('-d', '--max_delay', type=int, default=5,
                        help='Max seconds to wait between unfollow calls')

    args = parser.parse_args()


    # get credentials, authenticate
    ig = InstagramAPI(args.username, args.password)

    # success is just a bool
    success = ig.login()
    if not success:
        print('INSTAGRAM LOGIN FAILED!')
        sys.exit()

    # fetch your own primary key
    ig.getSelfUsernameInfo()
    self_id = ig.LastJson['user']['pk']

    # loop through json for followers/following
    followers = GetAllFollowers(ig, self_id)
    following = GetAllFollowing(ig, self_id)
    print('- following {} users'.format(len(following)))
    print('- followed by {} users'.format(len(followers)))

    # they don't reciprocate
    unreciprocated = following - followers

    # i don't reciprocate
    free_followers = followers - following

    print('- following {} users that dont follow back'.format(len(unreciprocated)))
    print('- you have {} followers that you dont follow back\n'.format(len(free_followers)))

    # loop through unreciprocated users and unfollow w/ random delay
    for _ in list(unreciprocated)[:min(len(unreciprocated), args.num_unfollows)]:
        ig.getUsernameInfo(str(_))
        print('  - unfollowing user {}'.format(ig.LastJson['user']['username']))
        ig.unfollow(str(_))
        time.sleep(random.uniform(1, args.max_delay))
