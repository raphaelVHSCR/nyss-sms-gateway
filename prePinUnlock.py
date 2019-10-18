#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import xmltodict
import requests
import json
import time
# import sendEmail

SMS_LIST_TEMPLATE = '''<request>
    <PageIndex>1</PageIndex>
    <ReadCount>20</ReadCount>
    <BoxType>1</BoxType>
    <SortType>0</SortType>
    <Ascending>0</Ascending>
    <UnreadPreferred>0</UnreadPreferred>
    </request>'''

SMS_DEL_TEMPLATE = '<request><Index>{index}</Index></request>'

"""SMS_SEND_TEMPLATE = '''<request>
    <Index>-1</Index>
    <Phones><Phone>{phone}</Phone></Phones>
    <Sca></Sca>
    <Content>{content}</Content>
    <Length>{length}</Length>
    <Reserved>1</Reserved>
    <Date>{timestamp}</Date>
    </request>'''
    """
    

PIN_SET_TEMPLATE = '''
<request>
<OperateType>{}</OperateType>
<CurrentPin>{}</CurrentPin>
<NewPin>{}</NewPin>
<PukCode>{}</PukCode>
</request>
'''

print(PIN_SET_TEMPLATE.format(0, 1348, '', ''))

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def isHilink(device_ip):
    try:
        r = requests.get(url='http://' + device_ip + '/api/device/information', timeout=(2.0,2.0))
    except requests.exceptions.RequestException as e:
        return False;

    if r.status_code != 200:
        return False
    return True
    
def getHeaders(device_ip):
    token = None
    sessionID = None
    try:
        r = requests.get(url='http://' + device_ip + '/api/webserver/SesTokInfo')
    except requests.exceptions.RequestException as e:
        return (token, sessionID)
    try:        
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'TokInfo' in d['response']:
            token = d['response']['TokInfo']
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'SesInfo' in d['response']:
            sessionID = d['response']['SesInfo']
        headers = {'__RequestVerificationToken': token, 'Cookie': sessionID}
    except:
        pass
    return headers
    
def unlockWithPin(device_ip, headers, pin):
    r = requests.post(url = 'http://' + device_ip + '/api/pin/operate', data = PIN_SET_TEMPLATE.format(0, pin, '', ''), headers = headers)
    d = xmltodict.parse(r.text, xml_attribs=True)
    print(d)
   

def disablePin(device_ip, headers, pin):
    r = requests.post(url = 'http://' + device_ip + '/api/pin/operate', data = PIN_SET_TEMPLATE.format(2, pin, '', ''), headers = headers)
    d = xmltodict.parse(r.text, xml_attribs=True)
    print(d)

def getSMS(device_ip, headers):
    r = requests.post(url = 'http://' + device_ip + '/api/sms/sms-list', data = SMS_LIST_TEMPLATE, headers = headers)
    d = xmltodict.parse(r.text, xml_attribs=True)
    print(d)
    # numMessages = int(d['response']['Count'])
    # messagesR = d['response']['Messages']['Message']
    # if numMessages == 1:
    #     temp = messagesR
    #     messagesR = [temp]
    # messages = getContent(messagesR, numMessages)
    # return messages, messagesR

# def getContent(data, numMessages):
#     messages = []
#     for i in range(numMessages):
#         message = data[i]
#         number = message['Phone']
#         content = message['Content']
#         date = message['Date']
#         messages.append('Message from ' + number + ' recieved ' + date + ' : ' + str(content))
#     return messages

# def delMessage(device_ip, headers, ind):
#     r = requests.post(url = 'http://' + device_ip + '/api/sms/delete-sms', data = SMS_DEL_TEMPLATE.format(index=ind), headers = headers)
#     d = xmltodict.parse(r.text, xml_attribs=True)
#     print(d['response'])

# def getUnread(device_ip, headers):
#     r = requests.get(url = 'http://' + device_ip + '/api/monitoring/check-notifications', headers = headers)
#     d = xmltodict.parse(r.text, xml_attribs=True)
#     unread = int(d['response']['UnreadMessage'])
#     return unread

if __name__ == "__main__":

    device_ip = '192.168.8.1'
    if not isHilink(device_ip):
        if not isHilink('hi.link'):
            print("Can't find a Huawei HiLink device on the default IP addresses, please try again and pass the device's IP address as a parameter")
            print('')
            sys.exit(-1)
        else:
            device_ip = 'hi.link'
            
    # headers = getHeaders(device_ip)
    getSMS(device_ip, getHeaders(device_ip))
    # unlockWithPin(device_ip, getHeaders(device_ip), 1348)
    # time.sleep(5)
    # disablePin(device_ip, getHeaders(device_ip), 1348)

