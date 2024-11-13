# SWE-SixFold

**Project:** CineSage  
**Team Members:** Carissa Halim, Demonte Walker, Leo Ding, Mikey Fagan, Selvin Castillo, Trevon Herman

## Table of Contents
- [Project Objectives](#project-objectives)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Deploying to Google Cloud Run](#deploying-to-google-cloud-run)
- [License](#license)

## Project Objectives
CineSage is a movie recommendation app that allows users to explore and discover movies through a simple and interactive interface. It integrates with the OMDb API for movie data and uses Firebase for secure user authentication.

## Features
- **User Authentication**: Secure login and registration managed with Firebase Authentication.
- **Random Movie Finder**: Discover random movies with details fetched from the OMDb API.
- **User-Friendly Interface**: Clean, easy-to-navigate design.
- **Search Functionality**: Search for specific movies using the OMDb API.

## Getting Started

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Firebase account and project](https://firebase.google.com/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Docker](https://docs.docker.com/get-docker/) (for containerized deployment)
- [Flask](https://flask.palletsprojects.com/)

### Environment Variables
To configure Firebase and the OMDb API:
- **GOOGLE_APPLICATION_CREDENTIALS**: Path to your Firebase Service Account Key JSON file.
- **OMDB_API_KEY**: Your OMDb API key.

### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/SWE-SixFold.git
    cd SWE-SixFold
    ```

2. **Create a Virtual Environment and Install Dependencies**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set Environment Variables**
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
    export OMDB_API_KEY="your-omdb-api-key"
    ```

4. **Docker Setup (Optional)**
    - If you prefer Docker, build and run the Docker container:
      ```bash
      docker-compose up --build
      ```

## Project Structure

```plaintext
SWE-SixFold/
├── app/
│   ├── app.py                   # Main Flask application
│   ├── templates/               # HTML templates
│   └── static/                  # Static assets like CSS and JavaScript
├── Dockerfile                   # Dockerfile for building the image
├── requirements.txt             # Python package dependencies
└── README.md                    # Documentation for the project
```

## Usage

## Research/Documentation
 - Sprints
     - Sprint 1:
     - Sprint 2:
     - Sprint 3:
     - Sprint 4:
     - Sprint 5:
 - Research/Resources

## License