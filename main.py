
import linkedIn
import cvr_miner as cm
import json

login_auth = open('login_auth.json', 'r')
login = json.load(login_auth)

class Company:

    def __init__(self,linkedInID, cvr):
        all_info = cm.cvr_all_info(cvr)
        self.lid = str(linkedInID)
        self.cvr = str(cvr)
        self.name = all_info['name']
        self.startdate = all_info['startdate']
        self.employees_number = all_info['employees']
        self.active = (all_info['enddate'] == None)
        self.address = {
            'address' : all_info['address'],
            'city' : all_info['city'],
            'zipcode': all_info['zipcode']
        }



    def employee_info(self,email,password):
        href_list = linkedIn.number_of_employee_links_by_id(self.lid, email, password)
        f = open('last_history_links.txt', 'w')
        for link in href_list:
            f.write(link + '\n')
        f.close()


        return linkedIn.get_user_info_by_list(href_list, email, password)


    def download_annual_report(self,location):

        return location


company1 = Company(725309,32163289)











#Test
employment_dict = company1.employee_info(login['user'],login['password'])




file_log = ""
f = open('last_history', 'w')

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
