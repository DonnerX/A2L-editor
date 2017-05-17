import re
def insert_mem(name,longidentifier,prgtype,memorytype,attribute,address,size,*arg):
    ins='\t/begin MEMORY_SEGMENT\n'+'\t  '+name+' '+'\"'+longidentifier+'\"'+' '+prgtype+' '+memorytype+' '+attribute+' '+address+' '+size+' '+'-1 -1 -1 -1 -1'
    for n in arg:
        ins=ins+' '+n
    ins=ins+'\n\t/end MEMORY_SEGMENT\n'
    #print ins
    try:
        with open('MOD_PAR_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
        with open('MOD_PAR.txt','r') as f:
            txt=f.read()
            f.close()
    m=re.search('/begin CALIBRATION_METHOD',txt)
    if m!=None:
        txt=txt[:m.start()]+ins+txt[m.start():]
    else:
        m=re.search('.*/end MOD_PAR',txt)
        txt=txt[:m.start()]+ins+txt[m.start():]
    with open('MOD_PAR_new.txt','w') as f:
        f.write(txt)
        f.close()
        
def getvalue_mem():
    try:
        with open('MOD_PAR_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
        with open('MOD_PAR.txt','r') as f:
            txt=f.read()
            f.close()
    valuelist=[]
    for m in re.finditer('/begin MEMORY_SEGMENT\s*',txt):
        txt2=re.split('\n',txt[m.end():])[0]
        #print txt2
        value=re.split('\s*',txt2)
        try:
            value.remove('')
        except:
            pass
        valuelist.append(value)
    return valuelist



def insert_memcode(name,longidentifier,prgtype,memorytype,attribute,address,size,*arg,**kw):
    ins=''
    if prgtype=='CODE':
        ins='\t/begin MEMORY_SEGMENT\n'+'\t  '+name+' '+'\"'+longidentifier+'\"'+' '+prgtype+' '+memorytype+' '+attribute+' '+address+' '+size+' '+'-1 -1 -1 -1 -1'\
             +'\n\t /begin IF_DATA XCP'+'\n\t  begin SEGMENT'
        if 'data1' in kw:
            ins=ins+'\n\t   %s'%kw['data1']
        else:
            ins=ins+'\n\t   0x01'
        if 'data2' in kw:
            ins=ins+'\n\t   %s'%kw['data2']
        else:
            ins=ins+'\n\t   0x01'
        if 'data3' in kw:
            ins=ins+'\n\t   %s'%kw['data3']
        else:
            ins=ins+'\n\t   0x00'
        if 'data4' in kw:
            ins=ins+'\n\t   %s'%kw['data4']
        else:
            ins=ins+'\n\t   0x00'
        if 'data5' in kw:
            ins=ins+'\n\t   %s'%kw['data5']
        else:
            ins=ins+'\n\t   0x00'
        ins=ins+'\n\t   /begin CHECKSUM'
        if 'str1' in kw:
            ins=ins+'\n\t   %s'%kw['str1']
        else:
            ins=ins+'\n\t    XCP_ADD_12'
        if 'str2' in kw:
            ins=ins+'\n\t   %s'%kw['str2']
        else:
            ins=ins+'\n\t    MAX_BLOCK_SIZE 0x010'
        ins=ins+'\n\t   /end CHECKSUM'+'\n\t   /begin PAGE'+'\n\t    0x00'
        if 'str3' in kw:
            ins=ins+'\n\t   %s'%kw['str3']
        else:
            ins=ins+'\n\t    ECU_ACCESS_WITH_XCP_ONLY'
        if 'str4' in kw:
            ins=ins+'\n\t   %s'%kw['str4']
        else:
            ins=ins+'\n\t    XCP_READ_ACCESS_WITH_ECU_ONLY'
        if 'str5' in kw:
            ins=ins+'\n\t   %s'%kw['str5']
        else:
            ins=ins+'\n\t    XCP_WRITE_ACCESS_NOT_ALLOWED'
        ins=ins+'\n\t   /end PAGE'+'\n\t  /end IF_DATA'
        ins=ins+'\n\t/end MEMORY_SEGMENT\n'
    if prgtype=='DATA':
        ins='\t/begin MEMORY_SEGMENT\n'+'\t '+name+' '+'\"'+longidentifier+'\"'+' '+prgtype+' '+memorytype+' '+attribute+' '+address+' '+size+' '+'-1 -1 -1 -1 -1'\
             +'\n\t /begin IF_DATA XCP'+'\n\t  /begin SEGMENT'
        if 'data1' in kw:
            ins=ins+'\n\t   %s'%kw['data1']
        else:
            ins=ins+'\n\t   0x01'
        if 'data2' in kw:
            ins=ins+'\n\t   %s'%kw['data2']
        else:
            ins=ins+'\n\t   0x02'
        if 'data3' in kw:
            ins=ins+'\n\t   %s'%kw['data3']
        else:
            ins=ins+'\n\t   0x00'
        if 'data4' in kw:
            ins=ins+'\n\t   %s'%kw['data4']
        else:
            ins=ins+'\n\t   0x00'
        if 'data5' in kw:
            ins=ins+'\n\t   %s'%kw['data5']
        else:
            ins=ins+'\n\t   0x00'
        ins=ins+'\n\t   /begin CHECKSUM'
        if 'str1' in kw:
            ins=ins+'\n\t   %s'%kw['str1']
        else:
            ins=ins+'\n\t    XCP_ADD_12'
        if 'str2' in kw:
            ins=ins+'\n\t   %s'%kw['str2']
        else:
            ins=ins+'\n\t    MAX_BLOCK_SIZE 0xB00'
        ins=ins+'\n\t   /end CHECKSUM'+'\n\t   /begin PAGE'+'\n\t    0x00'
        if 'str3' in kw:
            ins=ins+'\n\t   %s'%kw['str3']
        else:
            ins=ins+'\n\t    ECU_ACCESS_WITH_XCP_ONLY'
        if 'str4' in kw:
            ins=ins+'\n\t   %s'%kw['str4']
        else:
            ins=ins+'\n\t    XCP_READ_ACCESS_WITH_ECU_ONLY'
        if 'str5' in kw:
            ins=ins+'\n\t   %s'%kw['str5']
        else:
            ins=ins+'\n\t    XCP_WRITE_ACCESS_NOT_ALLOWED'
        ins=ins+'\n\t   /end PAGE'+'\n\t    /begin PAGE'+'\n\t    0x01'
        if 'str3' in kw:
            ins=ins+'\n\t   %s'%kw['str3']
        else:
            ins=ins+'\n\t    ECU_ACCESS_WITH_XCP_ONLY'
        if 'str4' in kw:
            ins=ins+'\n\t   %s'%kw['str4']
        else:
            ins=ins+'\n\t    XCP_READ_ACCESS_WITH_ECU_ONLY'
        if 'str5' in kw:
            ins=ins+'\n\t   %s'%kw['str5']
        else:
            ins=ins+'\n\t    XCP_WRITE_ACCESS_NOT_ALLOWED'
        ins=ins+'\n\t   /end PAGE'
        if 'ADD_MAP' in kw:
            ins=ins+'\n\t\t\t/begin ADDRESS_MAPPING'+'\n\t\t\t%s'%kw['ADD_MAP'][0]+'\n\t\t\t%s'%kw['ADD_MAP'][1]+'\n\t\t\t%s'%kw['ADD_MAP'][2]+'\n\t\t\t/end ADDRESS_MAPPING'
        ins=ins+'\n\t  /end SEGMENT'+'\n\t /end IF_DATA'+'\n\t/end MEMORY_SEGMENT\n'
    try:
        with open('MOD_PAR_new.txt','r') as f:
            txt=f.read()
            f.close()
    except:
        with open('MOD_PAR.txt','r') as f:
            txt=f.read()
            f.close()
    m=re.search('/begin CALIBRATION_METHOD',txt)
    if m!=None:
        txt=txt[:m.start()]+ins+txt[m.start():]
    else:
        m=re.search('.*/end MOD_PAR',txt)
        txt=txt[:m.start()]+ins+txt[m.start():]
    print txt
    with open('MOD_PAR_new.txt','w') as f:
        f.write(txt)
        f.close()

#insert_memcode('CALRAM','','DATA','RAM','INTERN','0x80240000','0x40000',ADD_MAP=['ABCC','ABC','ABC'])
        
















    
