# Garmin MCP Server

An MCP server that connects Garmin Connect health and activity data to MCP clients such as Claude Desktop.

## Current Tools

| Tool | Description |
| --- | --- |
| `get_recent_activities` | Fetches the requested number of recent activities and returns distance, duration, speed, heart rate, calories, steps, and heart-rate zones. |
| `get_sleep_data` | Fetches sleep data for the requested number of recent days and returns sleep duration, sleep stages, sleep score, respiration, resting heart rate, and body battery change. |
| `get_heart_rate_data` | Fetches heart rate data for the requested number of recent days and returns the daily minimum, maximum, resting, and calculated average heart rate. |
| `get_steps_data` | Fetches step data for the requested number of recent days and returns daily step totals and distance. |
| `get_stress_data` | Fetches stress data for the requested number of recent days and returns the daily average and maximum stress levels. |
| `get_vO2_data` | Fetches VO2 max data for the requested number of recent days and returns VO2 max and fitness age for days where Garmin provides the data. |
| `get_calorie_data` | Fetches calorie data for the requested number of recent days and returns daily total kilocalories. |
| `get_body_battery_data` | Fetches body battery data for the requested number of recent days and returns daily body battery charged and drained values. |

All daily tools accept a `days` argument that includes today. `get_recent_activities` accepts an `amount` argument to fetch a specified number of activities.

## Setup

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/).


### 2. Install the requirements

Open a terminal in the project directory and run:

```powershell
python -m pip install -r requirements.txt
```

### 3. Create the `.env` file

Create a file named `.env` in the project directory and add your Garmin Connect login details:

```dotenv
GARMIN_EMAIL=your-garmin-email@example.com
GARMIN_PASSWORD=your-garmin-password
```

### 4. Connect to Claude Desktop

1. Open Claude Desktop and go to **Settings**.
2. Open the **Developer** tab.
3. Select **Edit Config** to open `claude_desktop_config.json`.
4. Add or replace the `mcpServers` section with the following. Replace both paths with the locations of your Python executable and `main.py` file.

```json
{
  "mcpServers": {
    "Garmin": {
      "command": "C:\\path\\to\\python.exe",
      "args": ["C:\\path\\to\\Garmin MCP\\main.py"]
    }
  }
}
```

5. Save the configuration and restart Claude Desktop.