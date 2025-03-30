from fastapi import FastAPI, HTTPException, Depends, Header, Query
from pydantic import BaseModel, ValidationError
from typing import Dict, List, Any, Optional
import json
import httpx
import os
import datetime

app = FastAPI(
    title="Model Context Protocol Server for OpenWeather API",
    description="MCP server generated from OpenAPI spec for OpenWeather API",
    version="2.5.0"
)

# --- Generated Models ---

class WeatherResponse(BaseModel):
    
    coord: Optional[Dict[str, Any]] = None
    
    
    
    weather: Optional[List[Dict[str, Any]]] = None
    
    
    
    base: Optional[str] = None
      # Internal parameter
    
    
    main: Optional[Dict[str, Any]] = None
    
    
    
    visibility: Optional[int] = None
      # Visibility in meters
    
    
    wind: Optional[Dict[str, Any]] = None
    
    
    
    clouds: Optional[Dict[str, Any]] = None
    
    
    
    rain: Optional[Dict[str, Any]] = None
    
    
    
    snow: Optional[Dict[str, Any]] = None
    
    
    
    dt: Optional[int] = None
      # Time of data calculation, unix, UTC
    
    
    sys: Optional[Dict[str, Any]] = None
    
    
    
    timezone: Optional[int] = None
      # Shift in seconds from UTC
    
    
    id: Optional[int] = None
      # City ID
    
    
    name: Optional[str] = None
      # City name
    
    
    cod: Optional[int] = None
      # Internal parameter
    
    
    
    class Config:
        schema_extra = {
            "example": {
                
                "coord": "sample_coord",
                
                "weather": "sample_weather",
                
                "base": "sample_base",
                
                "main": "sample_main",
                
                "visibility": 0
                                  ,
                
                "wind": "sample_wind",
                
                "clouds": "sample_clouds",
                
                "rain": "sample_rain",
                
                "snow": "sample_snow",
                
                "dt": 0
                                  ,
                
                "sys": "sample_sys",
                
                "timezone": 0
                                  ,
                
                "id": 0
                                  ,
                
                "name": "sample_name",
                
                "cod": 0
                                  
                
            }
        }

class ForecastResponse(BaseModel):
    
    cod: Optional[str] = None
      # Internal parameter
    
    
    message: Optional[float] = None
      # Internal parameter
    
    
    cnt: Optional[int] = None
      # Number of timestamps returned
    
    
    list: Optional[List[Dict[str, Any]]] = None
    
    
    
    city: Optional[Dict[str, Any]] = None
    
    
    
    
    class Config:
        schema_extra = {
            "example": {
                
                "cod": "sample_cod",
                
                "message": 0.0
                                  ,
                
                "cnt": 0
                                  ,
                
                "list": "sample_list",
                
                "city": "sample_city"
                
            }
        }

class GeocodingResponse(BaseModel):
    
    
    class Config:
        schema_extra = {
            "example": {
                
            }
        }


# Create a dictionary of model classes for validation
models_dict = {
    
    "WeatherResponse": WeatherResponse,
    
    "ForecastResponse": ForecastResponse,
    
    "GeocodingResponse": GeocodingResponse,
    
}

# --- API Configuration ---
class APIConfig:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY", "")
        self.base_url = os.environ.get("API_BASE_URL", "https://api.openweathermap.org/data/2.5")
    
    def update(self, api_key=None, base_url=None):
        if api_key:
            self.api_key = api_key
        if base_url:
            self.base_url = base_url

api_config = APIConfig()

# --- API Client ---
async def get_api_client():
    headers = {}
    
    # Add security headers
    
    
    if api_config.api_key:
        headers["appid"] = api_config.api_key
    
    
    
    
    async with httpx.AsyncClient(base_url=api_config.base_url, headers=headers) as client:
        yield client

# --- MCP Endpoints ---
@app.get("/context")
async def list_models():
    return {
        "models": {
            
            "WeatherResponse": {
                "fields": {
                    
                    "coord": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "weather": {
                        "type": "array",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "base": {
                        "type": "string",
                        "required": False,
                        
                        "description": "Internal parameter"
                    },
                    
                    "main": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "visibility": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "Visibility in meters"
                    },
                    
                    "wind": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "clouds": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "rain": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "snow": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "dt": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "Time of data calculation, unix, UTC"
                    },
                    
                    "sys": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "timezone": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "Shift in seconds from UTC"
                    },
                    
                    "id": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "City ID"
                    },
                    
                    "name": {
                        "type": "string",
                        "required": False,
                        
                        "description": "City name"
                    },
                    
                    "cod": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "Internal parameter"
                    }
                    
                }
            },
            
            "ForecastResponse": {
                "fields": {
                    
                    "cod": {
                        "type": "string",
                        "required": False,
                        
                        "description": "Internal parameter"
                    },
                    
                    "message": {
                        "type": "number",
                        "required": False,
                        
                        "description": "Internal parameter"
                    },
                    
                    "cnt": {
                        "type": "integer",
                        "required": False,
                        
                        "description": "Number of timestamps returned"
                    },
                    
                    "list": {
                        "type": "array",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "city": {
                        "type": "object",
                        "required": False,
                        
                        "description": ""
                    }
                    
                }
            },
            
            "GeocodingResponse": {
                "fields": {
                    
                }
            }
            
        }
    }

@app.post("/validate")
async def validate_model(request: Dict[str, Any]):
    model_name = request.get("model_name")
    data = request.get("data", {})
    
    if not model_name:
        raise HTTPException(status_code=400, detail="model_name is required")
    
    if model_name not in models_dict:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    # Validate the data against the model
    try:
        model_class = models_dict[model_name]
        validated_data = model_class(**data)
        return {"valid": True, "data": validated_data.dict()}
    except ValidationError as e:
        return {"valid": False, "errors": e.errors()}

@app.post("/config")
async def update_config(config: Dict[str, str]):
    api_key = config.get("api_key")
    base_url = config.get("base_url")
    
    api_config.update(api_key=api_key, base_url=base_url)
    
    return {"message": "Configuration updated successfully"}

# --- Health Check ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_configured": bool(api_config.api_key and api_config.base_url)}

# --- Main Entry Point ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)