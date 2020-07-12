import requests
import time
import json

TOKEN = input("Введите токен ") # "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
USER_id = input("Введите id пользователя ") # "171691064" 18526683


class USER:

    def __init__(self, TOKEN):
        self.token = TOKEN
        return

    def get_groups(self):
        groupset = set()       
        response = requests.post('https://api.vk.com/method/execute?access_token='+TOKEN+'&v=5.107&code=return API.groups.get({"user_id":"'+USER_id+'","count":"1000"});')
        data = response.json()['response']['items']
        for i in data:
            groupset.add(i)
        return groupset

    def get_friends(self):
        friendset = set()
        response = requests.post('https://api.vk.com/method/execute?access_token='+TOKEN+'&v=5.107&code=return API.friends.get({"user_id":"'+USER_id+'","count":"1000","extended": 0, "order":"name"});')
        data = response.json()['response']['items']
        for i in data:
            friendset.add(i)
        return friendset

    def get_friends_groups(self):
        groups_friend_set = set()
        groups = self.get_groups()        
        for i in self.get_friends():
            time.sleep(0.5)
            response = requests.post('https://api.vk.com/method/execute?access_token='+TOKEN+'&v=5.107&code=return API.groups.get({"user_id":"'+str(i)+'","count":"1000","extended": 0});')
            data_fr = response.json()
            if 'response' in data_fr.keys():
                data = response.json()['response']['items']
                for group_id in data:
                    if group_id in groups:
                        groups_friend_set.add(group_id)
        return groups_friend_set

    def get_json_file(self):
        gotten_groups = []
        for i in self.get_friends_groups():
            r = requests.post('https://api.vk.com/method/execute?access_token='+TOKEN+'&v=5.107&code=return API.groups.getById({"group_ids":"'+str(i)+'","fields":"members_count"});')
            data = r.json()['response']
            time.sleep(0.5)
            for i in data:
                vk_dict = {"name": i["name"], "gid": i['id'], "members_count": i['members_count']}
                gotten_groups.append(vk_dict)
        with open('groups.json', 'w', encoding='UTF-8') as f:
            json.dump(gotten_groups, f, ensure_ascii=False, sort_keys=True, indent=2)

        return gotten_groups

Evg = USER(TOKEN)

print(Evg.get_json_file())
