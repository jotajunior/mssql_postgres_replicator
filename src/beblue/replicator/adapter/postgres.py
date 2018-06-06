from beblue.replicator.adapter import BaseQuery
from beblue.replicator import config
from sqlalchemy import create_engine
import tempfile
import shutil
import os

class PostgresQuery:
    @staticmethod
    def execute_changes(filename):
        os.system("""export PGPASSWORD='{password}';
        psql -U {user} -d {database} -h {host} < {filename}""".format(
            password=config.database['postgres']['password'],
            host=config.database['postgres']['host'],
            database=config.database['postgres']['database'],
            filename=filename,
            user=config.database['postgres']['user']))

    @staticmethod
    def get_last_sync():
        conn = PostgresQuery.get_conn()
        query = """
        CREATE TABLE IF NOT EXISTS "replicator_sync" (
            id  bigserial primary key,
            version bigint not null,
            created_at timestamp without time zone default (now() at time zone 'utc')
            );
        
        SELECT version FROM replicator_sync ORDER BY id DESC LIMIT 1;"""
        result = [i for i in conn.execute(query)]
        conn.close()
        if not result:
            return -1
        else:
            return result[0][0]


    @staticmethod
    def get_conn():
        engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(
            user=config.database['postgres']['user'],
            password=config.database['postgres']['password'],
            host=config.database['postgres']['host'],
            db=config.database['postgres']['database']))
        return engine.connect()

    @staticmethod
    def _generate_insert_query(insert, table, columns):
        query = 'INSERT INTO {table} ({columns}) VALUES '.format(
                table=table,
                columns=', '.join(columns))

        
        query += '(' + ', '.join([i for i in insert]) + ');\n'
       
        return query

    @staticmethod
    def _generate_update_query(update, table, columns, primary_keys):
        pk_indexes = [columns.index(i) for i in primary_keys]

        query = 'UPDATE {table} SET '.format(table=table)
        _set = []
        for i in range(len(update)):
            _set.append('{} = {}'.format(columns[i], update[i]))
        query += ', '.join(_set)
        if primary_keys:
            query += ' WHERE '
            query += ' AND '.join(['{} = {}'.format(
                primary_keys[i],
                update[pk_indexes[i]],
                ) for i in range(len(primary_keys))])
        query += ';\n'
       
        return query

    @staticmethod
    def _generate_delete_query(delete, table, primary_keys):
        query = 'DELETE FROM {table} WHERE '.format(table=table)
        
        if len(primary_keys) == 1:
            query += '{pk} IN ({values});'.format(
                    pk=primary_keys[0],
                    values=', '.join(delete))
            return query
        
        delete = '\n(' + ' AND '.join(
                [' {pk} = {val} '.format(
                    primary_keys[j],
                    delete[j]) for j in range(len(primary_keys))]) + ')'

        query += ' OR '.join(delete) + ';\n'
        
        return query

    @staticmethod
    def generate_update_last_sync_query(current_version):
        query = """
        INSERT INTO replicator_sync (version) VALUES ({version});""".format(
                version=int(current_version))

        return query

    @staticmethod
    def process_result(current_version, is_reinitialize, result, table, primary_keys,
            column_types, format_function):
        columns = None
        primary_keys = list(primary_keys)

        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as sql_file:
            if is_reinitialize:
                sql_file.write('TRUNCATE TABLE {table} CASCADE;\n'.format(table=table))
            for row in result:
                if columns == None:
                    columns = BaseQuery.get_columns(row)
                
                if row.get('SYS_CHANGE_OPERATION', False) == 'I' or is_reinitialize:
                    insert = format_function(row, column_types, columns)
                    sql_file.write(PostgresQuery._generate_insert_query(
                        insert, table, columns))
                elif row['SYS_CHANGE_OPERATION'] == 'U':
                    update = format_function(row, column_types, columns)
                    sql_file.write(PostgresQuery._generate_update_query(
                        update, table, columns, primary_keys))
                else:
                    delete = format_function(row, column_types, primary_keys)
                    sql_file.write(PostgresQuery._generate_delete_query(
                        delete, table, primary_keys))
           
            filename = sql_file.name

        return filename

    @staticmethod
    def combine_sql(file_list, setup_all_tables_query=None, update_last_sync_query=None, chunk_size=1024*1024*10):
        with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.sql') as final_file:
            final_file.write(b'BEGIN;\n')
            if setup_all_tables_query:
                final_file.write(setup_all_tables_query.encode('utf-8'))

            tmp_file_was_deleted = False
            for sql_filename in file_list:
                if not tmp_file_was_deleted:
                    with open(sql_filename, 'rb') as sql_file:
                        shutil.copyfileobj(sql_file, final_file, chunk_size)
                
                if os.path.isfile(sql_filename):
                    os.unlink(sql_filename)
                else:
                    tmp_file_was_deleted = True


            if update_last_sync_query:
                final_file.write(str.encode(update_last_sync_query))

            final_file.write(b'\nCOMMIT;')
            name = final_file.name

        if tmp_file_was_deleted:
            os.unlink(name)
            return False

        return name
