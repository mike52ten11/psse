import configparser

def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('webinterface/config/config.ini')
    server_host = config.get('Server', 'api_ip')
    server_port = config.get('Server', 'api_port') 
    proxy_https = config.get('Proxies', 'https') 
    proxy_http = config.get('Proxies', 'http') 

    return   {"server_host":server_host,
              "server_port":server_port,
              "proxies": {'https':proxy_https,
                        'http':proxy_http}
              }

if __name__ == "__main__" :
      read_config()           