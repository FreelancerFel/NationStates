# -*- coding: utf-8 -*-
"""
Modified on Thu Jul 27 10:56:36 2017

@author: aritad.choicharoon
"""

from urllib.request import urlopen
from xml.dom import minidom
import time
import pandas as pd


def count_endo(nation):
    Nation_Name = nation
    website = urlopen("http://www.nationstates.net/cgi-bin/api.cgi?nation="+Nation_Name+"&q=name+region+wa+endorsements")
    data = minidom.parseString(website.read())
    endo = data.getElementsByTagName('ENDORSEMENTS')
    for num in endo:
        if num.firstChild:
            x = (num.firstChild.nodeValue)
            i = 1
            for c in x:
                if c ==',':
                    i = i+1 
            return (i)
        else:
            return (0)


def whatisendo(nation):
    Nation_Name = nation
    time.sleep(0.5)
    website = urlopen("http://www.nationstates.net/cgi-bin/api.cgi?nation="+Nation_Name+"&q=name+region+wa+endorsements")
    data = minidom.parseString(website.read())
    dict = {'Name': '', 'WA_status': '', 'Endo': ''};
    '''
    Getting Nation Name
    '''
    names = data.getElementsByTagName('NAME')
    for name in names:
        nationname = name.firstChild.nodeValue
        dict['Name'] = nationname
    '''
    Checking WA Status?
    if nation is not WA, does not enter count_endo
    '''
    stats = data.getElementsByTagName('UNSTATUS')
    for stat in stats:
        x = (stat.firstChild.nodeValue)
        dict['WA_status'] = x
        a = 0
        if x == 'WA Member' or x == 'WA Delegate':
            a = count_endo(nation)
            dict['Endo'] = a
        else:
            dict['Endo'] = a
    return dict

def regionscan(region):
    website2 = urlopen("http://www.nationstates.net/cgi-bin/api.cgi?region="+region+"&q=nations+numnations+delegate")
    data = minidom.parseString(website2.read())
    numb = data.getElementsByTagName('NUMNATIONS')
    answer = pd.DataFrame()
    for i in numb:
        numc = (i.firstChild.nodeValue)
        print ("Total Number of Nations: "+numc)
    nati = data.getElementsByTagName('NATIONS')
    for i in nati:
        natio = (i.firstChild.nodeValue)
        empty = []
        string = ''
        i = 0
        for n in natio:
            if n == ':':
                empty.append(string)
                string = ''
            elif i == len(natio)-1:
                string = string + n
                empty.append(string)
            elif n != ":":
                string = string + n
            i = i+1
        count = 0
    for i in empty:
        a_dict = whatisendo(i)
        count = count+1
        print (count)
        new_df = pd.DataFrame(a_dict,index=(a_dict['Name'],a_dict['Name'],a_dict['Name'])).iloc[[0]]
        answer = answer.append(new_df)
    return answer


def NS_Scan(regionname):
    liss = regionscan(regionname)
    print ('Region: '+regionname)
    while len(liss) != 0:
        i = 0
        a = liss[i]
        n = 0
        while i < len(liss)-1:
            b = liss[i+1]
            if a['Endo'] < b['Endo']:
                a = b
                n = i+1
            elif a['Endo'] == b['Endo']:
                if len(a['Name']) < len(b['Name']):
                    a = b
                    n = i+1
            i = i+1
        print ('Name: '+a['Name']+"| WA Status: "+a['WA_status']+"| Endorsements: "+str(a['Endo']))
        liss.pop(n)
