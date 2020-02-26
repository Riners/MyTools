#!/home/tops/bin/python
#coding=utf-8
import os
import commands
import json
import sys

vpcregiondb_commands = "curl -s localhost:7070/api/v3/column/service.res.result | grep -C 1 vpcregiondb"
vpcregiondb_json = json.loads(commands.getoutput(vpcregiondb_commands)[:-1].replace('\\\"', '\"').replace('\"{', '{').replace('}\"', '}'))["service.res.result"]
vpcregiondb_info = "mysql -h{host} -u{user} -p{pwd} -D{db} -P{port}".format( host=vpcregiondb_json["db_host"], pwd=vpcregiondb_json["db_password"], user=vpcregiondb_json["db_user"], db=vpcregiondb_json["db_name"], port=vpcregiondb_json["db_port"] )
print "请输入阻塞任务的asyn_token信息："
asyn_token_id = raw_input()
action_name_commands = vpcregiondb_info + ' -e \"select action_name from request_token where asyn_token = \'' + asyn_token_id + '\';\" 2>/dev/null | sed -n \'1!p\''
action_name = commands.getoutput(action_name_commands)
if action_name == "":
	print "！！！-----asyn_token输入错误请重新输入-----！！！"
	sys.exit()
print "任务名：" + action_name
print "----------------------------------------------------------publish_task区----------------------------------------------------------"
publish_task_info_commands = vpcregiondb_info + ' -e \"select id,gmt_create,status,relation_type,relation_key,operation,has_repeated_times from publish_task where asyn_token = \'' + asyn_token_id + '\';\" 2>/dev/null | sed -n \'1!p\''
publish_task_info = commands.getoutput(publish_task_info_commands)
if publish_task_info != "":
	print "publish_task:"
	print "{:4s}{:12s}{:15s}{:7s}{:20s}{:21s}{:10s}{:18s}".format('','id','gmt_create','status','relation_type','relation_key','operation','has_repeated_times')
	for publish_task_info_line in publish_task_info.split('\n'):
		print "{:11s}{:11s}{:12s}{:9s}{:9s}{:32s}{:12s}{:20s}".format(publish_task_info_line.split()[0],publish_task_info_line.split()[1],publish_task_info_line.split()[2],publish_task_info_line.split()[3],publish_task_info_line.split()[4],publish_task_info_line.split()[5],publish_task_info_line.split()[6],publish_task_info_line.split()[7])
publish_task_id_all_commands = vpcregiondb_info + ' -e \"select id from publish_task where asyn_token = \'' + asyn_token_id + '\'\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
publish_task_id_all = commands.getoutput(publish_task_id_all_commands)
publish_task_id = ','.join(publish_task_id_all.split())
gateway_task_publish_task_id_all_commands = vpcregiondb_info + ' -e \"select id from publish_task where relation_type = 1 and id in (' + publish_task_id + ')\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
gateway_task_publish_task_id_all = commands.getoutput(gateway_task_publish_task_id_all_commands)
gateway_task_publish_task_id = ','.join(gateway_task_publish_task_id_all.split())
mvss_task_publish_task_id_all_commands = vpcregiondb_info + ' -e \"select id from publish_task where relation_type = 2 and id in (' + publish_task_id + ')\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
mvss_task_publish_task_id_all = commands.getoutput(mvss_task_publish_task_id_all_commands)
mvss_task_publish_task_id = ','.join(mvss_task_publish_task_id_all.split())
mvss_task_publish_task_relation_key_all_commands = vpcregiondb_info + ' -e \"select relation_key from publish_task where id in (' + mvss_task_publish_task_id + ')\\G\" 2>/dev/null | grep relation_key | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
mvss_task_publish_task_relation_key_all = commands.getoutput(mvss_task_publish_task_relation_key_all_commands)
mvss_task_publish_task_relation_key = ','.join(mvss_task_publish_task_relation_key_all.split())
if gateway_task_publish_task_id != "":
	print "----------------------------------------------------------gateway_task区----------------------------------------------------------"
	gateway_task_id_all_commands = vpcregiondb_info + ' -e \"select id from gateway_task where publish_task_id in (' + gateway_task_publish_task_id + ')\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	gateway_task_id_all = commands.getoutput(gateway_task_id_all_commands)
	gateway_task_id = ','.join(gateway_task_id_all.split())
	if gateway_task_id != "":
		print "gateway_task:"
		print "{:4s}{:12s}{:15s}{:7s}{:14s}{:13s}".format('','id','gmt_create','status','relation_type','relation_key')
		for gateway_task_publish_task_id_1 in gateway_task_publish_task_id_all.split():
			gateway_task_info_1_commands = vpcregiondb_info + ' -e \"select id,gmt_create,status,relation_type,relation_key from gateway_task where publish_task_id = \'' + 	gateway_task_publish_task_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
			gateway_task_info_1 = commands.getoutput(gateway_task_info_1_commands)
			for gateway_task_info_line in gateway_task_info_1.split('\n'):
				print "{:11s}{:11s}{:12s}{:9s}{:11s}{:32s}".format(gateway_task_info_line.split()[0],gateway_task_info_line.split()[1],gateway_task_info_line.split()[2],gateway_task_info_line.split()[3],gateway_task_info_line.split()[4],gateway_task_info_line.split()[5])
			gateway_task_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from gateway_task where publish_task_id = \'' + gateway_task_publish_task_id_1 + '\'\\G\" 2>/dev/null | grep relation_key | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
			gateway_task_relation_key_1 = commands.getoutput(gateway_task_relation_key_1_commands)
			gateway_task_gmt_create_1_commands = vpcregiondb_info + ' -e \"select gmt_create from gateway_task where publish_task_id = \'' + gateway_task_publish_task_id_1 + '\'\\G\" 2>/dev/null | grep gmt_create | awk  -F \': \' \'{printf($2)}\''
			gateway_task_gmt_create_1 = commands.getoutput(gateway_task_gmt_create_1_commands)
			gw_oplog_id_1_commands = vpcregiondb_info + ' -e \"select id from gw_oplog where relation_key = \'' + gateway_task_relation_key_1 + '\' and gmt_create like \'%' + gateway_task_gmt_create_1 + '%\';\" 2>/dev/null | sed -n \'1!p\''
			gw_oplog_id_1 = commands.getoutput(gw_oplog_id_1_commands)
		if gw_oplog_id_1 != "":
			print '\n' + "阻塞任务未过期"
			print "gw_oplog:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:8s}{:40s}".format('','id','gmt_create','relation_type','relation_key','version','operation')
			for gateway_task_id_1 in gateway_task_id_all.split():
				gateway_task_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep relation_key | awk  -F \': \' \'{printf($2)}\''
				gateway_task_relation_key_1 = commands.getoutput(gateway_task_relation_key_1_commands)
				gateway_task_gmt_create_1_commands = vpcregiondb_info + ' -e \"select gmt_create from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep gmt_create | awk  -F \': \' \'{printf($2)}\''
				gateway_task_gmt_create_1 = commands.getoutput(gateway_task_gmt_create_1_commands)
				gw_oplog_info_1_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,relation_key,version,operation from gw_oplog where relation_key = \'' + gateway_task_relation_key_1 + '\' and gmt_create like \'%' + gateway_task_gmt_create_1 + '%\';\" 2>/dev/null | sed -n \'1!p\''
				gw_oplog_info_1 = commands.getoutput(gw_oplog_info_1_commands)
				for gw_oplog_info_line in gw_oplog_info_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:13s}{:10s}{:6s}".format(gw_oplog_info_line.split()[0],gw_oplog_info_line.split()[1],gw_oplog_info_line.split()[2],	gw_oplog_info_line.split()[3],gw_oplog_info_line.split()[4],gw_oplog_info_line.split()[5],gw_oplog_info_line.split()[6])
			print '\n' + "gw_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:8s}".format('','id','gmt_modify','relation_type','relation_key','version')
			for gateway_task_id_1 in gateway_task_id_all.split():
				gateway_task_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep relation_key | awk  -F \': \' \'{printf($2)}\''
				gateway_task_relation_key_1 = commands.getoutput(gateway_task_relation_key_1_commands)
				gw_oplog_gw_key_version_1_commands = vpcregiondb_info + ' -e \"select id,gmt_modify,relation_type,relation_key,version from gw_key_version where relation_key = \'' + gateway_task_relation_key_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				gw_oplog_gw_key_version_1 = commands.getoutput(gw_oplog_gw_key_version_1_commands)
				for gw_oplog_gw_key_version_line in gw_oplog_gw_key_version_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:13s}{:9s}".format(gw_oplog_gw_key_version_line.split()[0],gw_oplog_gw_key_version_line.split()[1],gw_oplog_gw_key_version_line.split()[2],gw_oplog_gw_key_version_line.split()[3],gw_oplog_gw_key_version_line.split()[4],gw_oplog_gw_key_version_line.split()[5])
		else :
			print '\n' + "阻塞任务已过期"
			print "gw_oplog_history:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:8s}{:40s}".format('','id','gmt_create','relation_type','relation_key','version','operation')
			for gateway_task_id_1 in gateway_task_id_all.split():
				gateway_task_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep relation_key | awk  -F \': \' \'{printf($2)}\''
				gateway_task_relation_key_1 = commands.getoutput(gateway_task_relation_key_1_commands)
				gateway_task_gmt_create_1_commands = vpcregiondb_info + ' -e \"select gmt_create from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep gmt_create | awk  -F \': \' \'{printf($2)}\''
				gateway_task_gmt_create_1 = commands.getoutput(gateway_task_gmt_create_1_commands)
				gw_oplog_history_info_1_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,relation_key,version,operation,data from gw_oplog_history where relation_key = \'' + gateway_task_relation_key_1 + '\' and gmt_create like \'%' + gateway_task_gmt_create_1 + '%\';\" 2>/dev/null | sed -n \'1!p\''
				gw_oplog_history_info_1 = commands.getoutput(gw_oplog_history_info_1_commands)
				for gw_oplog_history_info_line in gw_oplog_history_info_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:13s}{:10s}{:6s}".format(gw_oplog_history_info_line.split()[0],gw_oplog_history_info_line.split()[1],gw_oplog_history_info_line.split()[2],gw_oplog_history_info_line.split()[3],gw_oplog_history_info_line.split()[4],gw_oplog_history_info_line.split()[5],gw_oplog_history_info_line.split()[6])
			print '\n' + "gw_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:8s}".format('','id','gmt_modify','relation_type','relation_key','version')
			for gateway_task_id_1 in gateway_task_id_all.split():
				gateway_task_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from gateway_task where id = \'' + gateway_task_id_1 + '\'\\G\" 2>/dev/null | grep relation_key | awk  -F \': \' \'{printf($2)}\''
				gateway_task_relation_key_1 = commands.getoutput(gateway_task_relation_key_1_commands)
				gw_oplog_history_gw_key_version_1_commands = vpcregiondb_info + ' -e \"select id,gmt_modify,relation_type,relation_key,version from gw_key_version where relation_key = \'' + gateway_task_relation_key_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				gw_oplog_history_gw_key_version_1 = commands.getoutput(gw_oplog_history_gw_key_version_1_commands)
				for gw_oplog_history_gw_key_version_line in gw_oplog_history_gw_key_version_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:13s}{:9s}".format(gw_oplog_history_gw_key_version_line.split()[0],gw_oplog_history_gw_key_version_line.split()[1],gw_oplog_history_gw_key_version_line.split()[2],gw_oplog_history_gw_key_version_line.split()[3],gw_oplog_history_gw_key_version_line.split()[4],gw_oplog_history_gw_key_version_line.split()[5])
	else :
		print "！！！-----gateway_task没有此任务-----！！！"

if mvss_task_publish_task_id != "":
	print "-----------------------------------------------------------mvss_task区------------------------------------------------------------"
	mvss_task_detail_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail where mvss_task_id in (' + mvss_task_publish_task_relation_key + ')\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_id_all = commands.getoutput(mvss_task_detail_id_all_commands)
	mvss_task_detail_id = ','.join(mvss_task_detail_id_all.split())
	mvss_task_detail_history_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail_history where mvss_task_id in (' + mvss_task_publish_task_relation_key + ')\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_history_id_all = commands.getoutput(mvss_task_detail_history_id_all_commands)
	mvss_task_detail_history_id = ','.join(mvss_task_detail_history_id_all.split())
	if mvss_task_detail_id != "":
		print "阻塞任务未过期"
		print "mvss_task_detail:"
		print "{:4s}{:12s}{:15s}{:7s}{:11s}{:13s}".format('','id','gmt_create','status','oplog_type','oplog_id')
		for mvss_task_detail_id_1 in mvss_task_detail_id_all.split():
			mvss_task_detail_info_commands = vpcregiondb_info + ' -e \"select id,gmt_create,status,oplog_type,oplog_id from mvss_task_detail where id = \'' + mvss_task_detail_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
			mvss_task_detail_info = commands.getoutput(mvss_task_detail_info_commands)
			for mvss_task_detail_info_line in mvss_task_detail_info.split('\n'):
				print "{:11s}{:11s}{:12s}{:9s}{:7s}{:32s}".format(mvss_task_detail_info_line.split()[0],mvss_task_detail_info_line.split()[1],mvss_task_detail_info_line.split()[2],mvss_task_detail_info_line.split()[3],mvss_task_detail_info_line.split()[4],mvss_task_detail_info_line.split()[5])
	if mvss_task_detail_history_id != "":
		print "阻塞任务已过期"
		print "mvss_task_detail_history:"
		print "{:4s}{:12s}{:15s}{:7s}{:11s}{:13s}".format('','id','gmt_create','status','oplog_type','oplog_id')
		for mvss_task_detail_history_id_1 in mvss_task_detail_history_id_all.split():
			mvss_task_detail_history_info_commands = vpcregiondb_info + ' -e \"select id,gmt_create,status,oplog_type,oplog_id from mvss_task_detail_history where id = \'' + mvss_task_detail_history_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
			mvss_task_detail_history_info = commands.getoutput(mvss_task_detail_history_info_commands)
			for mvss_task_detail_history_info_line in mvss_task_detail_history_info.split('\n'):
				print "{:11s}{:11s}{:12s}{:9s}{:7s}{:32s}".format(mvss_task_detail_history_info_line.split()[0],mvss_task_detail_history_info_line.split()[1],mvss_task_detail_history_info_line.split()[2],mvss_task_detail_history_info_line.split()[3],mvss_task_detail_history_info_line.split()[4],mvss_task_detail_history_info_line.split()[5])
	mvss_task_detail_vpc_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail where id in (' + mvss_task_detail_id + ') and oplog_type = 1\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_vpc_id_all = commands.getoutput(mvss_task_detail_vpc_id_all_commands)
	mvss_task_detail_vpc_id = ','.join(mvss_task_detail_vpc_id_all.split())
	mvss_task_detail_vpc_oplog_id_all_commands = vpcregiondb_info + ' -e \"select oplog_id from mvss_task_detail where id in (' + mvss_task_detail_vpc_id + ')\\G\" 2>/dev/null | grep oplog_id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_vpc_oplog_id_all = commands.getoutput(mvss_task_detail_vpc_oplog_id_all_commands)
	mvss_task_detail_vpc_oplog_id = ','.join(mvss_task_detail_vpc_oplog_id_all.split())
	mvss_task_detail_history_vpc_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail_history where id in (' + mvss_task_detail_history_id + ') and oplog_type = 1\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_history_vpc_id_all = commands.getoutput(mvss_task_detail_history_vpc_id_all_commands)
	mvss_task_detail_history_vpc_id = ','.join(mvss_task_detail_history_vpc_id_all.split())
	mvss_task_detail_history_vpc_oplog_id_all_commands = vpcregiondb_info + ' -e \"select oplog_id from mvss_task_detail_history where id in (' + mvss_task_detail_history_vpc_id + ')\\G\" 2>/dev/null | grep oplog_id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_history_vpc_oplog_id_all = commands.getoutput(mvss_task_detail_history_vpc_oplog_id_all_commands)
	mvss_task_detail_history_vpc_oplog_id = ','.join(mvss_task_detail_history_vpc_oplog_id_all.split())
	if mvss_task_detail_vpc_id != "":
		if mvss_task_detail_vpc_oplog_id != "":
			print '\n' + "vpc_oplog:"
			print "{:4s}{:12s}{:15s}{:14s}{:18s}{:17s}".format('','id','gmt_create','relation_type','version','vpc_id')
			for mvss_task_detail_vpc_oplog_id_1 in mvss_task_detail_vpc_oplog_id_all.split():
				vpc_oplog_info_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,vpc_id from vpc_oplog where id = \'' + mvss_task_detail_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_info = commands.getoutput(vpc_oplog_info_commands)
				vpc_oplog_relation_key_commands = vpcregiondb_info + ' -e \"select relation_key from vpc_oplog where id = \'' + mvss_task_detail_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_relation_key = commands.getoutput(vpc_oplog_relation_key_commands)
				for vpc_oplog_info_line in vpc_oplog_info.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:6s}{}".format(vpc_oplog_info_line.split()[0],vpc_oplog_info_line.split()[1],vpc_oplog_info_line.split()[2],vpc_oplog_info_line.split()[3],vpc_oplog_info_line.split()[4],vpc_oplog_info_line.split()[5]) + vpc_oplog_relation_key
			print '\n' + "vpc_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:18s}{:17s}{:10s}".format('','id','gmt_create','relation_type','version','vpc_id','success_version')
			for mvss_task_detail_vpc_oplog_id_1 in mvss_task_detail_vpc_oplog_id_all.split():
				vpc_oplog_vpc_id_1_commands = vpcregiondb_info + ' -e \"select vpc_id from vpc_oplog where id = \'' + mvss_task_detail_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_vpc_id_1 = commands.getoutput(vpc_oplog_vpc_id_1_commands)
				vpc_oplog_relation_type_1_commands = vpcregiondb_info + ' -e \"select relation_type from vpc_oplog where id = \'' + mvss_task_detail_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_relation_type_1 = commands.getoutput(vpc_oplog_relation_type_1_commands)
				vpc_oplog_vpc_key_version_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,vpc_id,success_version from vpc_key_version where relation_type = \'' + vpc_oplog_relation_type_1 + '\' and vpc_id = \'' + vpc_oplog_vpc_id_1 +'\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_vpc_key_version = commands.getoutput(vpc_oplog_vpc_key_version_commands)
				if vpc_oplog_vpc_key_version != "":
					for vpc_oplog_vpc_key_version_line in vpc_oplog_vpc_key_version.split('\n'):
						print "{:11s}{:11s}{:14s}{:12s}{:5s}{:33s}{:10s}".format(vpc_oplog_vpc_key_version_line.split()[0],vpc_oplog_vpc_key_version_line.split()[1],vpc_oplog_vpc_key_version_line.split()[2],vpc_oplog_vpc_key_version_line.split()[3],vpc_oplog_vpc_key_version_line.split()[4],vpc_oplog_vpc_key_version_line.split()[5],vpc_oplog_vpc_key_version_line.split()[6])
				else:
					print 'vpc_key_version 没有 relation_type = ' + vpc_oplog_relation_type_1 + ' and vpc_id = ' + vpc_oplog_vpc_id_1 + ' 的数据记录'
	if mvss_task_detail_history_vpc_id != "":
		if mvss_task_detail_history_vpc_oplog_id != "":
			print '\n' + "vpc_oplog_history:"
			print "{:4s}{:12s}{:15s}{:14s}{:18s}{:17s}".format('','id','gmt_create','relation_type','version','vpc_id')
			for mvss_task_detail_history_vpc_oplog_id_1 in mvss_task_detail_history_vpc_oplog_id_all.split():
				vpc_oplog_history_info_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,vpc_id from vpc_oplog_history where id = \'' + mvss_task_detail_history_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_history_info = commands.getoutput(vpc_oplog_history_info_commands)
				vpc_oplog_history_relation_key_commands = vpcregiondb_info + ' -e \"select relation_key from vpc_oplog_history where id = \'' + mvss_task_detail_history_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_history_relation_key = commands.getoutput(vpc_oplog_history_relation_key_commands)
				for vpc_oplog_info_history_line in vpc_oplog_history_info.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:6s}{}".format(vpc_oplog_info_history_line.split()[0],vpc_oplog_info_history_line.split()[1],vpc_oplog_info_history_line.split()[2],vpc_oplog_info_history_line.split()[3],vpc_oplog_info_history_line.split()[4],vpc_oplog_info_history_line.split()[5]) + vpc_oplog_history_relation_key
			print '\n' + "vpc_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:18s}{:17s}{:10s}".format('','id','gmt_create','relation_type','version','vpc_id','success_version')
			for mvss_task_detail_history_vpc_oplog_id_1 in mvss_task_detail_history_vpc_oplog_id_all.split():
				vpc_oplog_history_vpc_id_1_commands = vpcregiondb_info + ' -e \"select vpc_id from vpc_oplog_history where id = \'' + mvss_task_detail_history_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_history_vpc_id_1 = commands.getoutput(vpc_oplog_history_vpc_id_1_commands)
				vpc_oplog_history_relation_type_1_commands = vpcregiondb_info + ' -e \"select relation_type from vpc_oplog_history where id = \'' + mvss_task_detail_history_vpc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_history_relation_type_1 = commands.getoutput(vpc_oplog_history_relation_type_1_commands)
				vpc_oplog_history_vpc_key_version_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,vpc_id,success_version from vpc_key_version where relation_type = \'' + vpc_oplog_history_relation_type_1 + '\' and vpc_id = \'' + vpc_oplog_history_vpc_id_1 +'\';\" 2>/dev/null | sed -n \'1!p\''
				vpc_oplog_history_vpc_key_version = commands.getoutput(vpc_oplog_history_vpc_key_version_commands)
				if vpc_oplog_history_vpc_key_version != "":
					for vpc_oplog_history_vpc_key_version_line in vpc_oplog_history_vpc_key_version.split('\n'):
						print "{:11s}{:11s}{:14s}{:12s}{:5s}{:33s}{:10s}".format(vpc_oplog_history_vpc_key_version_line.split()[0],vpc_oplog_history_vpc_key_version_line.split()[1],vpc_oplog_history_vpc_key_version_line.split()[2],vpc_oplog_history_vpc_key_version_line.split()[3],vpc_oplog_history_vpc_key_version_line.split()[4],	vpc_oplog_history_vpc_key_version_line.split()[5],vpc_oplog_history_vpc_key_version_line.split()[6])
				else:
					print 'vpc_key_version 没有 relation_type = ' + vpc_oplog_history_relation_type_1 + ' and vpc_id = ' + vpc_oplog_history_vpc_id_1 + ' 的数据记录'
	mvss_task_detail_nc_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail where id in (' + mvss_task_detail_id + ') and oplog_type = 2\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_nc_id_all = commands.getoutput(mvss_task_detail_nc_id_all_commands)
	mvss_task_detail_nc_id = ','.join(mvss_task_detail_nc_id_all.split())
	mvss_task_detail_nc_oplog_id_all_commands = vpcregiondb_info + ' -e \"select oplog_id from mvss_task_detail where id in (' + mvss_task_detail_nc_id + ')\\G\" 2>/dev/null | grep oplog_id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_nc_oplog_id_all = commands.getoutput(mvss_task_detail_nc_oplog_id_all_commands)
	mvss_task_detail_nc_oplog_id = ','.join(mvss_task_detail_nc_oplog_id_all.split())
	mvss_task_detail_history_nc_id_all_commands = vpcregiondb_info + ' -e \"select id from mvss_task_detail_history where id in (' + mvss_task_detail_history_id + ') and oplog_type = 2\\G\" 2>/dev/null | grep id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_history_nc_id_all = commands.getoutput(mvss_task_detail_history_nc_id_all_commands)
	mvss_task_detail_history_nc_id = ','.join(mvss_task_detail_history_nc_id_all.split())
	mvss_task_detail_history_nc_oplog_id_all_commands = vpcregiondb_info + ' -e \"select oplog_id from mvss_task_detail_history where id in (' + mvss_task_detail_history_nc_id + ')\\G\" 2>/dev/null | grep oplog_id | xargs -n2 | awk  -F \':\' \'{printf($2)}\''
	mvss_task_detail_history_nc_oplog_id_all = commands.getoutput(mvss_task_detail_history_nc_oplog_id_all_commands)
	mvss_task_detail_history_nc_oplog_id = ','.join(mvss_task_detail_history_nc_oplog_id_all.split())
	if mvss_task_detail_nc_id != "":
		if mvss_task_detail_nc_oplog_id != "":
			print '\n' + "nc_oplog:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:12s}{}".format('','id','gmt_create','relation_type','version','ip','relation_key')
			for mvss_task_detail_nc_oplog_id_1 in mvss_task_detail_nc_oplog_id_all.split():
				nc_oplog_info_1_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,ip from nc_oplog where id = \'' + mvss_task_detail_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_info_1 = commands.getoutput(nc_oplog_info_1_commands)
				nc_oplog_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from nc_oplog where id = \'' + mvss_task_detail_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_relation_key_1 = commands.getoutput(nc_oplog_relation_key_1_commands)
				for nc_oplog_info_line in nc_oplog_info_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:6s}{:19s}".format(nc_oplog_info_line.split()[0],nc_oplog_info_line.split()[1],nc_oplog_info_line.split()[2],nc_oplog_info_line.split()[3],nc_oplog_info_line.split()[4],nc_oplog_info_line.split()[5])	+ 	nc_oplog_relation_key
			print '\n' + "nc_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:12s}{:16s}{}".format('','id','gmt_create','relation_type','version','ip','success_version','relation_key')
			for mvss_task_detail_nc_oplog_id_1 in mvss_task_detail_nc_oplog_id_all.split():
				nc_oplog_ip_1_commands = vpcregiondb_info + ' -e \"select ip from nc_oplog where id = \'' + mvss_task_detail_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_ip_1 = commands.getoutput(nc_oplog_ip_1_commands)
				nc_oplog_relation_type_1_commands = vpcregiondb_info + ' -e \"select relation_type from nc_oplog where id = \'' + 				mvss_task_detail_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_relation_type_1 = commands.getoutput(nc_oplog_relation_type_1_commands)
				nc_oplog_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from nc_oplog where id = \'' + 				mvss_task_detail_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_relation_key_1 = commands.getoutput(nc_oplog_relation_key_1_commands)
				nc_oplog_nc_key_version_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,ip,success_version from nc_key_version where relation_type = \'' + nc_oplog_relation_type_1 + '\' and relation_key = \'' + nc_oplog_relation_key_1 + '\' and ip = \'' + nc_oplog_ip_1 +'\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_nc_key_version = commands.getoutput(nc_oplog_nc_key_version_commands)
				if nc_oplog_nc_key_version != "":
					for nc_oplog_nc_key_version_line in nc_oplog_nc_key_version.split('\n'):
						print "{:11s}{:11s}{:14s}{:11s}{:6s}{:24s}{:12s}".format(nc_oplog_nc_key_version_line.split()[0],nc_oplog_nc_key_version_line.split()[1],nc_oplog_nc_key_version_line.split()[2],nc_oplog_nc_key_version_line.split()[3],nc_oplog_nc_key_version_line.split()[4],	nc_oplog_nc_key_version_line.split()[5],nc_oplog_nc_key_version_line.split()[6]) + nc_oplog_relation_key_1
				else:
					print 'nc_key_version 没有 relation_type = ' + nc_oplog_relation_type_1 + ' and ip = ' + nc_oplog_ip_1 + ' and relation_key = ' + nc_oplog_relation_key_1 + ' 的数据记录'
	if mvss_task_detail_history_nc_id != "":
		if mvss_task_detail_history_nc_oplog_id != "":
			print '\n' + "nc_oplog_history:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:12s}{}".format('','id','gmt_create','relation_type','version','ip','relation_key')
			for mvss_task_detail_history_nc_oplog_id_1 in mvss_task_detail_history_nc_oplog_id_all.split():
				nc_oplog_history_info_1_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,ip from nc_oplog_history where id = \'' + mvss_task_detail_history_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_info_1 = commands.getoutput(nc_oplog_history_info_1_commands)
				nc_oplog_history_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from nc_oplog_history where id = \'' + mvss_task_detail_history_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_relation_key_1 = commands.getoutput(nc_oplog_history_relation_key_1_commands)
				for nc_oplog_history_info_line in nc_oplog_history_info_1.split('\n'):
					print "{:11s}{:11s}{:14s}{:11s}{:6s}{:19s}".format(nc_oplog_history_info_line.split()[0],nc_oplog_history_info_line.split()[1],nc_oplog_history_info_line.split()[2],nc_oplog_history_info_line.split()[3],nc_oplog_history_info_line.split()[4],nc_oplog_history_info_line.split()[5])	+ nc_oplog_history_relation_key_1
			print '\n' + "nc_key_version:"
			print "{:4s}{:12s}{:15s}{:14s}{:13s}{:12s}{:16s}{}".format('','id','gmt_create','relation_type','version','ip','success_version','relation_key')
			for mvss_task_detail_history_nc_oplog_id_1 in mvss_task_detail_history_nc_oplog_id_all.split():
				nc_oplog_history_ip_1_commands = vpcregiondb_info + ' -e \"select ip from nc_oplog_history where id = \'' + mvss_task_detail_history_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_ip_1 = commands.getoutput(nc_oplog_history_ip_1_commands)
				nc_oplog_history_relation_type_1_commands = vpcregiondb_info + ' -e \"select relation_type from nc_oplog_history  where id = \'' + 				mvss_task_detail_history_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_relation_type_1 = commands.getoutput(nc_oplog_history_relation_type_1_commands)
				nc_oplog_history_relation_key_1_commands = vpcregiondb_info + ' -e \"select relation_key from nc_oplog_history  where id = \'' + 				mvss_task_detail_history_nc_oplog_id_1 + '\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_relation_key_1 = commands.getoutput(nc_oplog_history_relation_key_1_commands)
				nc_oplog_history_nc_key_version_commands = vpcregiondb_info + ' -e \"select id,gmt_create,relation_type,version,ip,success_version from nc_key_version where relation_type = \'' + nc_oplog_history_relation_type_1 + '\' and relation_key = \'' + nc_oplog_history_relation_key_1 + '\' and ip = \'' + nc_oplog_history_ip_1 +'\';\" 2>/dev/null | sed -n \'1!p\''
				nc_oplog_history_nc_key_version = commands.getoutput(nc_oplog_history_nc_key_version_commands)
				if nc_oplog_history_nc_key_version != "":
					for nc_oplog_history_nc_key_version_line in nc_oplog_history_nc_key_version.split('\n'):
						print "{:11s}{:11s}{:14s}{:11s}{:6s}{:24s}{:12s}".format(nc_oplog_history_nc_key_version_line.split()[0],nc_oplog_history_nc_key_version_line.split()[1],nc_oplog_history_nc_key_version_line.split()[2],nc_oplog_history_nc_key_version_line.split()[3],nc_oplog_history_nc_key_version_line.split()[4],nc_oplog_history_nc_key_version_line.split()[5],nc_oplog_history_nc_key_version_line.split()[6]) + nc_oplog_history_relation_key_1
				else:
					print 'nc_key_version 没有 relation_type = ' + nc_oplog_history_relation_type_1 + ' and ip = ' + nc_oplog_history_ip_1 + ' and relation_key = ' + nc_oplog_history_relation_key_1 + ' 的数据记录'

