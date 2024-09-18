import schedule
import time
import pandas as pd
import smtplib
import ssl
import MetaTrader5 as mt5
import mplfinance as mpf
# import threading
from django.core.management.base import BaseCommand
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from django.utils import timezone

# Initialize the MT5 terminal
if not mt5.initialize():
    print("Failed to initialize MetaTrader5, error code =", mt5.last_error())
    quit()

# Connect to your account
account_number = 179934467  # Replace with your actual account number
server = 'Exness-MT5Trial9'
password = "Ameer8889@"  # Replace with your actual password

authorized = mt5.login(account_number, password, server)
if authorized:
    print(f"Connected to account #{account_number}")
else:
    print(f"Failed to connect to account #{account_number}, error code =", mt5.last_error())

# Dictionary to track detected breakouts for each currency pair
detected_breakouts = {}

# List of currency pairs to check
currency_pairs = ['EURUSDm', 'GBPUSDm', 'USDJPYm', 'AUDUSDm','XAUUSDm','BTCUSDm']


# Define a function to fetch the latest OHLC data from your source (MetaTrader, CSV, API, etc.)
def fetch_latest_data(symbol):
    # Placeholder for fetching data. Replace with actual data fetching logic.
    timeframe = mt5.TIMEFRAME_H4  # Hourly timeframe
    num_candles = 3
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    # Convert MT5 data to DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df.rename(columns={'tick_volume':'volume'},inplace=True)
    return df

# Step 1: Your CRT pattern identification function
def identify_crt(df,pair):
    signals = []

    for i in range(1, len(df)):
        prev_candle = df.iloc[i - 1]
        current_candle = df.iloc[i]

        if current_candle['high'] > prev_candle['high']:
            entry_price = prev_candle['high']
            stoploss = current_candle['high']
            target_1 = (prev_candle['high'] + prev_candle['low']) / 2
            target_2 = prev_candle['low']
            
            signals.append({
                'time': current_candle.name,
                'entry_price': entry_price,
                'stop_loss': stoploss,
                'target_1': target_1,
                'target_2': target_2,
                'position': 'short',
                'pair': pair
            })

        elif current_candle['low'] < prev_candle['low']:
            entry_price = prev_candle['low']
            stoploss = current_candle['low']
            target_1 = (prev_candle['high'] + prev_candle['low']) / 2
            target_2 = prev_candle['high']
            
            signals.append({
                'time': current_candle.name,
                'entry_price': entry_price,
                'stop_loss': stoploss,
                'target_1': target_1,
                'target_2': target_2,
                'position': 'long',
                'pair': pair
            })

    return pd.DataFrame(signals)

# Step 2: Function to send email alerts
def send_email_alert(signal):
    sender_email = "4b6252001@smtp-brevo.com"
    receiver_email = "sanisbature17@gmail.com"
    password = "S9PRq7U2fB3ZgCwA"

    # Setting up the MIME
    message = MIMEMultipart("alternative")
    message["Subject"] = "CRT Pattern Detected for the pair " + signal['pair']
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    CRT Pattern Detected
    Pair: {signal['pair']}
    Entry Price: {signal['entry_price']}
    Stop Loss: {signal['stop_loss']}
    Target 1: {signal['target_1']}
    Target 2: {signal['target_2']}
    Position: {signal['position']}
    Time: {signal['time']}
    """

    part = MIMEText(text, "plain")
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp-relay.brevo.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# Step 3: Function to check data and trigger email alerts
def check_for_crt():
    import django
    django.setup()  # Ensure Django is set up correctly

    # Import your model and function after setup
    from Main.models import Breakout
    # from myapp.utils import check_for_crt

    for pair in currency_pairs:
        df = fetch_latest_data(pair)

        # Check for CRT pattern
        crt_signals = identify_crt(df, pair)

        # If signals are found, send an alert and store the detected breakout time
        if not crt_signals.empty:
            for _, signal in crt_signals.iterrows():
                signal_time = signal['time']

                # Convert naive datetime to timezone-aware datetime
                if timezone.is_naive(signal_time):
                    signal_time = timezone.make_aware(signal_time)
                    
                # Check if the breakout has already been detected for this pair and time
                if not Breakout.objects.filter(currency_pair=pair, breakout_time=signal_time).exists():
                    # Send email alert
                    send_email_alert(signal)

                    # Log the breakout in the database
                    Breakout.objects.create(currency_pair=pair, breakout_time=signal_time, alert_sent=True)
                    
                    print(f"Email sent for {pair} CRT pattern detected at {signal_time}")
                
                else:
                    print('already sent')

def run_crt_checker():
    """Runs the CRT checker in a loop every 5 minutes"""
    print("Checked for CRT breakouts")    
    
    while True:
        check_for_crt()
        time.sleep(300)  # 5-minute interval


class Command(BaseCommand):
    help = 'Run the CRT Checker'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting CRT Checker")
        # Just run the checker directly (no threading here)
        run_crt_checker()