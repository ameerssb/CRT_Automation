# import os
# import asyncio
from metaapi_cloud_sdk import MetaApi
import pandas as pd

token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI4YWRiYzUwYTY0NmU4ZWZiMWQxYzllOTUwMWU0M2I2ZCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6MTk2ZmYyZDUtN2MyYS00YWViLTk3YWQtNzE3NDBhYWUwZDhkIl19LHsiaWQiOiJtZXRhYXBpLXJlc3QtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDoxOTZmZjJkNS03YzJhLTRhZWItOTdhZC03MTc0MGFhZTBkOGQiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjE5NmZmMmQ1LTdjMmEtNGFlYi05N2FkLTcxNzQwYWFlMGQ4ZCJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjE5NmZmMmQ1LTdjMmEtNGFlYi05N2FkLTcxNzQwYWFlMGQ4ZCJdfSx7ImlkIjoibWV0YXN0YXRzLWFwaSIsIm1ldGhvZHMiOlsibWV0YXN0YXRzLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDoxOTZmZjJkNS03YzJhLTRhZWItOTdhZC03MTc0MGFhZTBkOGQiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6MTk2ZmYyZDUtN2MyYS00YWViLTk3YWQtNzE3NDBhYWUwZDhkIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjhhZGJjNTBhNjQ2ZThlZmIxZDFjOWU5NTAxZTQzYjZkIiwiaWF0IjoxNzI2Njc2MzY5fQ.AVMUO5xk8O98ZJ4NM7FtlcY1KacgiNXUDddZ_ZqndL-cwSoJRohqmL9ALG8ghIKD039YN58H0uU2xAjM5wS5qT7-7Eu47EhJS1hAS5FbvlbgOTpOxkkit7IN2nbX4A5Il-b62ICpeUyxMQVkUW0vmJ_yB9reJEj3Ga3jOA2DJVwstDbpb-BbmqxGKFiLx1etHZ2Ux73g1v1E9LLa8tHMnvN2T4Hx8dShaWb0axIQt1WasjcS2FyPgnjUxzNQfZetd1kCKhvqgUZAB5Q1cgYtJCMEPqnSR0sy75dzY6kpzEI_myBNBqJzqmzS9ywefr7dFpWgGNIS-3Dyc5QJTVtPpAZA0JSnnSx26mdk8f5ckfK6ZmHcZRegqatWEQO9BoJgTComqzZAG-151iFEJIv8eCZ1KXyGw_HdYINLtI2eMmt1LmJR7Ef2JYFkGNXjsRakih_zXFRg-COi2G2GYPwtulmy1bCM4-jVXCdQRSipwcPF3H-0RjauIvelMeGKNcamAwUJRSME4cFAVJK0swtQNhOxVs5hCrVaA5LVggotmriWEgLB4d1KYp2iwBcrFYDOi2QIEQk-m4RL-ebBiORNaB7nW1ojHXXPRGB1WFOvuz_Gfvhi2yhdeEYHIMCUWo1A5YGUdgj53JbeiKkbUcTzQCC_hWwAqf2JUltUZlQnhJw'

token = token
login = '179934467'
password = 'Ameer8889@'
server_name = 'Exness-MT5Trial9'


async def meta_api_synchronization(symbol='EURUSDm',timer='4h',candles=3):
    api = MetaApi(token)
    try:
        # Add test MetaTrader account
        accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        account = None
        for item in accounts:
            if item.login == login and item.type.startswith('cloud'):
                account = item
                break
        
	

        print('Waiting for API server to connect to broker (may take couple of minutes)')
        connection = account.get_rpc_connection()

        await connection.connect()
        await connection.wait_synchronized()


	    # Example: Retrieve the last 10 1-hour candles for EURUSD
        history = await account.get_historical_candles(
            symbol, timer, start_time=None, limit=candles
        )
        await connection.close()
        df = pd.DataFrame(history)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        df = df[['open','high','low','close','tickVolume','volume']]

        # print(df)
        return df
        

    except Exception as err:
        # process errors
        if hasattr(err, 'details'):
            # returned if the server file for the specified server name has not been found
            # recommended to check the server name or create the account using a provisioning profile
            if err.details == 'E_SRV_NOT_FOUND':
                print(err)
            # returned if the server has failed to connect to the broker using your credentials
            # recommended to check your login and password
            elif err.details == 'E_AUTH':
                print(err)
            # returned if the server has failed to detect the broker settings
            # recommended to try again later or create the account using a provisioning profile
            elif err.details == 'E_SERVER_TIMEZONE':
                print(err)
        print(api.format_error(err))
    exit()


# df = asyncio.run(meta_api_synchronization())