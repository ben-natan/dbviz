import click as click
import psycopg2
import matplotlib.pyplot as plt

def display_table_size(record: list, scale: str) -> None:
    tables_names = [record[i][0] for i in range(len(record))]
    full_size = [record[i][1] for i in range(len(record))]
    scale_name = ''
    if scale == 'k':
        for i in range(len(full_size)):
            full_size[i] = full_size[i] / 10**3
        scale_name = 'kB'
    elif scale == 'm':
        for i in range(len(full_size)):
            full_size[i] = full_size[i] / 10**6
        scale_name = 'MB'
    elif scale == 'g':
        for i in range(len(full_size)):
            full_size[i] = full_size[i] / 10**9
        scale_name = 'GB'    
    else:
        print('Scale not supported')
        return
    
    plt.bar(tables_names, full_size)
    plt.ylabel(scale_name)
    plt.title('Tables size')
    plt.show()


@click.command()
@click.option('--user', default='postgres')
@click.option('--password', default='')
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5432)
@click.option('--database',  required=True)
@click.option('--scale', default='m')
def main(user: str, password: str, host: str, port: int, database: str, scale: str) -> None:
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        print('Initiated PostgreSQL connection')
        cursor = connection.cursor()
        cursor.execute('select relname, pg_total_relation_size(relname::regclass) as full_size, pg_size_pretty(pg_relation_size(relname::regclass)) as table_size, pg_size_pretty(pg_total_relation_size(relname::regclass) - pg_relation_size(relname::regclass)) as index_size from pg_stat_user_tables order by pg_total_relation_size(relname::regclass) desc limit 10;')
        record = cursor.fetchall()
        print(record)
        display_table_size(record, scale)
        connection.close()
        print("PostgreSQL connection is closed")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        
    
if __name__ == '__main__':
    main()