import requests
import schedule
import time

from datetime import datetime, timedelta
from config import LOCATIONS, DELTA, WEBHOOK, CHECK_INTERVAL

SCHEDULER_API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start}&endTimestamp={end}'
TTP_TIME_FORMAT = '%Y-%m-%dT%H:%M'

NOTIF_MESSAGE = 'New appointment slot open at {location}: {date}'
MESSAGE_TIME_FORMAT = '%A, %B %d, %Y at %I:%M %p'

def notify_discord(message):
    webhook = WEBHOOK

    data = {
        'content': message
    }
    requests.post(webhook, json=data)

def check_for_openings(location_name, location_code):
    print(f'Checking for openings at {location_name}')
    start = datetime.now()
    end = start + timedelta(weeks=DELTA)

    url = SCHEDULER_API_URL.format(
        location=location_code,
        start=start.strftime(TTP_TIME_FORMAT),
        end=end.strftime(TTP_TIME_FORMAT)
    )
    try:
        response = requests.get(url)
        print('Response status code:', response.status_code)
        results = response.json()
    except requests.ConnectionError:
        print('Could not connect to scheduler API')
    except requests.exceptions.JSONDecodeError:
        print('Failed to decode JSON response')

    for result in results:
        if result['active'] > 0:
            print(f'Opening found for {location_name}')

            timestamp = datetime.strptime(result['timestamp'], TTP_TIME_FORMAT)
            message = NOTIF_MESSAGE.format(
                location=location_name,
                date=timestamp.strftime(MESSAGE_TIME_FORMAT)
            )

            print('Sending to discord: ' + message)
            notify_discord(message)

    print('No openings for {}'.format(location_name))


def main():
    print(f'Starting checks (locations: {len(LOCATIONS)})')
    for location_name, location_code in LOCATIONS:
        check_for_openings(location_name, location_code)

if __name__ == '__main__':
    print('Application started')
    locations_list = ''.join([f'{name}, ' for name, code in LOCATIONS])
    notify_discord(f'Application started. \nChecking for appointments every {CHECK_INTERVAL} minutes at {locations_list}')
    main()
    schedule.every(CHECK_INTERVAL).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)