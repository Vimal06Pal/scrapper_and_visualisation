import os
import selenium
from selenium import webdriver
import time,datetime
from webdriver_manager.chrome import ChromeDriverManager
from csv import writer
from selenium.webdriver.common.by import By
import pandas as pd








""" Scraper class scrap all data from SCRAP_UK_Cabinet_Contracts  """


class Scrper:
    
    def __init__(self):
        pass

    """ Scraper clas use for scraping, where we are using Selenium library,
    In whole proccess we are taking Xpath for scrping.
    
    """

    def scrap_uk_cabinet_contracts(self):
        
        """ here we are creating driver of Chrome"""
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        """  here we are using implicitly_wait(), for load data of website properly.
        """
        driver.implicitly_wait(10)
        
        driver.get('https://www.gov.uk/contracts-finder')
        
        element=driver.find_element("xpath", '/html/body/div[3]/main/div/div[2]/div/div/section[1]/p/a')
        element.click()
        input_field = driver.find_element("id", 'home_keywords')
        input_field.send_keys("cabinet")
        search=driver.find_element("id", 'adv_search')
        awrded_click=driver.find_element("id", 'awarded')
        awrded_click.click()
        search.click()
        driver.find_element("xpath","/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[2]/ul/li[7]/a").click()
        pages=driver.find_element("xpath","/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[2]/ul/li[8]/span[2]").text
        time.sleep(2)
        driver.find_element("xpath","/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[2]/ul/li[2]/a").click()
        time.sleep(2)
        search_data=driver.find_elements("xpath","/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]")
        data_lst=[]
        page=1
        
        """ Here we are iterate all the page of website pagination, 
            and scrape all data of the page.
        """
        # while page <= int(pages):
        while page <=3:  #--------------------> thise is use for statice page
            if page >=2:
                url=f"https://www.contractsfinder.service.gov.uk/Search/Results?&page={page}#dashboard_notices"
                driver.get(url)
                search_data=driver.find_elements("xpath","/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]")
            for i in search_data:
                count=1
                for data in i.find_elements("xpath",".//*"):
                    if count < 21:
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[1]"
                        contracts=data.find_element("xpath",path)
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[2]"
                        Agency_name=data.find_element("xpath",path) 
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[4]"
                        description=data.find_element("xpath",path)
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[6]"
                        procurement_stage=data.find_element("xpath",path).text
                        procurement_stage=procurement_stage.lstrip("Procurement stage ")
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[7]"
                        contracts_location=data.find_element("xpath",path).text
                        contracts_location=contracts_location.lstrip("Contract location ")
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[8]"
                        Awarded_vlaue=data.find_element("xpath",path).text
                        Awarded_vlaue=Awarded_vlaue.lstrip("Awarded value ")
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[9]"
                        Awarded_supplier=data.find_element("xpath",path).text
                        Awarded_supplier=Awarded_supplier.lstrip("Awarded supplier ")
                        path=f"/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div[1]/div{[count]}/div[10]"
                        publication_date=data.find_element("xpath",path).text
                        publication_date=publication_date.lstrip("Publication date ")
                        temp_lst=[contracts.text,Agency_name.text,description.text,procurement_stage,contracts_location,Awarded_vlaue,Awarded_supplier,publication_date]
                        count = count+1
                        data_lst.append(temp_lst)
                        
            page=page+1 
        print("==============Scraping Completed=================")
        return data_lst           




    """ thise method is use for Insert Scrape data in CSV format """
   
    def Insert_data_csv(self,data):
        csv_heding=["Contracts","Agency name","Description","Procurment stage","Contract location","Awarded value","Awarded supplier","Publiscation date"]
        df = pd.DataFrame(data, columns = csv_heding)
        df.to_csv("./data.csv",index=False) 
        print("==============Convert_csv Done==================")






""" Here we are creating object of Scraper class and call SCRAP_UK_Cabinet_Contracts 
    method to Scrape data of website ,and also call Insert_data_csv for Insret data in CSV
"""

obj=Scrper()
data=obj.scrap_uk_cabinet_contracts()
obj.Insert_data_csv(data)
   


