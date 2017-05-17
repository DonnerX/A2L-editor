import Division_fun_and_merge as div
import Check as check
import Fix as fix
import Insert_and_getvalue as ig

fil_name='Test_Fixed_Event_CATL_OK'
fil_newname=fil_name+'_new'
div.division(fil_name+'.a2l')

print '\nchecking error.....'
e1=check.check_error1()
print 'error1(Mem seg)=',e1
e2=check.check_error2()
print 'error2(optional)=',e2
e3=check.check_error3()
print 'error3(DAQ_RESUME)=',e3
e4=check.check_error4()
print 'error4(lack of ")=',e4[0]
e5=check.check_error5_2()
print 'error5(fixed_event_list)=',e5
e6=check.check_error6()
print 'error6(ALIGNMENT)=',e6
e7=check.check_error7()
print 'error7(MAX_DLC_REQUIRED)=',e7
e8=check.check_error8()
print 'error8(ECU_CALIBRATION_OFFSET 0x50378BA0)=',e8

choose=0
print '\nfixing...'
if e1==1:
    fix.fix_error1()
if e2==1:
    fix.fix_error2()  
if e3==1:
    fix.fix_error3()
if e4[0]==1:
    fix.fix_error4(e4[1])
if e5==1:
    fix.fix_error5_2()
if choose==1:
    fix.fix_error6to_1(e6)
else:
    fix.restore_error6(e6)
if e7==1:
    fix.fix_error7()
if e8==1:
    fix.fix_error8()
    
div.creat('HEAD.txt',fil_newname+'.a2l')

try:
    div.merge('A2ML_new.txt',fil_newname+'.a2l')
except:
    div.merge('A2ML.txt',fil_newname+'.a2l')
try:
    div.merge('MOD_COMMON.txt',fil_newname+'.a2l')
except:
    div.merge('MOD_COMMON_new.txt',fil_newname+'.a2l')

try:
    div.merge('MOD_PAR_new.txt',fil_newname+'.a2l')
except:
    div.merge('MOD_PAR.txt',fil_newname+'.a2l')
    
try:
    div.merge('XCP_new.txt',fil_newname+'.a2l')
except:
    div.merge('XCP.txt',fil_newname+'.a2l')
    
try:
    div.merge('CNP.txt',fil_newname+'.a2l')
except:
    pass

try:
    div.merge('REST_new.txt',fil_newname+'.a2l')
except:
    div.merge('REST.txt',fil_newname+'.a2l')
'''
try:
    div.merge('CHARACTERISTIC_new.txt',fil_newname+'.a2l')
except:
    div.merge('CHARACTERISTIC.txt',fil_newname+'.a2l')

div.merge('MEASUREMENT.txt',fil_newname+'.a2l')
print 'merged'

v=ig.getvalue_mem()
for i in v:
    print i
'''





