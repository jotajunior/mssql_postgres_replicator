from threading import RLock, BoundedSemaphore

class QuerySync:
    @staticmethod
    def _build_dependencies(foreign_keys):
        result = {}

        for row in foreign_keys:
            if row['FOREIGN_TABLE'] not in result:
                result[row['FOREIGN_TABLE']] = []

            if row['REFERENCED_TABLE'] == row['FOREIGN_TABLE']:
                continue

            if row['REFERENCED_TABLE'] not in result[row['FOREIGN_TABLE']]:
                result[row['FOREIGN_TABLE']].append(row['REFERENCED_TABLE'])

        return result

    @staticmethod
    def _build_reinitializations(foreign_keys):
        result = {}

        for row in foreign_keys:
            if row['FOREIGN_TABLE'] not in result:
                result[row['FOREIGN_TABLE']] = {}

            if row['REFERENCED_TABLE'] == row['FOREIGN_TABLE']:
                continue

            if row['REFERENCED_TABLE'] not in result[row['FOREIGN_TABLE']]:
                result[row['FOREIGN_TABLE']][row['REFERENCED_TABLE']] = False

        return result

    def add_reinitialization(self, table, reinitialized):
        self.reinitialize_lock.acquire()
        for t in self.reinitializations:
            if table in self.reinitializations[t]:
                self.reinitializations[t][table] = reinitialized
        self.reinitialize_lock.release()

    def need_to_reinitialize(self, table):
        for t in self.reinitializations.get(table, []):
            if self.reinitializations[table][t]:
                return True

        return False

    def is_free_to_run(self, table):
        result = self.dependencies.get(table, False)
        return not result

    def get_primary_keys_for_table(self, table):
        return self.primary_keys[table]

    def get_columns_for_table(self, table):
        return set(self.all_columns[table])

    def get_schema(self):
        return self.schema

    def remove_dependency(self, table):
        self.dep_lock.acquire()
        for i in self.dependencies.keys():
            if table in self.dependencies[i]:
                print('Removed dependency ' + table)
                self.dependencies[i].remove(table)
        self.dep_lock.release()
   
    def add_sql_file(self, table, filename):
        self.sql_files[table] = filename

    def shut_operation_down(self):
        self.shutdown = True

    def is_operation_running(self):
        return not self.shutdown

    def get_sql_files(self):
        return self.sql_files

    def _setup(self):
        self.conn_lock.acquire()
        
        conn = self.query_cls.get_conn()
        foreign_keys = self.query_cls.get_foreign_keys(conn, self.schema)
        self.foreign_keys = foreign_keys
        self.reinitializations = QuerySync._build_reinitializations(
                foreign_keys)
        self.current_version = self.query_cls.get_current_version(conn)
        self.dependencies = QuerySync._build_dependencies(foreign_keys)
        self.primary_keys = self.query_cls.get_primary_keys(conn, self.schema)
        self.all_columns, self.column_types = self.query_cls.get_all_columns(
                        conn,
                        self.schema)

        self.all_tables = self.query_cls.get_all_tables(conn, self.schema) if not self.tables \
                else self.tables
        self.query_cls.close_conn(conn)
        
        self.conn_lock.release()

    def __init__(self, schema=None, max_conn=None, query_cls=None, tables=None):
        self.schema = schema
        self.max_conn = max_conn
        self.query_cls = query_cls
        self.dep_lock = RLock()
        self.reinitialize_lock = RLock()
        self.conn_lock = BoundedSemaphore(value=max_conn)
        self.schema = schema
        self.sql_files = {}
        self.shutdown = False
        self.tables = tables
        self._setup()
