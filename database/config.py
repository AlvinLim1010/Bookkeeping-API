import os
from termcolor import colored



def setDatabaseURL():
    user = os.getenv('DB_USER',None)
    password = os.getenv('DB_PASSWORD',None)
    host = os.getenv('DB_HOST',None)
    port = os.getenv('DB_PORT',None)
    name = os.getenv('DB_NAME',None)

    # if None in locals() :
    if None in [user,password,host,port,name] :
        print(colored('Database Connection','green'), f"Using default database, sqlite:///db.sqlite")

        basedirectory = os.path.abspath(os.path.dirname(__file__))
        directory = 'sqlite:///' + os.path.join(basedirectory,'data.sqlite')

        return directory

    else :
        print(colored('Database Connection','green'), f"Using postgresql with {host}:{port}/{name}")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"  