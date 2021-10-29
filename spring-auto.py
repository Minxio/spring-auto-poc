"""
springboot检测脚本
‘练习多线程执行’
"""
import argparse
import concurrent.futures
import sys
from colorama import init
import random
import requests
import urllib3

#响应超时
TIMEOUT = 10

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",}

banner = r'''
          *******************
		  SpringBoot Actuator
		  *******************	   
                      '''

def get_args():
    # parser = argparse.ArgumentParser(description='Spring Boot Actuator POC')
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -f urls.log -o out.log")
    parser.add_argument("-f", "--file", dest='f',help='urls地址', required=True)
    parser.add_argument("-t", "--thread", dest='t',help='线程数  默认10', default=10, type=int)
    parser.add_argument("-o", "--output",dest='o', help='打印log')

    return parser.parse_args()

def get_info(filepath):
    try:
        fr = open(filepath,'r')
        urls = fr.read().strip().splitlines()
        fr.close()
        return urls
    except Exception as e:
        print(e)
        exit()

def saveinfo(result):
    if result:
        fw=open(args.o,'a')
        fw.write(result+'\n')
        fw.close()

def print_auto(s):
    t = random.randint(31,36)
    st = '\033[1;' + str(t) +';40m' + s +'\033[0m'
    print(st)

def spring_auto(url):
    path = url + '/env'
    try:
        r = requests.get(path, headers=headers, timeout=TIMEOUT, verify=False)
        if r.status_code == 200 and 'profiles' in r.text:
            print('\033[0;31;40m[+] vulnerability SpringBoot 1.x     \033[0m'+url+'\n',end='')
            if args.o != None: saveinfo(path)
        else:
            path = url  + '/actuator/env'
            r = requests.get(path, headers=headers, timeout=TIMEOUT, verify=False)
            if r.status_code == 200 and 'profiles' in r.text:
                print('\033[0;33;40m[+] vulnerability SpringBoot 2.x     \033[0m'+url+'\n',end='')
                if args.o != None: saveinfo(path)
            else:
                print('[-] Not vulnerability    ' + url+'\n'+'\n',end='')
    except:
        print('[-] Not vulnerability    ' + url+'\n',end='')


if __name__ == '__main__':
    # print(banner)
    print_auto(banner)
    args = get_args()
    max_thread = args.t
    urls = get_info(args.f)
    with concurrent.futures.ThreadPoolExecutor(max_thread) as pool:
        pool.map(spring_auto, urls)
