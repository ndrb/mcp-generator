from fastapi import FastAPI, HTTPException, Depends, Header, Query
from pydantic import BaseModel, ValidationError
from typing import Dict, List, Any, Optional
import json
import httpx
import os
import datetime

app = FastAPI(
    title="Model Context Protocol Server for Swagger Petstore",
    description="MCP server generated from OpenAPI spec for Swagger Petstore",
    version="1.0.0"
)

# --- Generated Models ---

class Pet(BaseModel):
    
    id: Optional[int] = None
    
    
    
    name: Optional[str] = None
    
    
    
    status: Optional[str] = None
    
      # Allowed values: ['available', 'pending', 'sold']
    
    
    class Config:
        schema_extra = {
            "example": {
                
                "id": 0
                                  ,
                
                "name": "sample_name",
                
                "status": "available"
                                  
                
            }
        }


# Create a dictionary of model classes for validation
models_dict = {
    
    "Pet": Pet,
    
}

# --- API Configuration ---
class APIConfig:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY", "")
        self.base_url = os.environ.get("API_BASE_URL", "https://petstore.swagger.io/v2")
    
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
        headers["api_key"] = api_config.api_key
    
    
    
    
    async with httpx.AsyncClient(base_url=api_config.base_url, headers=headers) as client:
        yield client

# --- MCP Endpoints ---
@app.get("/context")
async def list_models():
    return {
        "models": {
            
            "Pet": {
                "fields": {
                    
                    "id": {
                        "type": "integer",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "name": {
                        "type": "string",
                        "required": False,
                        
                        "description": ""
                    },
                    
                    "status": {
                        "type": "string",
                        "required": False,
                        
                        "enum": ["available", "pending", "sold"],
                        
                        "description": ""
                    }
                    
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