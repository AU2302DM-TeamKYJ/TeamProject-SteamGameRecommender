import json
import random
import urllib.request
import numpy as np
from urllib.parse import urlencode, quote_plus


def get_friends_list(steam_id, api_key):
  """
  Input
    - steam_id : steam ID for one user
    - api_key : API KEY for accessing steam dataset

  Output
    - friends_id_list : list of input user's friends
  """

  get_friends_API_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/"

  queryParams = '?' + urlencode({
      quote_plus('key'): api_key,
      quote_plus('steamid'): steam_id,
      quote_plus('relationship'): 'friend'
  })

  try:
    url = get_friends_API_URL + queryParams
    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)

    friends_id_list = []
    friends_data = json_return.get('friendslist').get('friends')
    for friend in friends_data:

      friends_id_list.append(friend.get('steamid'))

    friends_id_list = np.unique(friends_id_list)
  except:
    friends_id_list = []

  return friends_id_list


def get_friends_in_depth(root_id, api_key, depth):
  """
  Input
    - root_id : steam ID for root user to recursively search friends
    - api_key : API KEY for accessing steam dataset
    - depth : number of depths to go

  Output
    - total_list : list of user ID
  """

  total_list = []
  total_list.extend(get_friends_list(root_id, api_key))  # initialize

  for _ in range(depth):
    random_idx = random.randint(0, len(total_list) - 1)
    total_list.extend(get_friends_list(total_list[random_idx], api_key))

  return total_list


def get_user_info(user_id_list, api_key):
  """
  Input
    - user_id_list : list of user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - user_games_dict : dictionary of user info
    format : 
    {
      "user_id1" : [
        {"appid" : game_id1, "playtime_forever" : playtime1},
        {"appid" : game_id2, "playtime_forever" : playtime2},
        {"appid" : game_id3, "playtime_forever" : playtime3},
        ...
      ],
      "user_id2" : [
          {"appid" : game_id1, "playtime_forever" : playtime1},
          {"appid" : game_id2, "playtime_forever" : playtime2},
          {"appid" : game_id3, "playtime_forever" : playtime3},
          ...
        ],
      ...
    }
  """

  get_games_API_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

  user_games_dict = {}

  for user_id in user_id_list:
    queryParams = '?' + urlencode({
        quote_plus('key'): api_key,
        quote_plus('steamid'): user_id,
        quote_plus('include_played_free_games'): 1,
        quote_plus('format'): 'json'
    })

    url = get_games_API_URL + queryParams

    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)

    if json_return.get('response') == {}:
      continue

    owned_game_list = json_return.get('response').get('games')
    user_games_dict[user_id] = owned_game_list

  return user_games_dict
