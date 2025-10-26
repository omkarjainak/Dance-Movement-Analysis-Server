
# Dance Movement Analysis Server

## **Overview**

This project implements a **cloud-based AI/ML server** for analyzing body movements from short dance videos. It uses **Python**, **MediaPipe**, and **OpenCV** to detect body keypoints and generate a video with a **skeleton overlay** showing the dancer’s movements in real time.

The server is **containerized with Docker** and can be deployed on public cloud environments (AWS EC2, GCP Compute Engine, or any VPS).

---

## **Features**

* **Video Upload API:** Users can upload a short dance video for analysis.
* **Pose Detection:** Detects body keypoints using MediaPipe and overlays skeleton on the video.
* **Video Output:** Returns a processed video (`.mp4`) with visualized skeleton movements.
* **Unit Tests:** Tests verify the API endpoints and output correctness.
* **Dockerized:** Fully containerized with all dependencies included.
* **Cloud-ready:** Can be deployed to any Docker-compatible cloud environment.

---

## **Tech Stack**

* **Backend:** Python 3.10, FastAPI
* **Computer Vision:** OpenCV, MediaPipe, Numpy
* **Containerization:** Docker
* **Testing:** Pytest, FastAPI TestClient
* **Cloud Deployment:** AWS EC2 / GCP Compute Engine / VPS
* **Version Control:** GitHub

---

## **Project Structure**

```
dance-movement-analysis/
├── app/
│   ├── main.py                  # FastAPI server with upload & analyze endpoint
│   ├── templates/
│   │   └── index.html           # Upload page template
│── analysis/
│       └── pose_analyzer.py     # Video processing & keypoint detection
├── sample_video/
│   └── testvideo.mp4            # Sample video for testing
├── test/
│   └── test_main.py             # Pytest test scripts
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore
```

---

## **Setup & Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/your-username/dance-movement-analysis.git
cd dance-movement-analysis
```

### **2. Build Docker image**

```bash
docker build -t dance-analyzer .
```

### **3. Run the container locally**

```bash
docker run -d -p 8000:8000 --name dance-analyzer dance-analyzer
```

* The server will be available at: `http://localhost:8000/`

---

## **API Usage**

### **Upload Video via Web Page**

1. Open the browser: `http://localhost:8000/`
2. Select a short dance video (`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`)
3. Click **Upload & Analyze**
4. Processed video will be displayed or available for download

### **API Endpoint**

* **POST** `/analyze` – Accepts video file upload
* **Form Data:** `file` → Video file
* **Response:** `video/mp4` → Processed video with skeleton overlay

**Example using `curl`:**

```bash
curl -X POST -F "file=@sample_video/testvideo.mp4" http://localhost:8000/analyze --output result.mp4
```

---

## **Testing**

* **Run tests locally or inside Docker**:

```bash
# Inside container
PYTHONPATH=. pytest test/test_main.py -v
```

**Tested Scenarios:**

* Homepage load
* Video upload & analysis
* Output file type validation

---

## **Cloud Deployment**

1. Deploy the Docker container to **AWS EC2 / GCP Compute Engine / VPS**
2. Expose port 8000 for public access
3. The `/` endpoint serves a web page for uploading videos
4. The `/analyze` endpoint handles API requests programmatically

> **Note:** Ensure Docker and Python dependencies are installed on the cloud server.

---

## **Thought Process**

1. **Problem:** Enable remote analysis of dance movements for body pose understanding.
2. **Solution:**

   * Use **MediaPipe** for accurate pose/keypoint detection.
   * Overlay skeleton on video using **OpenCV**.
   * Build a **FastAPI server** to handle file uploads and return processed video.
   * Containerize with **Docker** for cloud deployment.
3. **Testing & Validation:** Pytest ensures endpoints work and output is correct.
4. **Deployment:** Docker allows **cross-platform deployment** and simplified cloud hosting.

---





# **Dance Movement Analysis API – Test**

## **1. Overview**

This document explains how to test the FastAPI `/` and `/analyze` endpoints of the **Dance Movement Analysis** application, including:

* Homepage load
* Video analysis endpoint

Tests are written using **pytest** and **FastAPI’s TestClient**.

---

## **2. Test Files**

* `test/test_main.py` – contains automated tests for API endpoints.
* `sample_video/testvideo.mp4` – small video file used for testing `/analyze`.

---

## **3. Test Setup**

### **Requirements**

Ensure the following Python packages are installed:

```
fastapi==0.99.0
uvicorn[standard]==0.22.0
pytest==7.4.0
httpx==0.24.1
python-multipart==0.0.6
opencv-python>=4.8.1
mediapipe==0.10.10
numpy==1.26.0
```

### **Docker Setup**

1. Build the Docker image:

```bash
docker build -t dance-analyzer .
```

2. Run the container:

```bash
docker run -d -p 8000:8000 --name dance-analyzer dance-analyzer
```

3. Enter the container shell:

```bash
docker exec -it dance-analyzer /bin/bash
```

---

## **4. Running Tests**

Inside the container:

```bash
cd /app
PYTHONPATH=. pytest test/test_main.py -v
```

**Notes:**

* `PYTHONPATH=.` ensures Python finds the `app` module.
* Tests are **self-contained** and can be run in any environment where the container runs.

---

## **5. Test Cases**

### **1️⃣ Homepage Load Test**

**File:** `test/test_main.py` → `test_homepage()`

**Purpose:** Verify that the homepage (`/`) loads successfully and contains the text `"Dance Movement Analysis"`.

**Expected Result:**

* HTTP status: 200
* Text contains `"Dance Movement Analysis"`

---

### **2️⃣ Video Analysis Test**

**File:** `test/test_main.py` → `test_analyze_video()`

**Purpose:** Verify `/analyze` endpoint processes an uploaded video and returns a video file.

**Steps:**

1. Opens `sample_video/testvideo.mp4`
2. Sends POST request to `/analyze` with video as `multipart/form-data`
3. Checks response status and content type
4. Saves output as `test_output.mp4` (optional)

**Expected Result:**

* HTTP status: 200
* Response `content-type` is `video/mp4`
* Output video is generated successfully

---

## **6. Troubleshooting**

* **No tests collected:** Ensure test file names start with `test_` and test functions start with `test_`.
* **ModuleNotFoundError:** Use `PYTHONPATH=.` when running pytest inside Docker.
* **Missing test video:** Make sure `sample_video/testvideo.mp4` exists and is mounted in Docker if using volumes.

---


✅ **Test Result Example**

```
test/test_main.py::test_homepage PASSED        [ 50%]
test/test_main.py::test_analyze_video PASSED   [100%]
```

Both tests passed successfully, indicating the API is functioning correctly.

---

