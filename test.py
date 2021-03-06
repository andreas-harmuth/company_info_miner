
import linkedIn
import json

login_auth = open('login_auth.json', 'r')
login = json.load(login_auth)

f = open('/Users/andreasharmuth/Google Drive/company_info_miner/last_history_links.txt')

href_list = [link for link in f.read().split("\n")]




employment_dict = linkedIn.get_user_info_by_list(href_list,login['user'],login['password'])



file_log = ""
f = open('last_history.txt', 'w')

for name in employment_dict:
    file_log += "=" * 50 + '\n'
    file_log += "Name: " + employment_dict[name]["name"] + '\n'
    file_log += "Link: " + name + '\n'
    if (employment_dict[name]["connections"]) == 501:
        file_log += "Connections: 500+\n"

    else:
        file_log += "Connections: " + str(employment_dict[name]["connections"])  + '\n'
    file_log += "-" * 50 + '\n'
    for employments in employment_dict[name]["experience"]:
        file_log += "Company: " + employments["company"] + '\n'
        file_log += "Employment: " + employments["employment"] + '\n'
        file_log += "Duration: " + employments["duration"] + '\n' + '\n'
    file_log += "-" * 50 + '\n'

    for skill in employment_dict[name]["skills"]:
        file_log += "Skill: " + skill ["skill"] + '\n'
        file_log += "endorsements: " + str(skill["endorsements"]) + '\n'+'\n'
    file_log += "-" * 50 + '\n'+'\n'
f.write(file_log)
f.close()  # you can omit in most cases as the destructor will call it
