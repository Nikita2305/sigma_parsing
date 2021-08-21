import json
import vk_api
import os
from threading import *
from sigma_parsing.data import *
import copy

def log(string):
    print("__LOG__: " + str(string))

def ask_user(string):
    log(string)
    ans = input()
    if (len(ans) == 0):
        return 'n'
    return ans.lower()[0]

def execute_string(string):
    T = Thread(target=os.system, args = (string,))
    T.start()

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()
MAX_ATTEMPT_NUMBER = 5

members = {}

try:
    with open('output/members.txt', 'r') as f:
        members = json.load(f)
except:
    log("members.txt не найден, остановка")
    quit()

i = -1
while((i + 1) < len(members)):
    i += 1
    member = members[i]
    if ((not "processed" in member) or member["processed"]):
        continue
    member_copy = copy.copy(member)
    member_copy.pop("vk_pages")
    member_copy.pop("processed")
    member_copy.pop("official_page")
    log(json.dumps(member_copy, ensure_ascii=False, indent=4))
    OFFSET = 0
    while (OFFSET < MAX_ATTEMPT_NUMBER):
        user = vk.users.search(
            q=member["name"] + " " + member["surname"],
            count=1,
            offset=OFFSET,
            city=104
        )["items"]
        OFFSET += 1
        if (len(user) == 0):
            log("Попытки закончились, переходим к следующему пользователю")
            break
        else:
            user = user[0]
            user_id = user["id"]
            vk_link = "https://vk.com/id" + str(user_id)
            execute_string("google-chrome " + vk_link + " > temp/google-logs.txt 2>temp/google-logs.txt") 
            execute_string("./bash/leftclick.sh")
            ans = ask_user("Это наш? - да(Y), нет(N), пропустить(S), вернуться назад(B)?")
            # execute_string("./bash/rightwindowkill.sh")
            # execute_string("./bash/leftclick.sh")
            print()
            print()
            print()
            if (ans == 'y'):
                member['processed'] = True
                member['official_page'] = user
                with open('output/members.txt', 'w') as f:
                    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
                break
            elif (ans == 'n'):
                continue
            elif (ans == 'b'):
                if (OFFSET == 1):
                    if (i == 0):
                        i -= 1
                    else:
                        i -= 2 
                    break;
                else:
                    OFFSET -= 2
            else:
                break 
            
log("Пользователи закончились!")
