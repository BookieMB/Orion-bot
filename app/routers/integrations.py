from fastapi import APIRouter, HTTPException, Query
import requests

router = APIRouter()

@router.get("/weather")
def weather(lat: float = Query(...), lon: float = Query(...)):
    """
    Simple integration example using Open-Meteo (no API key required).
    Call: /integrations/weather?lat=14.5995&lon=120.9842  (Manila)
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m", "forecast_days": 1}
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
