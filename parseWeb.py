import urllib.request as reqt
from bs4 import BeautifulSoup
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import time

def get_webInfo(url,filter):
    head = {}
    head['User-Agent']='Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
    req=reqt.Request(url,headers=head)
    rsp=reqt.urlopen(req)
    html=rsp.read().decode('gb2312','replace')

    html=BeautifulSoup(html,'html.parser')
    info=html.find_all('div', attrs=filter)
    examinfo=''
    for pa in info:
        for p in pa.find_all('p'):
            examinfo+=p.get_text()
            examinfo+='\n'

    print('===>parsing the webpage finsished and content is \n ' + examinfo)
    return examinfo

def sendemail(subject,article,receiver):
    host='smtp.163.com'
    user="kxsyr"
    passwd="<put the dynamics passwd here, can be get from 163.com>"
    sender = 'kxsyr<kxsyr@163.com>'
    coding = 'utf-8'
    message = MIMEText(article,'plain',coding)
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(subject,coding)

    try:
        mail_client = smtplib.SMTP_SSL(host,465)
        #mail_client.set_debuglevel(1)
        mail_client.login(user,passwd)
        mail_client.sendmail(sender,[receiver],message.as_string())
        mail_client.quit()
        print('email send successfully')
    except smtplib.SMTPException as e:
        print('failed to send email')
        print(e)

tmp={'history':None}

def check(url):
    filter={'class':'main_content main_content02'}
    now = get_webInfo(url,filter)
    if(tmp['history']):
        history = tmp['history']
        updated = False
        if(len(history) == len(now)):
            result=''
            for a,b in zip(history,now):
                if a == b:
                    continue
                else:
                    result = now
                    sendemail('page get updated 123',result,'autokxs<autokxs@163.com>')
                    updated = True
                    break
            if(updated):
                print('===>your webpage has get updated please check your email\n')
            else:
                print('===>nothing get updated \n')
        else:
            print('===>your webpage has get updated please check your email\n')
        tmp['history'] = now
    else:
        print('===>this is the first time to check')
        tmp['history'] = now
        #sendemail('page get updated 123',examinfo,'autokxs<autokxs@163.com>')

if __name__ == "__main__":
    url='https://js.huatu.com/guojia/'
    while True:
        check(url)
        print('sleep for 5 hours')
        time.sleep(5*3600)
        print('start checking')
