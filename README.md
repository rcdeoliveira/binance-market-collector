This is a simple script that collects asks and bids for a particular symbol 
(e.g. BTCUSDT) and stores it into a InfluxDB database. The measurement always 
will be the symbol name.

# Requirements #

The script needs the following python 3 modules: configparser, python-binance, 
and influxdb.

Also the script needs the database already created.

# Configuration #

Before launch the script, modify config.ini with your custom values (which are 
pretty self explanatory)
