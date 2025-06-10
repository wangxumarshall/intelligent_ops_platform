# FastAPI Chat Application

This is a simple chat application built with FastAPI, Nginx, and potentially integrating with LLM services and a Postgres database.

## Features (Planned)

- Real-time chat using WebSockets.
- LLM integration for intelligent responses (Ollama with Qwen3).
- Chat history storage in a Postgres database.
- Static frontend served by FastAPI and Nginx.

## Project Structure

```
.
├── Dockerfile
├── main.py         # FastAPI application
├── nginx.conf      # Nginx configuration
├── README.md       # This file
├── requirements.txt # Python dependencies
└── static/
    ├── index.html  # Main chat page
    ├── script.js   # Frontend JavaScript
    └── styles.css  # Frontend CSS
```

## Running the Application

There are two primary ways to run this application: using Docker (recommended for ease of deployment) or running the components locally.

### Running with Docker

This method assumes you have Docker installed and running on your system.

1.  **Build the Docker Image:**
    Open your terminal in the project root directory (where the `Dockerfile` is located) and run:
    ```bash
    docker build -t fastapi-chat-app .
    ```

2.  **Run the Docker Container:**
    Once the image is built, you can run it as a container:
    ```bash
    docker run -d -p 80:80 fastapi-chat-app
    ```
    This command runs the container in detached mode (`-d`) and maps port 80 of your host machine to port 80 of the container. You should then be able to access the application at `http://localhost`.

### Running Locally

This method requires you to install and configure the components (Python, Nginx, etc.) directly on your system.

1.  **Install Python Dependencies:**
    Ensure you have Python 3.8+ installed. It's recommended to use a virtual environment.
    Navigate to the project root directory and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` will need to be created and populated with dependencies like `fastapi`, `uvicorn`, `psycopg2-binary`, etc.)*

2.  **Install and Configure Nginx:**
    *   **Installation:**
        The installation process for Nginx varies depending on your operating system.
        -   On Debian/Ubuntu: `sudo apt update && sudo apt install nginx`
        -   On macOS (using Homebrew): `brew install nginx`
        -   For other systems, please refer to the official Nginx documentation.
    *   **Configuration:**
        You need to configure Nginx to proxy requests to the FastAPI application and serve static files.
        A sample `nginx.conf` is provided in this repository. You might need to adapt it and replace the default Nginx configuration or include it in the Nginx sites-available directory.
        Typically, you would copy or symlink your `nginx.conf` to `/etc/nginx/sites-available/fastapi-chat` and then create a symlink in `/etc/nginx/sites-enabled/`.
        Example:
        ```bash
        sudo cp nginx.conf /etc/nginx/sites-available/fastapi-chat
        sudo ln -s /etc/nginx/sites-available/fastapi-chat /etc/nginx/sites-enabled/
        sudo nginx -t # Test configuration
        sudo systemctl restart nginx # or sudo service nginx restart
        ```
        Ensure Nginx is configured to listen on port 80 and proxy to the FastAPI app on port 8000, and serve static files from the `static` directory.

3.  **Run the FastAPI Application:**
    Navigate to the project root directory where `main.py` is located. Run the application using Uvicorn:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    This will start the FastAPI development server. Nginx, listening on port 80, will then forward requests to this server.

## Future Development

-   Implement Postgres database integration for storing chat messages.
-   Integrate Ollama and Qwen3 for LLM-powered chat responses.
-   Develop a more robust frontend.
-   Add user authentication.
