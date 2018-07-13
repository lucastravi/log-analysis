#!/usr/bin/env python
#
# log_analysis.py -- implementation of a log analysis application
#


import psycopg2

# Connect to the tournament database using PostgreSQL


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=news")


def getPopularArticles():
    """Shows the top three most popular articles"""
    db = connect()
    cur = db.cursor()
    sql_command = """SELECT av.title, artv.count FROM av, artv
                    WHERE av.slug = artv.substring GROUP BY av.title
                    , artv.count
                    ORDER BY artv.count DESC LIMIT 3;"""
    cur.execute(sql_command)
    result = cur.fetchall()
    print("Most Popular Articles:")
    for row in result:
        plot = '{article}: {views} views.'.format(article=row[0], views=row[1])
        print(plot)


def getPopularAuthors():
    """Show the authors sorted by number of views"""
    db = connect()
    cur = db.cursor()
    sql_command = """SELECT av.name, SUM(artv.count) as total_views FROM av, artv
                    WHERE av.slug = artv.substring
                    GROUP BY av.name ORDER BY total_views DESC;"""
    cur.execute(sql_command)
    result = cur.fetchall()
    print("Most Popular Authors:")
    for row in result:
        plot = '{author}: {views} views.'.format(author=row[0], views=row[1])
        print(plot)


def getErrors():
    """Returns the percentage(rate) of errors per day"""
    db = connect()
    cur = db.cursor()
    sql_command = """SELECT date, ((errors*100)/(logs)) as error_rate
                    from exl WHERE ((errors*100)/(logs)) > 1
                    GROUP BY date, ((errors*100)/(logs))
                    ORDER BY ((errors*100)/(logs)) DESC;"""
    cur.execute(sql_command)
    result = cur.fetchall()
    print("Days on which more than 1'%' of the requests led to errors:")
    for row in result:
        plot = '{date}: {error_rate} %.'.format(date=row[0], error_rate=row[1])
        print(plot)


print('')
getPopularArticles()
print('')
getPopularAuthors()
print('')
getErrors()
print('')
