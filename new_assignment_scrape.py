from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta

load_dotenv()
os.environ['Path'] += r"C:\Web_Drivers\geckodriver-v0.35.0-win64"

def login(browser):
    browser.get("https://portal.svkm.ac.in/usermgmt/login")
    time.sleep(3)
    username=os.getenv("ID")
    password=os.getenv("PASS")

    elementID = browser.find_element(By.ID, 'userName')
    elementID.send_keys(username)
    elementID = browser.find_element(By.ID, 'userPwd')
    elementID.send_keys(password)
    time.sleep(5)
    elementID.submit()
    time.sleep(15)
    
def get_assignment(browser, assignment_link):
    arr = []
    browser.get(assignment_link)
    time.sleep(5)
    table_id = browser.find_element(By.ID, 'viewAssignmentTable')
    rows = table_id.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        arr.append([col.text for col in cols])
            
    return arr
        
def find_latest_assignment(arr):
    new_assignment = []
    for assignment in arr:
        if len(assignment) < 3:
            continue
        
        start_date = assignment[1]
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        current_time = datetime.now()
        
        time_diff = current_time - timedelta(hours=12)

        if start_date_obj >= time_diff and start_date_obj <= current_time:
            print("The date and time is within the last 12 hours.")
            new_assignment.append(assignment)
            
        else:
            print("The date and time is not within the last 12 hours.")
            
    return new_assignment

def parse_to_text(latest_assignmnets):
    if not latest_assignmnets:
        return "Checked Portal, no new ADS assignment."
    
    text = ""
    for assignment in latest_assignmnets:
        text += f"""
Assignmnet Name: {assignment[0]}
Start Date: {assignment[1]}
End Date: {assignment[2]}

        """
        
    return text
    
def ads_assignment_scrape(): 
    browser = webdriver.Firefox()
    login(browser)
    arr = get_assignment(browser, "https://portal.svkm.ac.in/MPSTME-NM-M/viewAssignmentFinal?courseId=5295774650332686")
    arr += get_assignment(browser, "https://portal.svkm.ac.in/MPSTME-NM-M/viewAssignmentFinal?courseId=5295774350332686")
    print(arr)
    latest_assignmnets = find_latest_assignment(arr)
    browser.quit()
    text = parse_to_text(latest_assignmnets)
    return text
    
if __name__ == "__main__":
    ads_assignment_scrape()