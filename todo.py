#! /sw/bin/python
# filename: todo.py
# author: MuhammadNM
#
# A simple todo list app using Python(2.7) and sqlite2 on CLI only

from sqlite3 import dbapi2 as sqlite

import sys
import time

def list():

	sqlstatement = "SELECT id, task, status FROM tasks WHERE status = 0"

	if len(sys.argv) > 2:
		if sys.argv[2] == "all":
			sqlstatement = "SELECT id, task, status FROM tasks;"
		elif sys.argv[2] == "completed":
			sqlstatement = "SELECT id, task, status FROM tasks WHERE status <> 0"

	try:
		cur.execute(sqlstatement)
		records = cur.fetchall()
		counter = 0
		for rec in records:
			counter = counter + 1

			if rec[2] == 0:
				status = "*"
			else:
				status = "Completed"
			print  "[#",rec[0],"]", rec[1], " => ", status

		print 'Note: * is not compelted tasks'
	except sqlite.Error, e:
		print "Ooops:", e.args[0]

def add(param):
	try:
		created = int(time.time())
		sql = "INSERT INTO tasks (task, status, created_at) VALUES ('" + param + "', 0," + str(created) + ")"
		cur.execute(sql)
		conn.commit()
		print "Added: 1 task [#"+ str(cur.lastrowid) +"]"
	except sqlite.Error, e:
		print "Ooops:", e.args[0]

def delete(param):

	try:
		cur.execute("DELETE FROM tasks WHERE ID='" + param + "'")
		conn.commit()
		print "Deleted: #", param
	except sqlite.Error, e:
		print "Ooops:", e.args[0]

def complete(param):

	try:
		cur.execute("UPDATE tasks set status=1" + " WHERE id=" + param)
		conn.commit()
		print "Completed: #", param
	except sqlite.Error, e:
		print "Ooops:", e.args[0]

def main():

	global conn
	global cur

	try:
		conn = sqlite.connect("pytodo.sqlite")
		cur = conn.cursor()
	except sqlite.Error, e:
		print "Ooops: ", e.args[0]

	usage = "Usage is: $todo.py list [all/completed] | add 'Task Details' | delete #TASK_ID | complete #TASK_ID"
	if len(sys.argv) == 1 :
		print usage
		sys.exit(0)
	carg = sys.argv[1]

	if carg == "add":
		if len(sys.argv) < 3:
			print "What task? Add some task details please!"
			sys.exit(0)
		add(sys.argv[2])
	elif carg == "delete":
		if len(sys.argv) < 3:
			print "Which task you want to delete? #ID please!"
			sys.exit(0)
		delete(sys.argv[2])
	elif carg == "complete":
		if len(sys.argv) < 3:
			print "Which task you want to complete? #ID please!"
			sys.exit(0)
		complete(sys.argv[2])
	elif carg == "list":
		list()
	else:
		print usage

if __name__ == "__main__":
	main()
