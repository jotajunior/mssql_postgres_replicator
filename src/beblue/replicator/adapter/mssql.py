from beblue.replicator.adapter import BaseQuery
from beblue.replicator import config
import _mssql

class MSSQLQuery:
    @staticmethod
    def setup_all_tables_query(tables, column_types, primary_keys, foreign_keys):
        query = ''
        for table in tables:
            query += MSSQLQuery.setup_table_query(
                    table,
                    column_types[table],
                    primary_keys.get(table, []),
                    foreign_keys)

        return query

    @staticmethod
    def _fix_numeric_precision(precision):
        precision = int(precision)
        scale = precision // 2
        
        return precision + scale, scale
    
    # convert types to Postgres
    @staticmethod
    def convert_column_type(info, skip=['varbinary']):
        if info['type'] in ['varchar', 'nvarchar']:
            if info['length'] != -1:
                _type = '\tvarchar({})'.format(info['length'])
            else:
                _type = '\tvarchar'
        elif info['type'] in ['datetime', 'datetime2', 'time']:
            _type = '\ttimestamp'
        elif info['type'] == 'date':
            _type = '\tdate'
        elif info['type'] == 'int':
            _type = '\tinteger'
        elif info['type'] == 'bigint':
            _type = '\tbigint'
        elif info['type'] == 'float':
            _type = '\treal'
        elif info['type'] == 'decimal':
            precision, scale = MSSQLQuery._fix_numeric_precision(info['precision'])
            _type = '\tnumeric({}, {})'.format(precision, scale)
        elif info['type'] == 'uniqueidentifier':
            _type = '\tvarchar(100)'
        elif info['type'] == 'bit':
            _type = '\tboolean'
        elif info['type'] == 'geography':
            _type = '\tpoint'
        elif info['type'] == 'time':
            _type = '\ttime'
        elif info['type'] in skip:
            _type = False
        else:
            print(info)
            raise Exception('Unknown type caught')

        return _type

    # convert table to Postgres
    @staticmethod
    def setup_table_query(table, column_types, primary_keys, foreign_keys):
        fks = BaseQuery.parse_foreign_keys_for_table_creation(table, foreign_keys) 
        query = 'CREATE TABLE IF NOT EXISTS {table} ('.format(table=table)
        
        for column in column_types:
            info = column_types[column]
            _type = MSSQLQuery.convert_column_type(info)
            if _type == False:
                continue
            is_null = '\tNOT NULL' if info['is_null'] == 'NO' else ''
            suffix = ''
            if column in primary_keys:
                suffix += '\tprimary key'

            if column in fks:
                suffix += '\treferences {}({})'.format(
                        fks[column][0],
                        ', '.join(fks[column][1]))

            query += '\n{column}{_type}{is_null}{suffix},'.format(
                    column=column,
                    _type=_type,
                    is_null=is_null,
                    suffix=suffix)
        query = query[:-1] + '\n);\n\n'

        return query

    # function that formats from MSSQL to Postgres (base format)
    @staticmethod
    def format_values(row, column_types, wanted_columns):
        result = []
        for column in wanted_columns:
            _type = column_types[column]['type']
            value = row[column]
            if value == None:
                to_add = 'NULL'
            elif _type == 'date':
                to_add = value.isoformat()
            elif _type == 'datetime':
                to_add = 'TIMESTAMP ' + \
                        repr(value.isoformat().replace('T', ' ').split('.')[0] + '-03:00')
            elif _type == 'datetime2':
                to_add = 'TIMESTAMP ' + repr(value.split('.')[0] + '-03:00')
            elif _type in ['nvarchar', 'varchar', 'uniqueidentifier']:
                if _type == 'uniqueidentifier':
                    value = str(value)
                value = ''.join(value.split('\x00'))
                to_add = "'{}'".format(value.replace("'", "''"))
            elif _type in ['decimal', 'float']:
                to_add = repr(float(value))
            elif _type in ['int', 'bigint']:
                to_add = repr(int(value))
            elif _type == 'bit':
                to_add = 'TRUE' if value else 'FALSE'
            else:
                print('value: ', value, ', type: ', _type)
                raise Exception('Unknown value {} of type {}'.format(repr(value), type(value)))
            result.append(to_add)

        return result

    @staticmethod
    def get_current_version(conn):
        query = """
        SELECT CHANGE_TRACKING_CURRENT_VERSION()"""
        conn.execute_query(query)
        return [i for i in conn][0][0]

    @staticmethod
    def get_conn():
        conn = _mssql.connect(server=config.database['mssql']['host'],
            user=config.database['mssql']['user'],
            password=config.database['mssql']['password'],
            database=config.database['mssql']['database'],
            )
        return conn

    @staticmethod
    def get_foreign_keys(conn, schema):
        query = """
            SELECT  
                 KCU1.CONSTRAINT_NAME AS FK_CONSTRAINT_NAME 
                ,KCU1.TABLE_NAME AS FOREIGN_TABLE
                ,KCU1.COLUMN_NAME AS FOREIGN_COLUMN 
                ,KCU1.ORDINAL_POSITION AS FK_ORDINAL_POSITION 
                ,KCU2.CONSTRAINT_NAME AS REFERENCED_CONSTRAINT_NAME 
                ,KCU2.TABLE_NAME AS REFERENCED_TABLE 
                ,KCU2.COLUMN_NAME AS REFERENCED_COLUMN
                ,KCU2.ORDINAL_POSITION AS REFERENCED_ORDINAL_POSITION
                ,KCU1.CONSTRAINT_SCHEMA AS FOREIGN_SCHEMA
                ,KCU2.CONSTRAINT_SCHEMA AS REFERENCED_SCHEMA
            FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS RC 

            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU1 
                ON KCU1.CONSTRAINT_CATALOG = RC.CONSTRAINT_CATALOG  
                AND KCU1.CONSTRAINT_SCHEMA = RC.CONSTRAINT_SCHEMA 
                AND KCU1.CONSTRAINT_NAME = RC.CONSTRAINT_NAME 

            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU2 
                ON KCU2.CONSTRAINT_CATALOG = RC.UNIQUE_CONSTRAINT_CATALOG  
                AND KCU2.CONSTRAINT_SCHEMA = RC.UNIQUE_CONSTRAINT_SCHEMA 
                AND KCU2.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME 
                AND KCU2.ORDINAL_POSITION = KCU1.ORDINAL_POSITION 
        """
        conn.execute_query(query)
        return [i for i in conn\
                if i['FOREIGN_SCHEMA'] == schema and i['REFERENCED_SCHEMA'] == schema]

    @staticmethod
    def get_all_tables(conn, schema):
        query = """
        SELECT * FROM INFORMATION_SCHEMA.Tables WHERE TABLE_SCHEMA='{schema}';
        """.format(schema=schema)
        conn.execute_query(query)
        return set([i['TABLE_NAME'].lower() for i in conn\
                if i['TABLE_TYPE'] == 'BASE TABLE'])


    @staticmethod
    def _format_primary_keys_result(result):
        to_return = {}

        for row in result:
            table = row['TABLE_NAME'].lower()
            column = row['COLUMN_NAME'].lower()
            
            if table not in to_return:
                to_return[table] = set()

            to_return[table].add(column)

        return to_return

    @staticmethod
    def get_all_columns(conn, schema):
        columns = {}
        column_types = {}

        query = """
        SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA='{schema}'""".format(schema=schema)
        conn.execute_query(query)

        for row in conn:
            table = row['TABLE_NAME'].lower()
            column = row['COLUMN_NAME'].lower()

            if table not in columns:
                columns[table] = []

            columns[table].append(column)

            if table not in column_types:
                column_types[table] = {}

            if column not in column_types[table]:
                column_types[table][column] = {
                        'type': row['DATA_TYPE'],
                        'is_null': row['IS_NULLABLE'],
                        'length': row['CHARACTER_MAXIMUM_LENGTH'],
                        'precision': row['NUMERIC_PRECISION'],
                        }

        return columns, column_types

    @staticmethod
    def get_primary_keys(conn, schema):
        query = """
        SELECT TABLE_NAME, COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
            AND TABLE_SCHEMA = '{schema}';
        """.format(schema=schema)
        conn.execute_query(query)
        return MSSQLQuery._format_primary_keys_result([i for i in conn])
    
    
    @staticmethod
    def _generate_table_change_query(table, pk_column_name, schema, last_sync, columns, current_sync):
        query = """
        SELECT
            CT.SYS_CHANGE_OPERATION, CT.SYS_CHANGE_VERSION,
            CT.SYS_CHANGE_CREATION_VERSION, {columns} 
        FROM
            {schema}.{table} AS T 
        RIGHT OUTER JOIN 
            CHANGETABLE(CHANGES {schema}.{table}, {last_sync}) AS CT 
        ON 

        """.format(columns=', '.join(['T.{}'.format(i) for i in columns]),
                table=table,
                schema=schema,
                last_sync=last_sync)

        if isinstance(pk_column_name, str):
            query += ' CT.{0} = T.{0} '.format(pk_column_name)
        elif hasattr(pk_column_name, '__iter__'):
            query += ' AND '.join([' CT.{0} = T.{0} '.format(i) for i in pk_column_name])
        else:
            raise TypeError('Iterable or string was expected.')
       
        if current_sync != None:
            query += ' WHERE CT.SYS_CHANGE_VERSION <= {current_sync} '.format(
                    current_sync=current_sync)

        query += ' ORDER BY CT.SYS_CHANGE_VERSION'
        return query

    @staticmethod
    def _generate_table_reinitialization_query(table, schema, columns, force_reinitialize=False):
        query = """
        SELECT
            {columns} 
        FROM 
            {schema}.{table}
        """.format(columns=', '.join(columns),
                table=table,
                schema=schema)
        
        if force_reinitialize:
            query = """
            SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
            BEGIN TRAN
            DECLARE @MinVersion int = CHANGE_TRACKING_MIN_VALID_VERSION(  
                                           OBJECT_ID('{schema}.{table}'))
            SELECT CHANGE_TRACKING_CURRENT_VERSION(), @MinVersion
            {old_query}
            COMMIT TRAN
            """.format(
                    schema=schema,
                    table=table,
                    old_query=query)

        return query

    @staticmethod
    def _generate_sync_table_query(table, pk_column_name, schema, last_sync, columns, current_sync):
        cmd = """
        SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
        BEGIN TRAN
            DECLARE @MinVersion int = CHANGE_TRACKING_MIN_VALID_VERSION(  
                                           OBJECT_ID('{schema}.{table}'))
            SELECT CHANGE_TRACKING_CURRENT_VERSION(), @MinVersion

            IF (@MinVersion > {last_sync})
                {table_reinitialization_query} 
            ELSE
                {table_change_query}
        COMMIT TRAN
        """.format(
                last_sync=last_sync,
                schema=schema,
                table=table,
                table_reinitialization_query=MSSQLQuery._generate_table_reinitialization_query(
                    table, schema, columns),
                table_change_query=MSSQLQuery._generate_table_change_query(
                    table, pk_column_name, schema, last_sync, columns, current_sync),
                )
        return cmd

    @staticmethod
    def sync_table(conn, table, pk_column_name, schema, last_sync, columns, current_sync=None,
            force_reinitialize=False):
        if not force_reinitialize:
            conn.execute_query(MSSQLQuery._generate_sync_table_query(table,
                pk_column_name,
                schema,
                last_sync,
                columns,
                current_sync))
        else:
            conn.execute_query(MSSQLQuery._generate_table_reinitialization_query(
                table,
                schema,
                columns,
                True))

        first_select = [i for i in conn]
        current_version = first_select[0][0]
        is_reinitialize = True if first_select[0][1] > last_sync or force_reinitialize else False

        return current_version, is_reinitialize, conn

    @staticmethod
    def process_result(current_version, is_reinitialize, result):
        print()
        print('Current version for table: ' + str(current_version))
        print('Is reinitialize? ' + str(is_reinitialize))
        print('Loading result...')
        result = [i for i in result]
        print(str(len(result)) + ' results')
        print('Done.')
        print()

    @staticmethod
    def close_conn(conn):
        conn.close()
