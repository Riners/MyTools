#!/home/tops/bin/python
#coding=utf-8
import commands
import json
import sys
vpcregiondb_commands = "curl -s localhost:7070/api/v3/column/service.res.result | grep -C 1 vpcregiondb"
vpcregiondb_json = json.loads(commands.getoutput(vpcregiondb_commands)[:-1].replace('\\\"', '\"').replace('\"{', '{').replace('}\"', '}'))["service.res.result"]
vpcregiondb_info = "mysql -h{host} -u{user} -p{pwd} -D{db} -P{port}".format( host=vpcregiondb_json["db_host"], pwd=vpcregiondb_json["db_password"], user=vpcregiondb_json["db_user"], db=vpcregiondb_json["db_name"], port=vpcregiondb_json["db_port"] )
choke_task_count_commands = vpcregiondb_info + ' -e \"select count(*) from request_token where status = \'processing\';\" 2>/dev/null | sed -n \'1!p\''
choke_task_count = commands.getoutput(choke_task_count_commands)

choke_task_commands = vpcregiondb_info + ' -e \"select gmt_create,count(*),action_name,asyn_token from request_token where status = \'processing\' group by action_name;\" 2>/dev/null | sed -n \'1!p\''
choke_task = commands.getoutput(choke_task_commands)
if choke_task == "":
	print "！！！-----当前环境vpc管控没有阻塞任务，请查找其他原因-----！！！"
	sys.exit()
else :
	print "{} {}".format('阻塞任务总数:',choke_task_count)
	print "{:33s}{:30s}{:45s}{:40s}".format('阻塞任务发生最早时间','阻塞任务统计','阻塞任务action_name','阻塞任务asyn_token')
	for choke_task_line in choke_task.split('\n'):
		print "{:11s}{:17s}{:10s}{:40}{:40s}".format(choke_task_line.split()[0],choke_task_line.split()[1],choke_task_line.split()[2],choke_task_line.split()[3],choke_task_line.split()[4])
