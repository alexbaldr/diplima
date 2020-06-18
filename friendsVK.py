import requests
from pprint import pprint
import time
import json

TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"  # input("Введите токен ")

USER_id = 171691064  # input("Введите id пользователя " )


class USER:
    def __init__(self, TOKEN):
        # Параметры для запроса groups.get
        self.token = TOKEN
        self.params = {
            'access_token': TOKEN,
            'v': 5.107,
            "user_id": USER_id}
        return

    def get_response(self):
        response = requests.get(
            'https://api.vk.com/method/groups.get', params=self.params)
        res = response.json()
        if "error" not in res:
            #time.sleep(1)
       # else:
            data = response.json()['response']['items']
            return data

    def get_groups(self):
        a = set()
        data = self.get_response()
        for i in data:
            a.add(i)
        return a

    def get_friends(self):
        params = self.params
        params["order"] = "name"
        params["fields"] = "domain"
        response = requests.get(
            "https://api.vk.com/method/friends.get", params=params)
        get_items = response.json()["response"]["items"]
        # Получаем список id друзей
        list_of_friends = []
        for i in get_items:
            #time.sleep(0.5)
            get_id = i["id"]
            list_of_friends.append(get_id)
        return list_of_friends

    def get_friends_groups(self):
        # Получаем список групп
        b = set()
        list_of_friends = self.get_friends()
        try:
            for i in list_of_friends:
                params = self.params
                params["user_id"] = i
                params["count"] = "1000"
                data = self.get_response()
                for i in data:
                    b.add(i)
        except TypeError:
            return b


    def get_json(self):
        set_of_id = Evg.get_groups() & Evg.get_friends_groups()
        gotten_groups = []
        # ПОЛУЧАЕМ ID ГРУПП
        for i in set_of_id:
            params = self.params
            params["group_id"] = i
            params["count"] = '5'

            response = requests.get(
                'https://api.vk.com/method/groups.getMembers', params=params)
            members_count = response.json()
            for i in members_count:
                time.sleep(0.5)
                members_count_list = members_count["response"]["count"]
                merged = {"members_count": members_count_list}
        # ПОЛУЧАЕМ ДАННЫЕ ГРУПП
            params = {
                'access_token': TOKEN,
                'v': 5.107,
                "group_ids": i
                }
            response = requests.get(
                    'https://api.vk.com/method/groups.getById', params=params)
            data = response.json()
            for i in data:
                time.sleep(0.5)
                res = response.json()["response"]

            for i in res:
                name = i.get("name")
                group_id = i.get("id")
                dict_of_same_groups = {"name": name, 
                "gid": group_id}
                dict_of_same_groups.update(merged)
                gotten_groups.append(dict_of_same_groups)

        # with open('groups.json', 'w',encoding = 'UTF-8') as f:
        #    json.dump(gotten_groups,f,ensure_ascii = False, sort_keys=True, indent=2)
            return gotten_groups

Evg=USER(TOKEN)
print(Evg.get_groups())
#Evg.get_friends()
#print(Evg.get_friends_groups())
#print(Evg.get_json())
