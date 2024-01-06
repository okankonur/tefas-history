# Tefas History

Small project to download tefas (https://fundturkey.com.tr) historical fund data to local database (sqlite3) for potential further analysis.

## Features

- Downloads all fund data to local db table. (tbl_tefas)
- Calculates profit percentages of these funds over periods (1mo, 3mo, 6mo, 1y) and saves it (tbl_tefas_profit)
- Sends email to configured recipients 

## Usage

`python3 -m app.main`

You can bind this to a cronjob and have it download the fund data starting from the latest date in the local database to the current date. Note that tefas api current only allows querying for only 3 months prior.

## Docker

```
cd tefas-history
docker build -t tefas-history .
```

The local database is created on the working directory. If you use a docker image and want to export the .db file, you can use a temporary container like this for exporting it to host machine:

```
docker run --rm -v tefas_db_volume:/db -v $(pwd):/tefas_backup alpine:latest cp /db/tefas.db /tefas_backup/
```
[!NOTE]
This assumes that you bound your image to a custom volume named `tefas_db_volume` for persistence.

## Email Properties

You should place an email_config.properties file inside /config directory.
It should look like this:
```
[EmailSettings]
email_user = test@gmx.com
email_password = gfdw454
email_send = test@gmail.com
```

## Thanks

This project depends on the tefas-crawler project: https://github.com/burakyilmaz321/tefas-crawler