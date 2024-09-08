import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('C:\\Users\\Milind\\Desktop\\projects\\LoginApp_py\\test\\config.conf')

# Accessing data from the 'database' section
db_host = config.get('database', 'host')
db_port = config.getint('database', 'port')  # Convert to int
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')

# Accessing data from the 'server' section
server_debug = config.getboolean('server', 'debug')  # Convert to boolean
server_log_path = config.get('server', 'log_path')

# Print the values
print(f"Database Host: {db_host}")
print(f"Database Port: {db_port}")
print(f"Database User: {db_user}")
print(f"Server Debug Mode: {server_debug}")
print(f"Server Log Path: {server_log_path}")