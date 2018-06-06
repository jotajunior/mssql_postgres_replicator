from beblue.replicator.command.update import UpdateCommand
from beblue.replicator.adapter import mssql, postgres
import beblue.replicator.config as config
import rollbar
from time import sleep
from slackclient import SlackClient

def _init_rollbar():
    api_key = config.ROLLBAR_API_KEY
    if not api_key:
        print('Rollbar is not configured')
        return False

    rollbar.init(api_key)
    return True

def _init_slack():
    if not config.SLACK_API_KEY:
        return False

    return SlackClient(config.SLACK_API_KEY)

def _send_slack_message(sc, msg):
    if sc == False:
        return

    sc.api_call(
            'chat.postMessage',
            channel='#replicator',
            text=msg,
            username='bot')

def run():
    rollbar_up = _init_rollbar()
    sc = _init_slack()
    last_sync = 0
    last_sync_count = 0

    while True:
        try:
            uc = UpdateCommand(
                    config.master_schema, 
                    config.replica_skip,
                    mssql.MSSQLQuery,
                    postgres.PostgresQuery,
                    config.max_connections,
                    config.whitelisted_tables,
                    )
            # if no change is found, sleep for a while
            if not uc.execute():
                print('no change found')
                sleep(config.no_change_sleep)
            else:
                if last_sync != uc.last_sync:
                    last_sync = uc.last_sync
                    last_sync_count = 0
                else:
                    last_sync_count += 1

                if last_sync_count >= 10 and rollbar_up:
                    rollbar.report_message('Something went wrong with the query')
                    _send_slack_message(sc, '** Replicator stopped! **')

            print('\n'*2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            if rollbar_up:
                rollbar.report_exc_info()
            print(repr(e))
        sleep(config.default_sleep)
