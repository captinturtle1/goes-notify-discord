# GOES Notify Discord

This application parses the interview scheduler for Global Entry and notifies you via Discord if there are openings. It checks the available dates within the weeks you specify and sends a notification to your Discord channel.

## Configuration

1. **Update Locations:**
   
   Update `config.py` to add locations of your choosing. You can find the location codes from the [Global Entry Scheduler API](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry). Search for your location and use the `id` field. The string name is only for the message and can be whatever you want.

   Example:
   ```python
   LOCATIONS = [
       ('LAX', 5180),
       ('JFK', 1234),
   ]
   ```

2. **Add Webhook**

    Add your Discord webhook URL. You can get one by following [this guide.](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

    Example:
    ```
    WEBHOOK = 'https://discord.com/api/webhooks/your_webhook_url'
    ```

3. **Other**

    You can also change the DELTA (how many weeks out you want to be notified of an opening) and the CHECK_INTERVAL (interval of the checks in minutes).

    Example:
    ```
    DELTA = 4  # How soon in weeks to alert for appointments
    CHECK_INTERVAL = 10  # Minutes between checks
    ```

## Running the Application

- **Locally**
    1. **Set up virtual environment:**

        Create a virtual environment in the project directory:
        ```
        python -m venv .venv
        ```

    2. **Activate the virtual environment:**

        - On Windows:
            ```
            .\venv\Scripts\activate
            ```
        
        - On macOS/Linux
            ```
            source venv/bin/activate
            ```

    3. **Install dependencies:**
        ```
        pip install -r requirements.txt
        ```

    4. **Run the application**
        ```
        python app.py
        ```

- **Docker**

    To run the application in Docker, use the following commands:

    1. Build the Docker image:
        ```
        docker build -t goes-notify-discord .
        ```

    2. Run the Docker container:
        ```
        docker run -d goes-notify-discord
        ```

## How It Works
1. The application starts and sends a notification to Discord indicating that it has started and will check for appointments.
2. It checks for openings at the specified locations every CHECK_INTERVAL minutes.
3. If an opening is found within the specified DELTA weeks, it sends a notification to Discord with the details.
