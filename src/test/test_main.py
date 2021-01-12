import os
import json
import requests
import uvicorn
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from src.main import app

from src.utils import get_logger

logger = get_logger(__name__)


client = TestClient(app)


def test_read_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_pokemon():
    pokemon_name = 'charizard'
    response = client.get("/pokemon/" + pokemon_name)
    assert response.status_code == 200


