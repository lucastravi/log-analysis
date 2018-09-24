# Logs Analysis Project - Lucas Travi

The **Logs Analysis Project** is a Python 2.7 application that get and print out the results for the three most searched articles, the most viewed authors and the days on which the requests led to more than 1% of errors.

### Running the Application
1. Download the zip file and unzip the folder that contains a Vagrantfile and a directory with the application;
2. You need to have Python 2.7 installed in your machine, download it accessing: https://www.python.org/download/releases/2.7/]
3. For Windows and Mac users: you must have a Virtual Machine software installed in your computer to run a Linux system in your machine, for this application is suggested to use Virtualbox and Vagrant, the most recent versions, download it accessing: https://www.virtualbox.org/wiki/Downloads, https://www.vagrantup.com/downloads.html;
4. If you are using a Windows based system, is suggested install Git Bash, download it acessing: https://git-for-windows.github.io/.
5. From the command line (or Git Bash interface), run "vagrant up" in the same directory that contains the Vagrantfile;
6. The Vagrantfile is already configured to run this application, wait some minutes for the downloads and installations;
7. In the same directory, run "vagrant ssh" to login in the Linux system;
8. Go to the directory containing the application running "$ cd /vagrant/loganalysis";
9. Run "psql -d news -f newsdata.sql" to log into the database and import the tables from newsdata.sql file;
10. Quit psql running "\q";
9. In the loganalysis directory, run "python log_analysis.py".

### Files contained:
1. Vagrantfile
2. log_analysis.py
3. output.txt
4. newsdata.sql

### Views created
1 - av: author views
create view av as select authors.name, articles.title, articles.slug, articles.id from authors, articles where articles.author = authors.id group by authors.id, authors.name, articles.title, articles.slug, articles.id order by authors.id;
2 - artv: article views
create view artv as select substring(path,10), count( * ) from log where not path='/' group by path order by count desc limit 8;
3 - ne: number of errors
create view ne as select cast(count(status) as numeric) as errors, date(time) from log where not status = '200 OK' group by date;
4 - nl: number of logs
create view nl as select cast(count(id) as numeric) as logs, date(time) from log group by date;
5 - exl: errors x logs
create view exl as select ne.errors, nl.logs, ne.date from ne, nl where ne.date = nl.date group by ne.errors, nl.logs, ne.date order by ne.errors desc;
