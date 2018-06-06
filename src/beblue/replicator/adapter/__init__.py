class BaseQuery:
    @staticmethod
    def parse_foreign_keys_for_table_creation(table, foreign_keys):
        fks = {}
        for i in foreign_keys:
            if i['FOREIGN_TABLE'] != table:
                continue
            
            foreign_column = i['FOREIGN_COLUMN']
            referenced_table = i['REFERENCED_TABLE']
            referenced_column = i['REFERENCED_COLUMN']

            if foreign_column not in fks:
                fks[foreign_column] = [None, []]

            fks[foreign_column][0] = referenced_table
            fks[foreign_column][1].append(referenced_column)

        return fks

    @staticmethod
    def get_columns(row):
        return list(set([i for i in row.keys() if not isinstance(i, int)]) - set(
        ['SYS_CHANGE_VERSION', 'SYS_CHANGE_OPERATION', 'SYS_CHANGE_CREATION_VERSION']))

