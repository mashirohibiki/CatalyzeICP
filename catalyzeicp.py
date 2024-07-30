'''
Author: Catalyze
Date: 2024-07-30 10:51:30
LastEditTime: 2024-07-30 20:09:10
FilePath: /python/icp.py
Description: 通过爬取该网站https://www.icpapi.com/来获得icp子备案号,目前该网站限制单IP一天内可访问20次
'''

import argparse
import urllib.parse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def banner():
    print()
    print(r'''     ______      __        __                 ______________ 
    / ____/___ _/ /_____ _/ /_  ______  ___  /  _/ ____/ __ \
   / /   / __ `/ __/ __ `/ / / / /_  / / _ \ / // /   / /_/ /
  / /___/ /_/ / /_/ /_/ / / /_/ / / /_/  __// // /___/ ____/ 
  \____/\__,_/\__/\__,_/_/\__, / /___/\___/___/\____/_/      
                         /____/                              ''')
    print()

def get_icp_info(icp):
    print("正在查询中,请稍等......")
    root = 'https://www.icpapi.com/'
    url = root + urllib.parse.quote(icp)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=chrome_options)

    # html结果提取
    def output(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        main_registration = soup.find_all('table', class_='table table-bordered')[0]
        main_rows = main_registration.find_all('tr')
        registration_number = icp
        entity_type = main_rows[0].find_all('td')[1].text
        entity_name = main_rows[1].find_all('td')[1].text

        sub_registration = soup.find_all('table', class_='table table-bordered')[1]
        sub_rows = sub_registration.find('tbody').find_all('tr')

        sub_info = []
        for row in sub_rows:
            cells = row.find_all('td')
            sub_info.append({
                'sub_registration_number': cells[0].text.strip(),
                'domain': cells[2].text.strip()
            })

        print(f"{registration_number}")
        print(f"备案类型: {entity_type}")
        print(f"备案主体: {entity_name}\n")

        print("子备案号\t\t备案域名")
        for info in sub_info:
            print(f"{info['sub_registration_number']}\t{info['domain']}")

    try:
        driver.get(url)
        time.sleep(5)  # 等待页面加载

        output(driver.page_source)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

def get_file_icp_info(filename):
    with open(filename, 'r') as f:
        file_data = f.readlines()
        for fi_s in file_data:
            fi_s = fi_s.strip('\n')
            get_icp_info(fi_s)
            time.sleep(5)

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description='一个主备案号查子备案号的小工具')
    parser.add_argument('-info', type=str, help='可指定备案号,公司名称')
    parser.add_argument('-file', type=str, help='指定文件')

    args = parser.parse_args()
    if args.info:
        get_icp_info(args.info)
    elif args.file:
        get_file_icp_info(args.file)
    else:
        parser.print_help()