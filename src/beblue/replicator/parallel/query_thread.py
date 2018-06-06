from beblue.replicator.parallel.query_sync import QuerySync
from threading import Thread
from time import sleep

class QueryThread(Thread):
    def __init__(self, table, in_query_cls, out_query_cls, last_sync, skip=None, query_sync=None):
        Thread.__init__(self)
        self.query_sync = QuerySync() if not query_sync else query_sync
        self.in_query_cls = in_query_cls
        self.out_query_cls = out_query_cls
        self.table = table
        self.last_sync = last_sync
        self.in_columns = self.query_sync.get_columns_for_table(self.table)
        if skip:
            self.in_columns -= set(skip)
        self.skip = skip
        self.current_sync = self.query_sync.current_version

    def run(self):
        while not self.query_sync.is_free_to_run(self.table):
            sleep(1)

        
        if not self.query_sync.is_operation_running():
            print('Operation was shut down')
            return False

        print('Running table ' + self.table)
        self.query_sync.conn_lock.acquire()
        conn = self.in_query_cls.get_conn()
        
        ran_successfully = False
        
        current_version, is_reinitialize, result = self.in_query_cls.sync_table(
                conn,
                self.table,
                self.query_sync.get_primary_keys_for_table(self.table),
                self.query_sync.get_schema(),
                self.last_sync,
                self.in_columns,
                self.current_sync,
                self.query_sync.need_to_reinitialize(self.table))

        filename = self.out_query_cls.process_result(
                current_version,
                is_reinitialize,
                result,
                self.table,
                self.query_sync.get_primary_keys_for_table(self.table),
                self.query_sync.column_types[self.table],
                self.in_query_cls.format_values)
        
        if self.query_sync.is_operation_running():
            self.query_sync.add_sql_file(self.table, filename)
            # completed successfully, get out of loop
            ran_successfully = True
            self.query_sync.remove_dependency(self.table)
            self.query_sync.add_reinitialization(self.table, is_reinitialize)
        
        if not ran_successfully:
            self.query_sync.shut_operation_down()

        self.in_query_cls.close_conn(conn)
        self.query_sync.conn_lock.release()
        print('Table {} finished'.format(self.table))
