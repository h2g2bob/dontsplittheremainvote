# Server install

It's made of:

- static html files
- a wsgi postcode lookup

Served with apache2

## Set up a server

```
apt-get update
apt-get dist-upgrade
apt-get install unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

```
apt-get install postgresql apache2 libapache2-mod-wsgi-py3
```

## Set up the database

```
sudo -u postgres createuser dontsplit
sudo -u postgres createdb dontsplit -O dontsplit
adduser dontsplit
```

```
su - dontsplit
psql
dontsplit=> create table postcodes_sqlite (postcode text, slug text);
```

Import the postcode data:

```
apt-get install sqlite3
su - dontsplit
wget https://dontsplittheremainvote.dbatley.com/postcodes.sqlite3
echo $'.mode csv\nselect * from postcodes;' | sqlite3 postcodes.sqlite3 | psql -c "copy postcodes_sqlite from stdin with (format 'csv');"
```

Let's store postcode and constituency in different tables - we might add extra data to constituency:

```
dontsplit=> create table constituency (constituency_id serial primary key, slug text unique not null);
dontsplit=> create table postcode (postcode text primary key, constituency_id int references constituency(constituency_id));
dontsplit=> insert into constituency (slug) select distinct slug from postcodes_sqlite;
dontsplit=> insert into postcode (postcode, constituency_id) select sq.postcode, c.constituency_id from postcodes_sqlite sq join constituency c using (slug);
```


## Setting up WSGI

```
apt-get install python3-flask python3-psycopg2
```

```
# scp data.dontsplittheremainvote.com.conf remote:/etc/apache2/sites-available/
a2ensite data.dontsplittheremainvote.com
a2dissite 000-default
systemctl reload apache2.service
```

```
mkdir -p /home/dontsplit/dontsplittheremainvote/postcodes-data-service/public/
# scp wsgi.py remote:/home/dontsplit/dontsplittheremainvote/postcodes-data-service/public/
chown -R dontsplit:dontslit /home/dontsplit/dontsplittheremainvote/
```

## Copy static files

```
sudo -u dontsplit mkdir /home/dontsplit/dontsplittheremainvote/generated/
apt-get install rsync
```

```
./do_rsync.sh
```
