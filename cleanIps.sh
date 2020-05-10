#!/bin/bash
# clean Ips of iptables and Security Group AWS
# by Rafeal Klock

IPS_LIST_AWS=$(/sbin/iptables -nL|grep portknocker|sort|uniq|awk '{print $4}')
for ip in $(echo $IPS_LIST_AWS); do
  /opt/api/cleanIpSecurityGroupAws.py ${ip}/32
done

IPS_LIST=$(/sbin/iptables -nL|grep portknocker|awk '{print $4}')
for ip in $(echo $IPS_LIST); do
  /sbin/iptables -D INPUT -s ${ip} -m comment --comment "Liberado pelo portknocker" -j ACCEPT
  /sbin/iptables -D INPUT -s ${ip} -m comment --comment "Liberado pelo portknocker" -j ACCEPT
done
