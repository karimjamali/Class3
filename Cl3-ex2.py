from snmp_helper import snmp_get_oid_v3
from snmp_helper import snmp_extract
import time
import pygal
import smtplib

def Differential_Array(a):
    diff_array=[]
    for i in range (len(a)):
        if i ==0:
            continue
        else:
            temp = int (a[i]) - int(a[i-1])
            diff_array.append(temp)
    return diff_array

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

    ip_addr='184.105.247.70'
    port=161
    user="pysnmp"
    auth_key="galileo1"
    encr_key="galileo1"

    oid='1.3.6.1.2.1.1.1.0'
    oids=(
    ('sysName', '1.3.6.1.2.1.1.5.0', None), 
    ('sysUptime', '1.3.6.1.2.1.1.3.0', None), 
    ('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5', None), 
    ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5', True), 
    ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5', True), 
    ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5', True), 
    ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5', True)
)

    pynet_rtr1=(ip_addr,port)
    a_user=(user,auth_key,encr_key)
    sys_descr = '1.3.6.1.2.1.1.1.0'
    InOctets_Array=[]
    OutOctets_Array=[]
    InUcastPkts_Array=[]
    OutUcastPkts_Array=[]
    output=''
    five_min=[0,300,600,900,1200,1500,1800,2100,2400,2700,3000,3300,3600]
    var=300
    for t in five_min:
        output+='\n Time  {}'.format(t) + 'seconds  \n' 
        for descr,a_oid,is_count in oids:
           # snmp_data = snmp_get_oid_v3(pynet_rtr1, a_user, oid=a_oid)
           # result=snmp_extract(snmp_data)
            result=SNMP_Extract_Data(pynet_rtr1,a_user,oid=a_oid)
            if "InOct" in descr:
                InOctets_Array.append(result)
            if "OutOct" in descr:
                OutOctets_Array.append(result)
            if "InUcast" in descr:
                InUcastPkts_Array.append(result)
            if "OutUcast" in descr:
                OutUcastPkts_Array.append(result)
            output+= descr + ': '+  result + '\n' 
       # output+='\n Time is {}'.format(t) + '\n\n'
        output+='\n'
        time.sleep(var)
    print output
    
    
   # print InOctets_Array,OutOctets_Array,InUcastPkts_Array,OutUcastPkts_Array
    #print OutOctets_Array
    #print InUcastPkts_Array
    #print OutUcastPkts_Array
    
    InOctets_diff=Differential_Array(InOctets_Array)
    OutOctets_diff=Differential_Array(OutOctets_Array)
    InUcastPkts_diff=Differential_Array(InUcastPkts_Array)
    OutUcastPkts_diff=Differential_Array(OutUcastPkts_Array)
    Save_Output_to_File(output,'NEW_SNMP_v4.txt')
#    print type(descr),type(result)
       # output+=descr,result
        #print result   
    #output+= descr,result
        
   # print output
    #Save_Output_to_File(output,'SNMP_v3.txt')
    print InOctets_diff,OutOctets_diff,InUcastPkts_diff,OutUcastPkts_diff
    
    Packets_chart=pygal.Line()
    Packets_chart.title='Input/Output Packets'
    Packets_chart.x_labels=['5','10','15','20','25','30','35','40','45','50','55','60']
    
    Packets_chart.add('InUcastPkts', InUcastPkts_diff)
    Packets_chart.add('OutUcastPkts', OutUcastPkts_diff)

    Packets_chart.render_to_file('Fa4_Packets.svg')

    Octets_chart=pygal.Line()
    Octets_chart.title='Input/Output Bytes'
    Octets_chart.add('InOctets', InOctets_diff)
    Octets_chart.add('OutOctets', OutOctets_diff)
    
    Octets_chart.render_to_file('Fa4_Octets.svg')



if __name__ =='__main__':
    main()

