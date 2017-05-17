#coding:-utf-8-

import re

def check_error1():   #check LACK_OF_MEMORZ_SEGMENT
    flag1=0
    flag2=0
    with open('MOD_PAR.txt','r') as f:
        txt=f.read()
        f.close()
    if re.search('/begin MEMORY_SEGMENT',txt)==None:
        print 'lack of begin'
        flag1=1
    if re.search('/end MEMORY_SEGMENT',txt)==None:
        print 'lack of end'
        flag2=1
    return flag1|flag2

def check_error2():    #check OPTIONAL
    with open('XCP.txt','r') as f:
        txt=f.read()
        f.close()
    l=txt.split('\n')
    if re.match(r'.*CCP',l[0])!=None:
        ms=re.findall(r'OPTIONAL_CMD 0x[\d\w]+',txt)
        if len(ms)!=10:
            return 1
        else:
            return 0
    else:
        print 'not CCP'
        return 0

def check_error3():     #check keyword: DAQ_RESUME_SUPPORTED
    with open('A2ML.txt','r')as f:
        txt=f.read()
        f.close()
    n=0
    for m in re.finditer('DAQ_RESUME_SUPPORTED',txt):
        if m!=None:
            n+=1
    if n!=0:
        return 1
    else:
        return 0

def check_error4():                #检查双引号
    l=[]
    with open('REST.txt','r')as f:
        for s in f.readlines():
            l.append(s)
        f.close()
    enum=0
    c=[]
    para=0                         #para用于标记换行符数量
    for p in range(len(l)):
        if para==0:                #在上一行没有换行的情况下
            countq=len(re.findall('"',l[p]))
            countb=len(re.findall(r'\\\\"',l[p]))
            countz=len(re.findall(r'\\"',l[p]))
            count=countq+countb-countz
            if count%2==1:         #初始行双引号为奇数时
                s=l[p]
                #print s
                if len(s)>2:       #若该行长度大于等于3时，（为了避免s[-3]不存在）
                    #print s[-2],s[-3]
                    if (s[-2]=='\\')&(s[-3]=='\\'):  #若结尾存在换行符，则进入下一行判断
                        #print 'go next para'
                        para+=1
                        continue
                    else:          #若结尾没有换行符，则该行缺少双引号
                        #print 'lack of "'
                        c.append(p)
                        enum+=1
                else:              #若长度小于3，则除了\n，一定只剩一个双引号，所以缺少双引号
                    #print 'lack of "'
                    c.append(p)
                    enum+=1
        if para!=0:                #在上一行换行的情况下
            #print 'get in para!=0'
            count+=len(re.findall('"',l[p]))
            if count%2==1:         #两行双引号数量和为奇数时
                s=l[p]
                #print s
                if len(s)>2:       #判断s[-3]是否存在
                    #print s[-2],s[-3]
                    if (s[-2]=='\\')&(s[-3]=='\\'):  #若结尾存在换行符，则进入下一行判断
                        para+=1
                        continue
                    else:          #若结尾没有换行符，则缺少双引号
                        #print 'lack of "'
                        c.append(p)
                        enum+=1
                        para=0     #结束本次判断，换行符清零
                else:              #若长度小于3，则除了\n，一定只剩一个双引号，所以缺少双引号
                    print 'lack of "'
                    c.append(p)
                    enum+=1
            else:                  #若没有缺少双引号，换行符清零
                para=0
    if enum==0:
        return [0,None]
    else:
        #print 'lack %d "'%enum
        return [1,c]

def check_error5(): #检查characteristic中有没有'FIXED_EVENT_LIST'字段，有就返回1，没有返回0
    with open('CHARACTERISTIC.txt','r') as f:
        txt=f.read()
        f.close()
    m=re.search('FIXED_EVENT_LIST',txt)
    if m==None:
        return 0
    else:
        return 1
def check_error5_2():
    #该方法用于不将characteristic从REST中分离出来的情况下判断是否存在ERROR5，即characteristic段中存在'FIXED_EVENT_LIST'
    with open('REST.txt','r') as f:
        txt=f.read()
        f.close()
    s=[]
    e=[]
    re_lx1 = re.compile(r'/begin CHARACTERISTIC[\s|\S]+?/end CHARACTERISTIC')
    re_lx2 = re.compile(r' +/begin IF_DATA XCP\
    [\s|\S]+?FIXED_EVENT_LIST[\s|\S]+?/end IF_DATA')
    for m in re.finditer(re_lx1,txt):
        s.append(m.start())
        e.append(m.end())
    s2=[]
    e2=[]
    for m in re.finditer(re_lx2,txt):
        for i in range(len(s)):
            if (m.start()>s[i])&(m.end()<e[i]):
                s2.append(m.start())
                e2.append(m.end())
    if len(s2)!=0:
        return 1
    else:
        return 0

def check_error6():#检查MOD_COMMON中有没有ALIGNMENT_BYTE，ALIGNMENT_WORD等段
    with open('MOD_COMMON.txt','r') as f:
        txt=f.read()
        f.close()
    l=[]
    m1=re.search('.*ALIGNMENT_BYTE\s*',txt)
    if m1!=None:
        l.append(txt[m1.end()])
        txt=txt[:m1.start()]+txt[m1.end()+2:]#如果有，先把它删掉...
    else:
        l.append('0')
    m2=re.search('.*ALIGNMENT_WORD\s*',txt)
    if m2!=None:
        l.append(txt[m2.end()])
        txt=txt[:m2.start()]+txt[m2.end()+2:]
    else:
        l.append('0')
    m3=re.search('.*ALIGNMENT_LONG\s*',txt)
    if m3!=None:
        l.append(txt[m3.end()])
        txt=txt[:m3.start()]+txt[m3.end()+2:]
    else:
        l.append('0')
    m4=re.search('.*ALIGNMENT_FLOAT32_IEEE\s*',txt)
    if m4!=None:
        l.append(txt[m4.end()])
        txt=txt[:m4.start()]+txt[m4.end()+2:]
    else:
        l.append('0')
    m5=re.search('.*ALIGNMENT_FLOAT64_IEEE\s*',txt)
    if m5!=None:
        l.append(txt[m5.end()])
        txt=txt[:m5.start()]+txt[m5.end()+2:]
    else:
        l.append('0')
    m6=re.search('.*ALIGNMENT_INT64\s*',txt)
    if m6!=None:
        l.append(txt[m6.end()])
        txt=txt[:m6.start()]+txt[m6.end()+2:]
    else:
        l.append('0')
    #print txt
    with open('MOD_COMMON.txt','w') as f:
        f.write(txt)
        f.close()
    return l

def check_error7():    #检查MAX_DLC_REQUIRED
    try:
        with open('XCP_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
        with open('XCP.txt','r') as f:
            txt=f.read()
            f.close()
    m=re.search('MAX_DLC_REQUIRED',txt)
    if m!=None:
        return 0
    else:
        return 1

def check_error8():  #检查ECU_CALIBRATION_OFFSET 0x50378BA0
    try:
        with open('MOD_PAR_new.txt','r')as f:
            txt=f.read()
            f.close()
    except:
        with open('MOD_PAR.txt','r')as f:
            txt=f.read()
            f.close()
    m=re.search('ECU_CALIBRATION_OFFSET 0x50378BA0',txt)
    if m!=None:
        return 0
    else:
        return 1



#---------------for check-------------------#












