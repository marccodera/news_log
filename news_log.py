#!/usr/bin/env python3
"""
Database code for news log analysis
Creates connection for every question,
so the DB is closed every time for security
"""

# Import connection to DB library
import psycopg2

# Creation of DB name variable to connect to it
DBNAME = "news"


# Connect to the DB and get the first we need
def get_articles_most_seen():
	"""
	Prints the 3 most popular articles of all time
	Returns the result of one SQL query
	"""
	try:
		# A try is worthit to catch errors
		conn = psycopg2.connect(database=DBNAME)
	except:
		print ("I am unable to connect to the database")

	cur = conn.cursor()
	# Cursor for connection is created to do some operations in the DB

	view1 = (
		"create temp view log_articles as select articles.title, "
		"articles.author from articles join log on articles.slug "
		"= (regexp_split_to_array(path,E'/article/'))[2];")

	cur.execute(view1)
	# Articles temp view while joining log and articles tables for next query

	select1 = (
		"select title, count(title) as total "
		"from log_articles group by title order by total desc limit 3;")
	cur.execute(select1)
	# Select and sort them descending, showing only first 3 results

	return cur.fetchall()
	# Returns the result of one SQL query

	conn.close()
	# Connection is needed to be closed


def get_authors_most_seen():
	"""
	Prints the 3 most popular authors of all time
	Returns the result of one SQL query
	"""
	try:
		# A try is worthit to catch errors
		conn = psycopg2.connect(database=DBNAME)
	except:
		print ("I am unable to connect to the database")

	cur = conn.cursor()
	# Cursor for connection is created to do some operations in the DB

	view1 = (
		"create temp view log_articles as select articles.title, "
		"articles.author from articles join log on articles.slug "
		"= (regexp_split_to_array(path,E'/article/'))[2];")

	cur.execute(view1)
	# Articles temp view while joining log, authors and articles tables

	select1 = (
		"select authors.name, count(log_articles.title) as total "
		"from log_articles join authors on log_articles.author "
		"= authors.id group by authors.name order by total desc;")

	cur.execute(select1)
	# Then just count, order them, and that’s it

	return cur.fetchall()

	conn.close()
	# Connection is needed to be closed


def get_log_errors_day_percent():
	"""
	Prints the 3 most popular authors of all time
	Returns the result of one SQL query
	"""
	try:
		# A try is worthit to catch errors
		conn = psycopg2.connect(database=DBNAME)
	except:
		print ("I am unable to connect to the database")

	cur = conn.cursor()
	# Cursor for connection is created to do some operations in the DB

	view1 = (
		"create temp view requests as select time ::timestamp::date as date, "
		"count(status) as total from log group by date order by date;")

	cur.execute(view1)
	# Create temp view with the total number of requests

	view2 = (
		"create temp view errors as select time ::timestamp::date as date, "
		"count(status) as total from log where status <> '200 OK' "
		"group by date order by date;")

	cur.execute(view2)
	# Create temp view with the total errors number

	view3 = (
		"create temp view results as select requests.date, "
		"((cast(errors.total as float) / cast(requests.total as float))"
		" * 100) as errors_percent from requests "
		"join errors on requests.date = errors.date;")

	cur.execute(view3)
	# Temp view joining previous views and calculating percentage

	cur.execute("select * from results where errors_percent > 1;")
	# Select only higher than 1% from the view

	return cur.fetchall()

	conn.close()
	# Connection is needed to be closed

text1 = (
	"\n- Descending list with the three most popular "
	"articles of all time:")
print (text1)
articles = get_articles_most_seen()
# articles is a list of tuples and it has to be printed in a nicely way
for p in articles:
	print (p[0], " - ", p[1])

text2 = (
	"\n- Descending list with the ranking of the most "
	"popular authors of all time:")
print (text2)
authors = get_authors_most_seen()
# authors is a list of tuples and it has to be printed in a nicely way
for p in authors:
	print (p[0], " - ", p[1])

print ("\n- Descending list of days having more than 1% of errors:")
errors = get_log_errors_day_percent()
# errors is a list of tuples and it has to be printed in a nicely way
for p in errors:
	print (p[0], " - ", p[1])
