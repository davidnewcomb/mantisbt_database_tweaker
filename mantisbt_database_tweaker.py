#!/usr/bin/python
# ##############################################################################
#
# MantisBT Database Tweaker
#
# @copyright (c) 2000-2018 BigSoft Limited - {@link http://www.bigsoft.co.uk/}.
#
# @license The MIT License - https://opensource.org/licenses/MIT
#
# @author David Newcomb
#
# Requires MySQL support for Python:
# http://www.bigsoft.co.uk/blog/index.php/2011/07/07/installing-python-2-7-with-mysql-support-on-plesk-centos-5-5
#
# ##############################################################################
#

version = "2.0"

#
# ##############################################################################

# IMPORTS  #####################################################################

import sys

# CONFIG  ######################################################################

db_host = "localhost"
db_username = "root"
db_password = "mysql"
db_database = "mantisbt"
db_table_prefix = "mantis_"
db_table_suffix = "_table"

# DB  ##########################################################################

def _db(table_name):
	return db_table_prefix + table_name + db_table_suffix

def db_get_col(sql):
	db.query(sql)
	rows = db.store_result()
	x = rows.fetch_row()[0]
	return x[0]

def db_get_rows(sql):
	db.query(sql)
	rows = db.store_result()
	n_rows = rows.num_rows()
	list = []
	for x in range(0, n_rows):
		r = rows.fetch_row()
		xx = r[0]
		list.append(xx)
	return list

# GET  #########################################################################

def get_user_name(id):
	sql = "SELECT realname FROM " + _db("user") + " WHERE id = " + str(id)
	x = db_get_col(sql)
	x = x + " (" + str(id) + ")"
	return x

def get_bug_summary(id):
	sql = "SELECT summary FROM " + _db("bug") + " WHERE id = " + str(id)
	x = db_get_col(sql)
	x = x + " (" + str(id) + ")"
	return x

def get_bugnote_txt(id):
	sql = "SELECT note FROM " + _db("bugnote_text") + " bt, " + _db("bugnote") + " b WHERE b.id = " + str(id) + " AND b.bugnote_text_id = bt.id"
	x = db_get_col(sql)
	x = x + " (" + str(id) + ")"
	return x

def get_bugnote_text_id(bugnote_id):
	sql = "SELECT bugnote_text_id FROM " + _db("bugnote") + " WHERE id = " + str(bugnote_id)
	x = db_get_col(sql)
	return x

# ASK  #########################################################################

def ask_index(prompt):
	print prompt, ":",
	x = raw_input()
	xi = int(x) - 1
	return xi

def ask_free_text(prompt):
	print "Enter %s (press ^d to finish):" % (prompt,)
	lines = sys.stdin.readlines()

	txt = ""
	for line in lines:
		l = line.strip()
		if l == "":
			continue
		txt = "%s%s\n" % (txt, l)
	return txt

def ask_user_id():
	sql = "SELECT id, username, realname FROM " + _db("user") + " WHERE enabled = 1 ORDER BY realname"
	db.query(sql)
	rows = db.store_result()
	n_rows = rows.num_rows()
	for idx in range(0, n_rows):
		x = rows.fetch_row()[0]
		full_name = x[2].partition(" ")
		first = full_name[0]
		last = full_name[2]
		user_name = x[1]
		user_id = x[0]
		print "%3s %-12s %-20s %s" % (user_id, first, last, user_name)
	print "Select user id: ",
	x = raw_input()
	id = int(x)
	return x

def ask_project():
	sql = "SELECT id, name FROM %s ORDER BY name" % (_db("project"))
	rows = db_get_rows(sql)
	idx = 0
	for r in rows:
		idx = idx + 1
		print "%d) %s(%s)" % (idx, r[1], r[0])
	id = ask_index("Enter project")
	return rows[id]

def ask_category(project_id, prompt):
	sql = "SELECT category FROM %s WHERE project_id = %s ORDER BY category" % (_db("project_category"), project_id)
	rows = db_get_rows(sql)
	idx = 0
	for r in rows:
		idx = idx + 1
		print "%d) %s" % (idx, r[0])
	x = ask_index(prompt)
	return rows[x][0]

def ask_id(field):
	print "Enter " + field + " number: ",
	x = raw_input()
	id = int(x)
	return id

def ask_time_tracking():
	print "Enter time tracking [hh:mm] or [mm]:",
	x = raw_input()
	idx = x.split(":", 2)
	if len(idx) == 1:
		minutes = int(idx[0])
	else:
		h = int(idx[0])
		m = int(idx[1])
		minutes = h * 60 + m
	return minutes

def ask_time():
	print "Enter time [YYYY-MM-DD HH:MM:SS]: ",
	x = raw_input()
	x = x.strip()
	return x

# UTILS  #######################################################################

def is_no():
	print "[y/n]:",
	x = raw_input()
	if x == "y":
		return False
	return True

def print_title(x):
	print ""
	print "=" * (len(x) + 1)
	print x
	print "-" * (len(x) + 1)
	print ""

def trim_to(s, l):
	if len(s) < l:
		return s
	x = s[0:(l - 3)] + "..."
	return x

def flatten_text(txt):
	txt = " ".join(txt.split())
	txt = trim_to(txt, 80)
	return txt

def module_exists(module_name):
	try:
		__import__(module_name)
	except ImportError:
		return False
	else:
		return True

# PAGES ########################################################################

def option_screen():
	print ""
	title = "Mantis Database Tweaker v%s" % (version,)
	print title
	print "=" * (len(title) + 1)

	idx = 1
	for opt in options:
		o = opt[0]
		if len(opt) == 1:
			print ""
			print o
			print "-" * (len(o) + len(str(idx)) - 1)
			continue
		print "%d) %s" % (idx, opt[0])
		idx = idx + 1
	print ""
	print "Enter selection (return to exit):",
	x = raw_input()
	if x == "":
		return None
	if x.isdigit() == False:
		return None
	xi = int(x)
	xi = xi - 1

	real_idx = 0
	diff = 0
	for opt in options:
		if len(opt) == 1:
			real_idx = real_idx + 1
			diff = diff + 1
			continue
		if xi == (real_idx - diff):
			break
		real_idx = real_idx + 1

	if len(options) == real_idx:
		return None

	return options[real_idx]

def add_monitor():
	print_title("Add monitor")
	user_id = ask_user_id()
	bug_id = ask_id("bug")
	user = get_user_name(user_id)
	bug = get_bug_summary(bug_id)
	print "Add '" + user + "' as monitor to '" + bug + "'"
	if is_no():
		return

	sql = "DELETE FROM %s WHERE bug_id = %s AND user_id = %s" % (_db("bug_monitor"), bug_id, user_id)
	print sql
	db.query(sql)
	sql = "INSERT INTO %s(bug_id, user_id) VALUES (%s, %s)" % (_db("bug_monitor"), bug_id, user_id)
	print sql
	db.query(sql)

def delete_monitor():
	print_title("Delete monitor")
	user_id = ask_user_id()
	bug_id = ask_id("bug")
	user = get_user_name(user_id)
	bug = get_bug_summary(bug_id)
	print "Delete '" + user + "' from '" + bug + "'"
	if is_no():
		return

	sql = "DELETE FROM %s WHERE bug_id = %s AND user_id = %s" % (_db("bug_monitor"), bug_id, user_id)
	print sql
	db.query(sql)

def move_bugnote():
	print_title("Move bugnote")
	bugnote_id = ask_id("bugnote")
	bug_id = ask_id("bug")
	bug = get_bug_summary(bug_id)
	bugnote = get_bugnote_txt(bugnote_id)
	bugnote = trim_to(bugnote, 70)
	print "==========================="
	print "Move:"
	print "==========================="
	print bugnote
	print "==========================="
	print "To:", bug
	if is_no():
		return

	sql = "SELECT bug_id FROM %s WHERE id = %s" % (_db("bugnote"), bugnote_id)
	old_id = db_get_col(sql)
	sql = "UPDATE %s SET bug_id = %s WHERE id = %s" % (_db("bugnote"), old_id, bugnote_id)
	print "Rollback:", sql

	sql = "UPDATE %s SET bug_id = %s WHERE id = %s" % (_db("bugnote"), bug_id, bugnote_id)
	print sql
	db.query(sql)

def modify_time_tracking():
	print_title("Modify time tracking")
	bugnote_id = ask_id("bugnote")
	bugnote = get_bugnote_txt(bugnote_id)
	bugnote = trim_to(bugnote, 70)
	time = ask_time_tracking()
	print "==========================="
	print "Modify time tracking for:"
	print "==========================="
	print bugnote
	print "==========================="
	print "To:", time
	if is_no():
		return

	sql = "SELECT time_tracking FROM %s WHERE id = %s" % (_db("bugnote"), bugnote_id)
	old_time = db_get_col(sql)
	print "Rollback: UPDATE %s SET time_tracking = %s WHERE id = %s" % (_db("bugnote"), old_time, bugnote_id)

	sql = "UPDATE %s SET time_tracking = %s WHERE id = %s" % (_db("bugnote"), time, bugnote_id)
	print sql
	db.query(sql)

def modify_bug_owner():
	print_title("Change bug owner")
	user_id = ask_user_id()
	user = get_user_name(user_id)
	bug_id = ask_id("bug")
	bug = get_bug_summary(bug_id)
	print "Change owner of '" + bug + "' to '" + user + "'"
	if is_no():
		return

	sql = "SELECT reporter_id FROM %s WHERE id = %s" % (_db("bug"), bug_id)
	old_reporter_id = db_get_col(sql)

	print "Rollback: UPDATE %s SET reporter_id = %s WHERE id = %s" % (_db("bug"), old_reporter_id, bug_id)
	sql = "UPDATE %s SET reporter_id = %s WHERE id = %s" % (_db("bug"), user_id, bug_id)
	print sql
	db.query(sql)

def modify_bugnote_owner():
	print_title("Change bugnote owner")
	user_id = ask_user_id()
	user = get_user_name(user_id)
	bugnote_id = ask_id("bugnote")
	bugnote_txt = get_bugnote_txt(bugnote_id)
	bugnote_txt = flatten_text(bugnote_txt)
	print "Change owner of '" + bugnote_txt + "' to '" + user + "'"
	if is_no():
		return

	sql = "SELECT reporter_id FROM %s WHERE id = %s" % (_db("bugnote"), bugnote_id)
	old_reporter_id = db_get_col(sql)

	print "Rollback: UPDATE %s SET reporter_id = %s WHERE id = %s" % (_db("bugnote"), old_reporter_id, bugnote_id)
	sql = "UPDATE %s SET reporter_id = %s WHERE id = %s" % (_db("bugnote"), user_id, bugnote_id)
	print sql
	db.query(sql)

def modify_category():
	print_title("Modify category")
	bug_id = ask_id("bug")
	bug = get_bug_summary(bug_id)

	sql = "SELECT project_id FROM %s WHERE id = %s" % (_db("bug"), bug_id)
	project_id = db_get_col(sql)[0]

	sql = "SELECT name FROM %s WHERE id = %s" % (_db("project"), project_id)
	project_name = db_get_col(sql)

	category = ask_category(project_id)

	print "Change category of '%s' to '[%s] %s'" % (bug, project_name, category)
	if is_no():
		return

	sql = "SELECT category FROM %s WHERE id = %s" % (_db("bug"), bug_id)
	old_category = db_get_col(sql)
	print "Rollback: UPDATE %s SET category = \"%s\" WHERE id = %s" % (_db("bug"), old_category, bug_id)

	sql = "UPDATE %s SET category = \"%s\" WHERE id = %s" % (_db("bug"), category, bug_id)
	print sql
	db.query(sql)

def delete_category():
	print_title("Delete category, move bugs to new category")

	project = ask_project()
	project_id = project[0]
	project_name = project[1]

	category_new = ask_category(project_id, "Enter category to move bugs to")
	category_old = ask_category(project_id, "Enter category to delete")

	print "Move '%s' bugs to '[%s] %s'" % (category_old, project_name, category_new)
	if is_no():
		return

	sql = "UPDATE %s SET category = \"%s\" WHERE project_id = %s AND category = \"%s\"" % (_db("bug"), category_new, project_id, category_old)
	db.query(sql)
	print sql
	sql = "DELETE FROM %s WHERE project_id = %s AND category = \"%s\"" % (_db("project_category"), project_id, category_old)
	print sql
	db.query(sql)

def add_bugnote():
	print_title("Add a bugnote to a bug")

	bug_id = ask_id("bug")
	user_id = ask_user_id()
	time = ask_time();
	text = ask_free_text("bugnote")
	text_sql = _mysql.escape_string(text)

	user = get_user_name(user_id)
	bug = get_bug_summary(bug_id)

	print "Add bugnote to:-"
	print "Bug: %s" % (bug,)
	print "User: %s" % (user,)
	print "When: %s" % (time,)
	print "Notes: %s" % (text,)

	if is_no():
		return

	sql = "INSERT INTO %s(note) VALUES(\"%s\")" % (_db("bugnote_text"), text_sql)
	print sql
	db.query(sql)
	note_id = db.insert_id()
	print "Rollback: DELETE FROM %s WHERE id = \"%s\"" % (_db("bugnote_text"), note_id)

	if time == "":
		time_str = "UNIX_TIMESTAMP()";
	else:
		time_str = "\"%s\"" % (time,)

	sql = "INSERT INTO %s(bug_id, reporter_id, bugnote_text_id, view_state, note_type, note_attr, time_tracking, last_modified, date_submitted) \
		 VALUES      (%s,       %s,             %s,           10,        0,         \"\",        0,           %s,           %s)" \
	%     (_db("bugnote"), bug_id,   user_id,     note_id,                                                     time_str,      time_str)
	print sql
	db.query(sql)
	bugnote_id = db.insert_id()
	print "Rollback: DELETE FROM %s WHERE id = \"%s\"" % (_db("bugnote"), bugnote_id)

def modify_bugnote_time():
	print_title("Modify the time a bugnote was submitted")
	
	bugnote_id = ask_id("bugnote")
	the_time = ask_time()
	
	bugnote_txt = get_bugnote_txt(bugnote_id)

	print bugnote_txt
	print "New time: %s" % (the_time,)

	if is_no():
		return

	sql = "UPDATE %s SET last_modified = UNIX_TIMESTAMP(\"%s\"), date_submitted = UNIX_TIMESTAMP(\"%s\") WHERE id = %s" % (_db("bugnote"), the_time, the_time, bugnote_id)
	print sql
	db.query(sql)


# FUTURES  - To come ###########################################################

# UPDATE mantis_bug_table SET date_submitted = UNIX_TIMESTAMP('2012-04-16 16:19:00') WHERE id = 620;
# UPDATE mantis_bug_table SET last_updated = UNIX_TIMESTAMP('2012-04-16 16:19:00') WHERE id = 620;


# MAIN #########################################################################

if module_exists("_mysql") == False:
	print "Can not import _mysql"
	sys.exit()
else:
	import _mysql

if db_username == "my_username" or db_password == "my_password" or db_database == "my_database":
	print "Edit this file to change database authentication"
	sys.exit()

options = (
	 ["Bugs"]
	,["Change owner", modify_bug_owner]
	,["Monitor"]
	,["Add monitor to an issue", add_monitor]
	,["Delete monitor from issue", delete_monitor]
	,["Bugnotes"]
	,["Add bugnote", add_bugnote]
	,["Move bugnote", move_bugnote]
	,["Modify time tracking", modify_time_tracking]
	,["Modify time", modify_bugnote_time]
	,["Modify owner", modify_bugnote_owner]
	,["Categories"]
	,["Modify category", modify_category]
	,["Delete category", delete_category]
	)



db = _mysql.connect(db_host, db_username, db_password, db_database)

opt = option_screen()
if opt == None:
	print "Exiting..."
	sys.exit()

opt[1]()

db.close()

