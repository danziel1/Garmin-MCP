import os
from dotenv import load_dotenv
from datetime import date, timedelta

from garminconnect import Garmin
from mcp.server.fastmcp import FastMCP

load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")
client = Garmin(EMAIL, PASSWORD)
client.login()

mcp = FastMCP("Gets information from Garmin Connect")


@mcp.tool()
def get_recent_activities(amount: int) -> list:
    """
    Get the user's most recent Garmin activities.
    Args:
        amount: Number of recent activities to fetch.
    """
    simplified = []
    activities = client.get_activities(0, amount)
    for activity in activities:
        simplified.append({
            "activityName": activity.get("activityName"),
            "activityType": activity.get("activityType", {}).get("typeKey"),
            "distanceKm": round(activity.get("distance", 0) / 1000, 2),
            "durationMinutes": round(activity.get("duration", 0) / 60, 1),
            "elapsedDurationMinutes": round(activity.get("elapsedDuration", 0) / 60, 1),
            "movingDurationMinutes": round(activity.get("movingDuration", 0) / 60, 1),
            "averageSpeedMph": round(activity.get("averageSpeed", 0) * 2.23694, 2),
            "maxSpeedMph": round(activity.get("maxSpeed", 0) * 2.23694, 2),
            "averageHR": activity.get("averageHR"),
            "maxHR": activity.get("maxHR"),
            "calories": activity.get("calories"),
            "steps": activity.get("steps"),
            "avgStrideLengthCm": round(activity.get("avgStrideLength", 0), 1),
            "lapCount": activity.get("lapCount"),
            "heartRateZones": {
                "zone1": activity.get("hrTimeInZone_1"),
                "zone2": activity.get("hrTimeInZone_2"),
                "zone3": activity.get("hrTimeInZone_3"),
                "zone4": activity.get("hrTimeInZone_4"),
                "zone5": activity.get("hrTimeInZone_5")
            },
            "startTimeLocal": activity.get("startTimeLocal"),
            "endTimeGMT": activity.get("endTimeGMT")
        })

    return simplified


@mcp.tool()
def get_sleep_data(days: int) -> list:
    """
    Get the user's recent sleep data.

    Args:
        days: Number of recent days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()

        raw = client.get_sleep_data(day_str)

        daily_sleep = (raw or {}).get("dailySleepDTO", {}) or {}

        simplified.append({
            "date": day_str,
            "sleepTimeMinutes": round(daily_sleep.get("sleepTimeSeconds", 0) / 60, 1) if daily_sleep.get("sleepTimeSeconds") is not None else None,
            "deepSleepMinutes": round(daily_sleep.get("deepSleepSeconds", 0) / 60, 1) if daily_sleep.get("deepSleepSeconds") is not None else None,
            "lightSleepMinutes": round(daily_sleep.get("lightSleepSeconds", 0) / 60, 1) if daily_sleep.get("lightSleepSeconds") is not None else None,
            "remSleepMinutes": round(daily_sleep.get("remSleepSeconds", 0) / 60, 1) if daily_sleep.get("remSleepSeconds") is not None else None,
            "awakeSleepMinutes": round(daily_sleep.get("awakeSleepSeconds", 0) / 60, 1) if daily_sleep.get("awakeSleepSeconds") is not None else None,
            "sleepScore": (daily_sleep.get("sleepScores") or {}).get("overall", {}).get("value"),
            "sleepStartTimestampGMT": daily_sleep.get("sleepStartTimestampGMT"),
            "sleepEndTimestampGMT": daily_sleep.get("sleepEndTimestampGMT"),
            "averageRespiration": raw.get("avgSleepRespirationValue") if raw else None,
            "restingHeartRate": raw.get("restingHeartRate") if raw else None,
            "bodyBatteryChange": raw.get("bodyBatteryChange") if raw else None,
        })

    return simplified

@mcp.tool()
def get_heart_rate_data(days: int) -> list:
    """
    Get the user's heart rate data.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()

        raw = client.get_heart_rates(day_str)
        daily_heart_rate = raw

        heartRates = raw.get("heartRateValues")

        average = 0
        noneCount = 0
        for i in heartRates:
            if (i[1] != None and i[1] != 0): 
                average += i[1]
            else:
                noneCount += 1
        average /= len(heartRates)-noneCount

        simplified.append({
            "date": day_str,
            "maxHeartRate": daily_heart_rate.get("maxHeartRate"),
            "minHeartRate": daily_heart_rate.get("minHeartRate"),
            "restingHeartRate": daily_heart_rate.get("restingHeartRate"),
            "averageHeartRate": average
        })
        
    return simplified


@mcp.tool()
def get_steps_data(days: int) -> list:
    """
    Get the user's steps.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()

        raw = client.get_daily_steps(day_str, day_str)
        simplified.append({
            "date": day_str,
            "totalSteps": raw.get("totalSteps"),
            "totalDistance": raw.get("totalDistance")
        })
        
    return simplified

@mcp.tool()
def get_stress_data(days: int) -> list:
    """
    Get the user's stress data.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()

        raw = client.get_stress_data(day_str)
        simplified.append({
            "date": day_str,
            "maxStressLevel": raw.get("maxStressLevel"),
            "avgStressLevel": raw.get("avgStressLevel")
        })
        
    return simplified


@mcp.tool()
def get_vO2_data(days: int) -> list:
    """
    Get the user's VO2 max data.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()
        raw = client.get_max_metrics(day_str)
        try: # gives error on days with no runs
            simplified.append({
                "date": day_str,
                "vo2MaxPreciseValue": raw.get("vo2MaxPreciseValue"),
                "fitnessAge": raw.get("fitnessAge")
            })
        except:
            pass
    return simplified


@mcp.tool()
def get_calorie_data(days: int) -> list:
    """
    Get the user's calorie data.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()
        raw = client.get_user_summary(day_str)
        simplified.append({
            "date": day_str,
            "totalKilocalories": raw.get("totalKilocalories"),
        })
        
    return simplified

@mcp.tool()
def get_body_battery_data(days: int) -> list:
    """
    Get the user's body battery data.
    
    Args:
        days: Number of days to fetch (including today).
    """
    simplified = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.isoformat()
        raw = client.get_body_battery(day_str)
        simplified.append({
            "date": day_str,
            "charged": raw.get("charged"),
            "drained": raw.get("drained")
        })
        
    return simplified


if __name__ == "__main__":
    print("Registered tools:")
    for tool in mcp._tool_manager._tools:
        print(tool)
    mcp.run()