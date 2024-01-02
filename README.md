# Tefas History

Small project to download tefas (https://fundturkey.com.tr) historical fund data to local database (sqlite3) for potential further analysis.

## Usage

`python3 -m app.main`

You can bind this to a cronjob and have it download the fund data starting from the latest date in the local database to the current date. Note that tefas api current only allows querying for only 3 months prior.

The local database is created on the working directory. If you use a docker image and want to export the .db file, you can use a temporary container like this for exporting it to host machine:

`docker run --rm -v tefas_db_volume:/db -v $(pwd):/tefas_backup alpine:latest cp /db/tefas.db /tefas_backup/`

This assumes that you bound your image to a custom volume named `tefas_db_volume` for persistence.

## Thanks

This project depends on the tefas-crawler project: https://github.com/burakyilmaz321/tefas-crawler