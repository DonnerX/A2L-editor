import re

def fix_error1():   # lack of MEMORY_SEGMENT
    l=[]
    with open('MOD_PAR.txt','r') as f:
        txt=f.read()
        f.close()
    m=re.search(r'\n.*/end MOD_PAR',txt)
    txt=txt[:m.start()]+'\n\t/begin MEMORY_SEGMENT'+'\n\t    cal_data "CAL_Data" DATA \
 FLASH INTERN 0x80000000  0x00010000  -1 -1 -1 -1 -1'+'\n\t/end MEMORY_SEGMENT'\
        +txt[m.start():]
    #print txt

    with open('MOD_PAR_new.txt','w') as f:
        f.write(txt)
        f.close()
    print 'finish fix error1'

def fix_error2():    #fix Optional
    with open('XCP.txt','r') as f:
        txt=f.read()
        f.close()

    ms=re.finditer(r'OPTIONAL_CMD 0x[\d\w]+',txt)
    md=re.search(r'/end TP_BLOB',txt)
    s=ms.next().start()
    e=md.start()
    txt=txt[:s]+'''  OPTIONAL_CMD 0xF 
            OPTIONAL_CMD 0x23 
            OPTIONAL_CMD 0xE 
            OPTIONAL_CMD 0x8 
            OPTIONAL_CMD 0x22 
            OPTIONAL_CMD 0x5 
            OPTIONAL_CMD 0x11
            OPTIONAL_CMD 0x19
            OPTIONAL_CMD 0xC
            OPTIONAL_CMD 0xD'''+'\n'+'\t'+txt[e:]
    #print txt

    with open('XCP_new.txt','w') as f:
        f.write(txt)
        f.close()
    print 'finish fix error2'



def fix_error3():    #replace DAQ_RESUME_SUPPORTED with RESUME_SUPPORTED
    with open('A2ML.txt','r')as f:
        txt=f.read()
        f.close()
    l=re.findall('DAQ_RESUME_SUPPORTED',txt)
    for i in l:
        txt=txt.replace('DAQ_RESUME_SUPPORTED','RESUME_SUPPORTED')
    with open('A2ML_new.txt','w')as f:
        f.write(txt)
        f.close()
    print 'finish fix error3'
    
def fix_error4(c):
    print 'fixing error4'
    l=[]
    with open('REST.txt','r')as f:
        txt=f.read()
        f.close()
    l=txt.split('\n')
    #print 'error4 exist:'
    for p in c:
        print l[p]
        l[p]=l[p]+'"'
    txt='\n'.join(l)
    with open('REST_new.txt','w') as f:
        f.write(txt)
        f.close()
    print 'finish fix error4'

def fix_error5():  #FIXED_EVENT_LIST
    print 'fixing error5'
    with open('CHARACTERISTIC.txt','r') as f:
        txt=f.read()
        f.close()
    m=re.search('FIXED_EVENT_LIST',txt)
    while m!=None:
        for ms in re.finditer('/begin IF_DATA XCP',txt):
            if ms.end()<m.start():
                s=ms.start()
        for me in re.finditer('/end IF_DATA',txt):
            if me.start()>m.end():
                e=me.end()
                break
        #print s,e
        txt=txt[:s]+txt[e:]
        m=re.search('FIXED_EVENT_LIST',txt)
    with open('CHARACTERISTIC_new.txt','w') as f:
        f.write(txt)
        f.close()
    print 'finish fix error5'

def fix_error5_2():
    try:
        with open('REST_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
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
    #print len(s2)          
    for i in range(-len(s2)+1,1,1):
        #print txt[s2[i]:e2[i]]
        txt=txt[:s2[i]]+txt[e2[i]:]    
    with open('REST_new.txt','w') as f:
        f.write(txt)
        f.close()
    print 'finish fix error5'
    
def fix_error6to_1(l):
    with open('MOD_COMMON.txt','r') as f:
        txt=f.read()
        f.close()
    txt2='      ALIGNMENT_BYTE 1\n      ALIGNMENT_WORD 1\n      ALIGNMENT_LONG 1\n      ALIGNMENT_FLOAT32_IEEE 1\n      ALIGNMENT_FLOAT64_IEEE 1\n      ALIGNMENT_INT64 1'
    if l[0]=='0':
        txt2='      ALIGNMENT_BYTE 1'
    '''else:
        txt2='      ALIGNMENT_BYTE %s'%l[0]
    if l[1]=='0':
        txt2=txt2+'\n      ALIGNMENT_WORD 1'
    else:
        txt2=txt2+'\n      ALIGNMENT_WORD %s'%l[1]
    if l[2]=='0':
        txt2=txt2+'\n      ALIGNMENT_LONG 1'
    else:
        txt2=txt2+'\n      ALIGNMENT_LONG %s'%l[2]
    if l[3]=='0':
        txt2=txt2+'\n      ALIGNMENT_FLOAT32_IEEE 1'
    else:
        txt2=txt2+'\n      ALIGNMENT_FLOAT32_IEEE %s'%l[3]
    if l[4]=='0':
        txt2=txt2+'\n      ALIGNMENT_FLOAT64_IEEE 1'
    else:
        txt2=txt2+'\n      ALIGNMENT_FLOAT64_IEEE %s'%l[4]
    if l[5]==0:
        txt2=txt2+'\n      ALIGNMENT_INT64 1'
    else:
        txt2=txt2+'\n      ALIGNMENT_INT64 %s'%l[5]'''
    #print txt2
    m=re.match('\s*/begin MOD_COMMON\s*".*".*\n',txt)
    txt=txt[:m.end()]+txt2+'\n'+txt[m.end():]
    with open('MOD_COMMON.txt','w') as f:
        f.write(txt)
        f.close()

def restore_error6(l):
    with open('MOD_COMMON.txt','r') as f:
        txt=f.read()
        f.close()
    txt2=''
    if l[0]!='0':
        txt2='      ALIGNMENT_BYTE %s\n'%l[0]
    if l[1]!='0':
        txt2=txt2+'      ALIGNMENT_WORD %s\n'%l[1]
    if l[2]!='0':
        txt2=txt2+'      ALIGNMENT_LONG %s\n'%l[2]
    if l[3]!='0':
        txt2=txt2+'      ALIGNMENT_FLOAT32_IEEE %s\n'%l[3]
    if l[4]!='0':
        txt2=txt2+'      ALIGNMENT_FLOAT64_IEEE %s\n'%l[4]
    if l[5]!='0':
        txt2=txt2+'      ALIGNMENT_INT64 %s\n'%l[5]
    #print txt2
    m=re.match('\s*/begin MOD_COMMON\s*".*".*\n',txt)
    txt=txt[:m.end()]+txt2+txt[m.end():]
    with open('MOD_COMMON.txt','w') as f:
        f.write(txt)
        f.close()

def fix_error7():
    try:
        with open('XCP_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
        with open('XCP.txt','r') as f:
            txt=f.read()
            f.close()
    m2=re.search('.*DAQ_LIST_CAN_ID',txt)
    if m2!=None:
        txt=txt[:m2.start()]+'            "MAX_DLC_REQUIRED" ;\n'+txt[m2.start():]
    else:
        m3=re.search('.*/end XCP_ON_CAN',txt)
        txt=txt[:m3.start()]+'            "MAX_DLC_REQUIRED" ;\n'+txt[m3.start():]
    with open('XCP_new.txt','w') as f:
        f.write(txt)
        f.close()

def fix_error8():                #ECU_CALIBRATION_OFFSET 0x50378BA0
    try:
        with open('MOD_PAR_new.txt','r')as f:
            txt=f.read()
            f.close()
    except:
        with open('MOD_PAR.txt','r')as f:
            txt=f.read()
            f.close()
    m=re.search('/begin MOD_PAR.*',txt)
    txt=txt[:m.end()]+'\n	ECU_CALIBRATION_OFFSET 0x50378BA0'+txt[m.end():]
    with open('MOD_PAR_new.txt','w')as f:
        f.write(txt)
        f.close











    
