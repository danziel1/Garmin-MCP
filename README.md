# Garmin MCP Server

An MCP server that connects data from Garmin Connect to MCP clients such as Claude Desktop.

## Current Tools

| Tool | Description |
| --- | --- |
| `get_recent_activities` | Fetches the X most recent activites and returns distance, duration, speed, heart rate, calories, steps, and heart-rate zones. |
| `get_sleep_data` | Fetches sleep data from the X most recent days and returns sleep duration, sleep stages, sleep score, respiration, resting heart rate, and body battery change. |
| `get_heart_rate_data` | Fetches heart rate data from the X most recent days and returns the daily minimum, maximum, resting, and calculated average heart rate. |
| `get_steps_data` | Fetches step data from the X most rercent days and returns daily step totals and distance. |
| `get_stress_data` | Fetches stress data from the X most recent days and returns the daily average and maximum stress levels. |
| `get_vO2_data` | Fetches VO2 max datat from the X most recent days and returns the VO2 max and fitness age for days where Garmin provides the data. |
| `get_calorie_data` | Fetches the calorie data from the X most recent days and returns daily total kilocalories. |
| `get_body_battery_data` | Fetches body battery data from the X most recent days and returns daily body battery charged and drained values. |

All tools accept a `days` argument to specify how many days back to look (includes today). `get_recent_activities` accepts an `amount` argument to fetch a specified number of activities.