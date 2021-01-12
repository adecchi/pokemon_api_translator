"""
@author: Alejandro Decchi
@description:
"""
import httpx
from fastapi import FastAPI
import uvicorn
import json

from src.mapping.mapping import Mapping
from src.utils import get_logger


logger = get_logger(__name__)

app = FastAPI()

__all__ = ["read_status", "read_cache_status", "read_pokemon"]


@app.get("/status")
def read_status():
    return {"status": "ok"}


@app.get("/pokemon/{pokemon_name}")
def read_pokemon(pokemon_name: str):
    try:
        pokemon = Mapping()
        status, result = pokemon.get_pokemon_translation(pokemon_name)
        if status:
            return {"name": pokemon_name, "description": result}
        else:
            if isinstance(result, httpx.Response):
                return {"error": json.loads(result.text), "status_code": result.status_code, "url": result.url}
            else:
                return {"name": pokemon_name, "description": result}
    except Exception as ex:
        logger.error(f"Error calling function get_pokemon_translation for pokemon: {pokemon_name} with error: {ex}")


@app.get("/cache_status")
def read_cache_status():
    cache = Mapping()
    data = cache.cache_status()
    return {"status": data}


if __name__ == "__main__":
    #pass
    uvicorn.run(app, host="0.0.0.0", port=8000)
