from beblue.replicator.parallel.query_thread import QueryThread
from beblue.replicator.parallel.query_sync import QuerySync
from collections import Counter
import os

class UpdateCommand:
    def _build_foreign_keys_graph(self):
        to_return = {}
        for row in self.foreign_keys:
            foreign_table = row['FOREIGN_TABLE'].lower()
            referenced_table = row['REFERENCED_TABLE'].lower()

            if referenced_table not in self.tables or foreign_table not in self.tables:
                continue

            if referenced_table not in to_return:
                to_return[referenced_table] = set()

            to_return[referenced_table].add(foreign_table)
            
        self.graph = to_return
    
    def _build_out_score(self):
        self.out_score = dict([(i, len(self.graph[i])) for i in self.graph])
    
    def _build_in_score(self):
        self.in_score = Counter([j for i in self.graph.items() for j in i[1]])

    def _build_dependencies(self):
        result = {}

        for row in self.foreign_keys:
            foreign_table = row['FOREIGN_TABLE'].lower()
            referenced_table = row['REFERENCED_TABLE'].lower()

            if referenced_table not in self.tables or foreign_table not in self.tables:
                continue

            if foreign_table not in result:
                result[foreign_table] = []

            if referenced_table == foreign_table:
                continue

            if referenced_table not in result[foreign_table]:
                result[foreign_table].append(referenced_table)

        self.dependencies = result

    def _order_candidates(self, candidates):
        eligible_candidates = [
                (i, self.in_score.get(i, 0), self.out_score.get(i, 0))\
                        for i in candidates if not self.dependencies.get(i, False)]
        eligible_candidates.sort(key=lambda i: (i[1], -i[2]))
        return [i[0] for i in eligible_candidates]
    
    def _remove_dependencies(self, remove_list):
        for i in self.dependencies.keys():
            for to_remove in remove_list:
                if to_remove in self.dependencies[i]:
                    self.dependencies[i].remove(to_remove)
    
    def _breadth_first_traversal(self):
        head_tables = self.tables - set(self.in_score.keys())
        order = []
        candidates = self._order_candidates(
                head_tables,
                )
        while len(order) != len(self.tables):
            order += candidates
            self._remove_dependencies(candidates)
            candidates = self._order_candidates(
                    set([j for c in candidates for j in self.graph.get(c, []) if j and j not in order]),
                    )


        return order

    def __init__(self, schema, skip, in_query_cls, out_query_cls, max_conn, tables=None):
        self.query_sync = QuerySync(schema, max_conn, in_query_cls, tables)

        # TODO: Make a way of defining this without this workaround
        # Necessary because MSSQL makes possible multiple primary keys 
        # whether Postgres allows only one. So this was manually set
        self.query_sync.primary_keys['cashbackdailytransactionbycustomer'] = [
                'cashbackdailytransactionbycustomerid']

        self.foreign_keys = self.query_sync.foreign_keys
        self.tables = self.query_sync.all_tables 
        self.out_query_cls = out_query_cls
        self.in_query_cls = in_query_cls
        self.last_sync = self.out_query_cls.get_last_sync()

        self._build_foreign_keys_graph()
        self._build_out_score()
        self._build_in_score()
        self._build_dependencies()
        self.order = self._breadth_first_traversal()
        self.setup_all_tables_query = self.in_query_cls.setup_all_tables_query(
                self.order,
                self.query_sync.column_types,
                self.query_sync.primary_keys,
                self.foreign_keys)
        self.threads = [
                QueryThread(
                    table, 
                    in_query_cls,
                    out_query_cls,
                    self.last_sync,
                    skip.get(table, None),
                    self.query_sync,
                    ) for table in self.order]

    def execute(self):
        if self.last_sync == self.query_sync.current_version:
            print('No change found. Sleeping...')
            return False

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        print(self.query_sync.sql_files)
        files_in_order = [self.query_sync.sql_files[i] for i in self.order]
        last_sync_query = self.out_query_cls.generate_update_last_sync_query(
                self.query_sync.current_version)
        result_filename = self.out_query_cls.combine_sql(files_in_order,
                self.setup_all_tables_query,
                last_sync_query)
        self.out_query_cls.execute_changes(result_filename)
        os.unlink(result_filename)
        return True 
