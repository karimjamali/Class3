from snmp_helper import snmp_get_oid_v3
from snmp_helper import snmp_extract
import time
import pygal
import smtplib
import pickle



def SNMP_Extract_Data(dev,user,oid):        
    snmp_data = snmp_get_oid_v3(dev,user, oid)
    result=snmp_extract(snmp_data)
    return result
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def Save_Output_to_File(output, filename):
    with open(filename,'a') as f:
        f.write('\n\n')
        f.write(output)

def main():

    ip_addr='184.105.247.71'
    port=161
    user="pysnmp"
    auth_key="galileo1"
    encr_key="galileo1"

    oid='1.3.6.1.2.1.1.1.0'
    oids=( 
    ('sysUptime', '1.3.6.1.2.1.1.3.0', True), 
    ('ccmHistoryRunningLastChanged', '1.3.6.1.4.1.9.9.43.1.1.1.0', True), 
    ('ccmHistoryRunningLastSaved ', '1.3.6.1.4.1.9.9.43.1.1.2.0', True), 
    ('ccmHistoryStartupLastChanged', '1.3.6.1.4.1.9.9.43.1.1.3.0', True), 
)

    pynet_rtr1=(ip_addr,port)
    a_user=(user,auth_key,encr_key)
    sys_descr = '1.3.6.1.2.1.1.1.0'
    output=''
    fifteen_min=[0,20,40,60]
    var=20
    for t in fifteen_min:
        my_result_list=[]
        output+='\n Time  {}'.format(t) + 'seconds  \n' 
        for descr,a_oid,is_count in oids:
           
            result=SNMP_Extract_Data(pynet_rtr1,a_user,oid=a_oid)
            my_result_list.append(result)
            output+=result + '\n'
        
        output+='\n\n'  
        
        if t == 0:
            with open('my_previous_run.pkl','w') as f:
                pickle.dump(my_result_list,f)
                f.close()
        else:
            with open('my_previous_run.pkl','r') as f:
                old_result=pickle.load(f)
                f.close() 
                
                if int(my_result_list[0]) > int(old_result[0]):
                    if my_result_list[1] > old_result[1]:
                      sendemail(from_addr='karim.jamali@gmail.com',
                        to_addr_list = ['karim.jamali@gmail.com'],
                        cc_addr_list = ['karim.jamali@gmail.com'],
                        subject      = 'Running_Configuration_Changed',
                        message      = 'Running_Configuration_Changed',
                        login        = 'ahc',
                        password     = 'def')
                if int(my_result_list[3]) > int(old_result[3]):
                      sendemail(from_addr='karim.jamali@gmail.com',
                        to_addr_list = ['karim.jamali@gmail.com'],
                        cc_addr_list = ['karim.jamali@gmail.com'],
                        subject      = 'Startup_Configuration_Changed',
                        message      = 'Startup_Configuration_Changed',
                        login        = 'ahc',
                        password     = 'def')
                if int(my_result_list[0]) < int(old_result[0]):
                      sendemail(from_addr='karim.jamali@gmail.com',
                        to_addr_list = ['karim.jamali@gmail.com'],
                        cc_addr_list = ['karim.jamali@gmail.com'],
                        subject      = 'Router_Reloaded',
                        message      = 'Router_Reloaded',
                        login        = 'ahc',
                        password     = 'def')
            with open('my_previous_run.pkl','w') as f: 
                    pickle.dump(my_result_list,f)         
                    f.close() 
        time.sleep(var) 
                
        
    print output
    

if __name__ =='__main__':
    main()
