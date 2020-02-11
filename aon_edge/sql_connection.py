

def sql_connection(ServerName, DBName):
    """Returns a SQLAlchemy engine, given the server and database name.
    
    Params:
        ServerName (str): - Server name
        DBName (str): - Database name
    
    Returns:
        Object of type (sqlalchemy.engine.base.Engine) for use in pandas pd.to_sql functions
    """
    
    from sqlalchemy import create_engine

    sqlcon = create_engine('mssql+pyodbc://@' +
                           ServerName +
                           '/' +
                           DBName +
                           '?driver=ODBC+Driver+13+for+SQL+Server',
                           fast_executemany=True)
    
    return sqlcon
