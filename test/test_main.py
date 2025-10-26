import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# Path to a small test video
TEST_VIDEO = "sample_video/testvideo.mp4"

def test_homepage():
    """Test if the homepage loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Dance Movement Analysis" in response.text

def test_analyze_video():
    """Test the /analyze endpoint with a video file"""
    if not os.path.exists(TEST_VIDEO):
        pytest.skip("Test video not found")

    with open(TEST_VIDEO, "rb") as f:
        response = client.post("/analyze", files={"file": (os.path.basename(TEST_VIDEO), f, "video/mp4")})

    assert response.status_code == 200
    # Check content type of the response
    assert response.headers["content-type"] == "video/mp4"
    # Optionally, save the output to check manually
    with open("test_output.mp4", "wb") as out_file:
        out_file.write(response.content)
