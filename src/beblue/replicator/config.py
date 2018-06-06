import os

database = {
        'mssql': {
            'user': os.environ['MSSQL_DB_USER'],
            'password': os.environ['MSSQL_DB_PASSWORD'],
            'host': os.environ['MSSQL_DB_HOST'],
            'database': os.environ['MSSQL_DB_NAME'],
            'port': os.environ.get('MSSQL_DB_PORT', 1433),
            },
        'postgres': {
            'user': os.environ['POSTGRES_DB_USER'],
            'password': os.environ['POSTGRES_DB_PASSWORD'],
            'host': os.environ['POSTGRES_DB_HOST'],
            'database': os.environ['POSTGRES_DB_NAME'],
            'port': os.environ.get('POSTGRES_DB_PORT', 5432),
            },
        }

max_connections = 21
master_schema = 'dbo'
replica_skip = {
        'clientmerchants': ['thumbnail', 'geog', 'legaltaxname', 'typecompany', 'neighborhood', 'zipcode', 'number', 'softdescriptor', 
            'mccid', 'posquantity', 'contactname'],
        'customers': ['profilephoto', 'resetedpass', 'facebooknewid'],
        'merchantcoverimages': ['image'],
        'merchants': ['thumbnail', 'geog'],
        'cashbackvoucher': ['thumbnail'],
        'cashbackaccount': ['lockedfunds'],
        'marketplaceaccounttransaction': ['saleid'],
        }

#       'marketplaceaccounttransaction': ['paymentid'],
blacklisted_source_tables = set(['cashbackvoucher', 'cashbackvouchercustomer'])
whitelisted_tables = set([
        'cashbackaccount',
        'cashbackaccounttransaction',
        'cashbackaccounttransactiondata',
        'cashbackaccounttransactionmerchant',
        'cashbackaccounttransactionparcel',
        'cashbackaccounttransferer',
        'cashbackdailytransactionbycustomer',
        'cashbackinvitefriends',
        'cashbackinviteredeem',
        'cashbackinvites',
        'cashbacktransactiontype',
        'cashbackvoucher',
        'cashbackvouchercustomer',
        'clientmerchants',
        'clientmerchantscashback',
        'clientmerchantstransactions',
        'customers',
        'establishmentypes',
        'marketplaceaccount',
        'marketplaceaccounttransaction',
        'merchantcoverimages',
        'merchants',
        'merchantsratings',
        'cashbackaccounttransactionrating',
        'cashbackaccounttransactionratingtags',
        'cashbacksurveyquestion',
        'cashbackquestion',
        'cashbacksurvey',
        'cashbacksurveysent',
        'cashbackanswer',
        'marketplacebulkanticipationstransactions',
        ])

no_change_sleep = int(os.environ.get('NO_CHANGE_SLEEP', 20))
default_sleep = int(os.environ.get('DEFAULT_SLEEP', 300))

ROLLBAR_API_KEY = os.environ.get('ROLLBAR_API_KEY', None)
SLACK_API_KEY = os.environ.get('SLACK_API_KEY', None)
