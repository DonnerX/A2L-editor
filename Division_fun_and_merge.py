#/usr/bin/python
#该模块用于将a2l文件划分为几个小块，分别存入txt中方便后续操作

import re  #导入re模块


def get_p(l,r):  #输入为一个list:l，和一个字符串:r 。 l中按行存储着文件内容，r为需要匹配的内容。
    for p in range(len(l)):
        if re.match(r,l[p])!=None:
            #循环操作，逐行查找文件中是否有匹配r的内容，如果有就将这行的行数赋予P_point，结束循环
            p_point=p
            #print 'get start'
            break
    return p_point #返回r内容所在的行数

def write_accord_p(l,p_start,p_end,str_name):
    #创建一个新的文件，文件名为str_name,将l中从第p_start到p_end的内容写入文件
    with open(str_name,'w') as f:
        for p in range(p_start,p_end+1):
            f.writelines(l[p])
        f.close()

def merge(text_name,new_name):#将text_name文件中的内容添加到new_name文件的后面
    with open(text_name,'r')as f:
        txt=f.read()
        f.close()
    txt=txt+'\n\n'
    with open(new_name,'a')as f:
        f.write(txt)
        f.close()
        
def creat(text_name,new_name): #创建new_name文件，内容为text_name中的内容
    with open(text_name,'r')as f:
        txt=f.read()
        f.close()
    txt=txt+'\n\n'
    with open(new_name,'w')as f:
        f.write(txt)
        f.close()

def division(name): #将a2l文件划分为几个部分
    l=[]
    with open(name,'r') as f: #逐行读入name文件中的内容，保存在l中
        for s in f.readlines():
            l.append(s)
        f.close()
        print "get the text"
#------------get A2ML and init---------------------#
    try: #尝试寻找A2ML段和HEAD段，并写入HEAD.txt和A2ML.txt中
        p_a2start=get_p(l,r'    /begin A2ML')
        p_a2end=get_p(l,r'    /end A2ML')
        print 'A2ML_start=',p_a2start,'A2ML_end=',p_a2end

        write_accord_p(l,0,p_a2start-1,'HEAD.txt')
        write_accord_p(l,p_a2start,p_a2end,'A2ML.txt')
        del l[0:p_a2end+1] #删除已经写入的部分
        #print l[0:100]
    except: #当中发生错误，则认为A2ML段不存在
        print "A2ML do not exist"
#-------------get MOD_PAR-----------------------------#
    try:#尝试寻找MOD_PAR段，写入MOD_PAR.txt，同时删除已经写入的部分
        p_mparstart=get_p(l,r'    /begin MOD_PAR ')
        p_mparend=get_p(l,r'    /end MOD_PAR')
        print 'MOD PAR_start=',p_mparstart,'MOD PAR_end=',p_mparend

        write_accord_p(l,p_mparstart,p_mparend,'MOD_PAR.txt')
        del l[p_mparstart:p_mparend+1]
    except:#如果发生错误，则认为MOD_PAR段不存在
        print 'MOD_PAR do not exist'
#-----------------get MOD_COMMON-----------------------#
    try:#尝试寻找MOD_COMMON段，写入MOD_COMMON.txt，同时删除已经写入的部分
        p_mcomstart=get_p(l,r'    /begin MOD_COMMON ""')
        p_mcomend=get_p(l,r'    /end MOD_COMMON')
        print 'MOD_COMMON_start=',p_mcomstart,'MOD_COMMON_end=',p_mcomend

        write_accord_p(l,p_mcomstart,p_mcomend,'MOD_COMMON.txt')
        del l[p_mcomstart:p_mcomend+1]
    except:#如果发生错误，则认为MOD_COMMON段不存在
        print 'MOD_COMMON do not exist'
#------------------get IF_DATA XCP----------------------#
    for p in range(len(l)):#寻找XCP的定义段，存入XCP.txt，并删除写入部分
        if (re.match(r'\s*/begin IF_DATA .*[CX]CP',l[p])!=None):#&\
           #(~((p>p_a2start)&(p<p_a2end)))& (~((p>p_mparstart)&(p<p_mparend)))&\
           #(~((p>p_mcomstart)&(p<p_mcomend))):
            print 'XCP_start=',p
            p_xcps=p #先找到XCP段开始部分，赋值给p_xcps，然后跳出循环
            #print 'get start'
            break
    m=re.search(r'/',l[p_xcps]) #匹配/begin IF_DATA .*[CX]CP中‘/’在该行中的位置
    numplace=m.start()#‘/’的序号即前面有几个空格

    l2=l[p_xcps:] #取p_xcps后面的内容
    for p in range(len(l2)): #寻找XCP段的结尾
        if re.match(r'\s{%d}/end IF_DATA'%numplace,l2[p])!=None:
            #因为XCP中也可能存在IF_DATA，因此需要对前面的空格也进行匹配。
            print 'XCP_end=',p,'(relative)'
            p_xcpe=p #获得结尾的相对位置，赋予p_xcpe，结束循环
            break
    l_xcp=l2[0:p_xcpe+1] #取出XCP内容
    #print l_xcp

    with open('XCP.txt','w')as f: #写入XCP.txt
        for s in l_xcp:
            f.writelines(s)
        f.close()
    del l[p_xcps:p_xcps+p_xcpe+1] #删除写入部分
#------------get IF_DATA CNP_CREATE_INI------------#
    try: #同样的道理，找到CNP段，写入CNP.txt，删除写入部分
        for p in range(len(l)):
            if (re.match(r'\s*/begin IF_DATA CNP_CREATE_INI',l[p])!=None)&\
               (re.match(r'\s*\n',l[p-1])!=None):
                print 'find CNP_CREATE_INI,p_start=',p
                p_cnps=p
                #print 'get start'
                break
        m=re.search(r'/',l[p_cnps])
        numplace=m.start()

        l2=l[p_cnps:]
        for p in range(len(l2)):
            if re.match(r'\s{%d}/end IF_DATA'%numplace,l2[p])!=None:
                print 'CNP_end=',p,'(relative)'
                p_cnpe=p
                break
        l_cnp=l2[0:p_cnpe+1]

        with open('CNP.txt','w')as f:
            for s in l_cnp:
                f.writelines(s)
            f.close()
        del l[p_cnps:p_cnpe+1]
    except:
        print 'IF_DATA CNP_CREATE_INI do not exist'

#-----------------------get REST--------------------#
    write_accord_p(l,0,len(l)-1,'REST.txt') #将剩余部分写入REST.txt
#------------------get CHARACTERISTIC-----------------#
'''    l=[]
    txtch=''
    ms=[]
    me=[]
    with open('REST.txt','r')as f:
            txt=f.read()
            f.close()
    for m in re.finditer('.*/begin CHARACTERISTIC',txt):
        ms.append(m.start())
    for m in re.finditer('.*/end CHARACTERISTIC.*\n',txt):
        me.append(m.end())
    print 'preparing for CHARACTERISTIC.txt'
    for i in range(len(ms)):
        txtch=txtch+txt[ms[i]:me[i]]+'\n'
    with open('CHARACTERISTIC.txt','w')as f:
        f.write(txtch)
        f.close()
    ms.reverse()
    me.reverse()
    print 'preparing for MEASUREMENT.txt'
    for i in range(len(ms)):
        txt=txt[:ms[i]]+txt[me[i]:]
    with open('MEASUREMENT.txt','w')as f:
        f.write(txt)
        f.close()
'''
#------------------get MEASURMENT--------------------#
#--------------for test--------------------#
#division('Test.a2l')














