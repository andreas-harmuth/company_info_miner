from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json





















def filter_employee(unfiltered):
    for check_int in unfiltered.split(" "):  # Assume only one integer. This is a good assumption given linkedIn build
        del_words = [".","+"]
        new_char = "" # Custom replace

        for char in check_int: # Counter thousand separator and more than (+)
            if char not in del_words:
                new_char += char
        check_int = new_char

        try:

            int(check_int)  # Assign and test at once

            return int(check_int)
        except:
            pass

    else:
        return (0)  # Same as setting to false, but easier with to check














def scroll_and_load(driver,jmp=100,slow=1):


    #offset = driver.find_element_by_class_name(class_name).location["y"]
    for i in range(0,4000,jmp):

        driver.execute_script(
            "window.scrollTo(0,"+ str(i) +");")  # Get all the links - loads on scroll
        time.sleep(1/100*slow)






















def login(driver,first_url,email,password,slower = 1):
    timeout = 10
    ################ LOGIN ##################
    driver.get(first_url)
    start = time.time()
    while time.time() < start + timeout:
        try:
            driver.find_element_by_class_name("sign-in-link").click()
            break
        except:
            pass

    start = time.time()
    while time.time() < start + timeout:
        try:
            un = driver.find_element_by_class_name('form-password')
            pw = driver.find_element_by_class_name('password_wrapper')
            un.send_keys(email)
            pw.click()  # As this is a password, you have to click it!
            pw.send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_id('btn-primary').click()
            break
        except:
            pass
    # TODO: check if logged in and then move:
        """
        un.send_keys(email)
            pw.click()  # As this is a password, you have to click it!
            pw.send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_id('btn-primary').click()
        """







def force_login(driver,email,password):

    timeout = 10

    start = time.time()
    while time.time() < start + timeout:
        try:
            un = driver.find_element_by_class_name('form-password')
            pw = driver.find_element_by_class_name('password_wrapper')
            break
        except:
            pass

    un.send_keys(email)
    pw.click()  # As this is a password, you have to click it!
    pw.send_keys(password)
    time.sleep(0.5)
    driver.find_element_by_id('btn-primary').click()


















def scrape_data(driver,url,slower=1):
    ############# Check number for most business #################
    if url != None:
        driver.get(url)
    time.sleep(3 * slower)  # Let the page load
    employee_element = driver.find_element_by_class_name(
        'org-company-employees-snackbar__see-all-employees-link').get_attribute('innerHTML')

    # Assumption based on linkedIn build ie. that the information is in the strong tag
    employee_strong = employee_element.split("strong")[1]

    employee_number = filter_employee(employee_strong)

    ############# Give estimate if above fails #################
    if (employee_number == 0):
        company_main_info = 'company-size'
        employee_element = driver.find_element_by_class_name(company_main_info).get_attribute('innerHTML')
        employee_number = filter_employee(employee_element)

    #################### GET NAME OF COMPANY #####################

    name_class = 'org-top-card-module__name'

    name = driver.find_element_by_class_name(
        name_class).get_attribute('innerHTML').strip()

    #################### RETURN ######################

    if (employee_number == 0):
        employee_number = "No employees found"

    return name,employee_number
# Optimize: https://www.scrapehero.com/tutorial-scraping-linkedin-for-public-company-data/
















def number_of_employees_by_id(listOfCompanyIDs,email,password):


    # Set driver
    driver = webdriver.Firefox()

    # Init the dict
    employee_number_dict = {}

    # Give the first url
    login(driver,listOfCompanyIDs[0],email,password)
    listOfCompanyIDs[0] = None #To make sure the url won't reload


    for url in listOfCompanyIDs:

        name,employee_number = scrape_data(driver,url)
        employee_number_dict[name] = employee_number



    driver.close()  # Terminate the driver

    return employee_number_dict













def number_of_employee_links_by_id(company_id,email,password,slower=1):
    timeout = 10
    # Set driver
    driver = webdriver.Firefox()

    url = 'https://www.linkedin.com/company-beta/'+ str(company_id) + '/'
    employee_links = []

    # Give the first url
    login(driver, url, email, password)

    time.sleep(5*slower)
    start = time.time()
    while time.time()<start+timeout:
        try:
            driver.find_element_by_class_name('snackbar-description-see-all-link').click()
            break
        except:
            pass

    time.sleep(4 * slower)

    try:
        pages_list = len(driver.find_element_by_class_name('page-list').find_elements_by_tag_name('li'))
        if pages_list == 0:
            pages_list = 1
    except:
        pages_list = 1

    main_url = driver.current_url



    for i in range(pages_list):
        driver.get(main_url + '&page='+str(i+1))
        time.sleep(3 * slower)
        scroll_and_load(driver, jmp=50, slow=10)

        user_elements = driver.find_elements_by_class_name('search-result__image-wrapper')
        for user in user_elements:
            if len(user.find_element_by_class_name('search-result__result-link').get_attribute('href').split('https://www.linkedin.com/search/results/people/')) > 1:
                employee_links.append('OON') # Check if the person if out of the network
            else:
                # Append valid links to the list
                employee_links.append(user.find_element_by_class_name('search-result__result-link').get_attribute('href'))



    driver.close()  # Terminate the driver
    return employee_links















def get_user_info_by_list(urls, email, password,slow=1):
    print(urls)
    urls = [url for url in urls if url != 'OON'] # Only get the urls that contain valid people
    print(urls)
    timeout = 10
    driver = webdriver.Firefox()
    employee_info = {}



    for index,url in enumerate(urls):
        if index != 0:
            driver.get(url)

        else:
            driver.get(url)
            driver.find_element_by_class_name('nav-signin').click()
            force_login(driver, email, password)
            time.sleep(3)
            driver.get(url)


        start = time.time()
        while time.time() < start + timeout:
            try:
                name = driver.find_element_by_class_name('pv-top-card-section__name').get_attribute('innerHTML')
                break
            except:
                pass



        # Have to load the JS-generated html by scrolling
        scroll_and_load(driver)

        ######################## Common info #############################

        for c in driver.find_element_by_class_name('pv-top-card-section__connections').find_element_by_class_name(
            'svg-icon-wrap').find_element_by_class_name('visually-hidden').get_attribute('innerHTML').split(" "):

            if c == "500+":
                conn = 501
                break
            try:
                conn = int(c)
                break
            except:
                pass
        else:
            conn = 0


        # We can assume the name to be unique, but the url must be!
        employee_info[url] = {
            "connections" : conn,
            "name": name,
            "experience": [],
            "skills": []
        }

        ######################## Expand hiddens #############################
        try:
            btn_div = driver.find_element_by_class_name('pv-profile-section__actions-inline')
            btn_div.find_element_by_class_name('link').click()
            time.sleep(2*slow)
        except:
            pass

        try:
            driver.find_element_by_class_name('pv-profile-section__see-more-inline link').click()
            time.sleep(2 * slow)
        except:
            pass


        try:
            driver.find_element_by_class_name('pv-skills-section__additional-skills').click()
            time.sleep(2 * slow)
        except:
            pass


        ######################## Employment information #############################
        ele = driver.find_elements_by_class_name('pv-profile-section__section-info')[1]
        for p in (ele.find_elements_by_tag_name('li')):
            for h3, h4 in zip(p.find_elements_by_tag_name('h3'), p.find_elements_by_tag_name('h4')):

                #print(h4.find_element_by_class_name('pv-entity__date-range').get_attribute('innerHTML'))
                employee_info[url]["experience"].append({
                    "company" : h4.find_element_by_class_name('pv-entity__secondary-title').get_attribute('innerHTML'),
                    "duration": p.find_element_by_class_name('pv-entity__date-range').find_elements_by_tag_name('span')[1].get_attribute('innerHTML'),
                    "employment" : h3.get_attribute('innerHTML')
                })


        ######################## Employment information #############################
        all_skills = driver.find_elements_by_class_name('pv-skill-entity--featured')

        for skill in all_skills:
            employee_info[url]["skills"].append({
                "skill" : skill.find_element_by_class_name('pv-skill-entity__skill-name').get_attribute('innerHTML'),
                "endorsements" : filter_employee(skill.find_element_by_class_name('visually-hidden').get_attribute('innerHTML'))
            })

    driver.close()  # Terminate the driver
    return employee_info


