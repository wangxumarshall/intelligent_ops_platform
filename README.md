# Full-Stack Application with FastAPI Backend and Modern Frontend

This project demonstrates a full-stack application architecture featuring a Python FastAPI backend and a modern JavaScript-based frontend (e.g., Vue.js with Vite), containerized using Docker and orchestrated with Docker Compose. The frontend is designed as a portal for various tools, and the backend is set up to support functionalities like WebSocket communication.

## Features (Current & Planned)

-   **Backend**:
    -   FastAPI for robust and fast API development.
    -   WebSocket endpoint (`/ws`) for real-time communication (basic echo implemented).
    -   Gunicorn with Uvicorn workers for production-ready serving.
    -   Containerized with Docker.
    -   (Planned) LLM integration for intelligent responses.
    -   (Planned) Postgres database integration for data persistence.
-   **Frontend**:
    -   Modern JavaScript framework setup (placeholders for Vue/Vite).
    -   Static assets (HTML, CSS, JS) served by Nginx.
    -   Nginx configured for SPA routing and API proxying.
    -   Containerized with Docker, using a multi-stage build.
    -   Portal-style `index.html` with links to external/internal tools.
-   **Overall**:
    -   Docker Compose for easy multi-container application management.
    -   Separation of concerns between backend and frontend services.

## Project Structure

```
.
├── backend/
│   ├── Dockerfile              # Dockerfile for the FastAPI backend
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── Dockerfile              # Dockerfile for the Nginx + Frontend App
│   ├── nginx.conf              # Nginx configuration for serving frontend and proxying API
│   ├── package.json            # Frontend Node.js dependencies and scripts
│   ├── vite.config.js          # Vite configuration (if using Vite)
│   ├── tailwind.config.js      # Tailwind CSS configuration
│   ├── postcss.config.js       # PostCSS configuration
│   └── src/
│       ├── index.html          # Main HTML file for the frontend portal
│       ├── script.js           # Basic JavaScript for the portal (if any)
│       └── styles.css          # Basic CSS for the portal (if any)
├── docker-compose.yml          # Docker Compose file for orchestrating services
└── README.md                   # This file
```

## Running the Application

There are two primary ways to run this application:

### 1. Running with Docker Compose (Recommended)

This method builds and runs both the backend and frontend services as defined in `docker-compose.yml`. Ensure you have Docker and Docker Compose installed.

1.  **Navigate to the Project Root:**
    Open your terminal in the project root directory (where `docker-compose.yml` is located).

2.  **Build and Run Containers:**
    ```bash
    docker-compose up -d --build
    ```
    -   `--build`: Forces Docker to build the images before starting the containers (useful if you've made changes to Dockerfiles or source code).
    -   `-d`: Runs the containers in detached mode (in the background).

3.  **Accessing the Application:**
    Once the containers are up and running, you should be able to access the frontend portal at:
    `http://localhost` (or `http://<your-docker-host-ip>` if not running locally).

    The Nginx service in the `frontend` container will serve the static portal and proxy any requests starting with `/api/` to the `backend` service. The backend's WebSocket endpoint would be accessible via `ws://localhost/api/ws` (or directly if Nginx is configured for WebSocket proxying on `/ws` which the current `frontend/nginx.conf` does not explicitly detail for `/api/ws` but for `/ws` directly to backend if it were exposed differently). The `frontend/nginx.conf` proxies `/api` to `http://backend:8000`. If `main.py`'s WebSocket is at `/ws`, then it would be `ws://localhost/ws` (if Nginx is configured for that path) or `ws://localhost/api/ws` (if the backend FastAPI app prefixes its routes with `/api`, which it currently doesn't).
    *Note: The current `frontend/nginx.conf` proxies `/api` to `backend:8000`. The FastAPI app in `backend/main.py` has its WebSocket at `/ws`. For the frontend JS to connect to `ws://localhost:8000/ws` (as in `frontend/src/script.js`) when running via Docker Compose, the Nginx proxy in `frontend/nginx.conf` should handle `/ws` path separately or the JS should connect to `/api/ws` if the backend FastAPI app is mounted under `/api` or Nginx rewrites the path.* For simplicity with current setup, direct access to backend port for WebSocket might be easier if not going through the frontend's Nginx, or the frontend Nginx needs a `/ws` location block similar to the `/api` block.

4.  **Stopping the Application:**
    ```bash
    docker-compose down
    ```

### 2. Running Locally (for Development)

This method allows you to run the backend and frontend services directly on your machine, which can be useful for development and debugging.

#### a. Running the Backend (FastAPI)

1.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

2.  **Install Python Dependencies:**
    It's highly recommended to use a Python virtual environment.
    ```bash
    # (Optional) Create and activate a virtual environment:
    # python -m venv venv
    # source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI Application with Gunicorn:**
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
    ```
    The backend API will be available at `http://localhost:8000`. The WebSocket endpoint will be at `ws://localhost:8000/ws`.

#### b. Running the Frontend (Vue/Vite Dev Server)

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js Dependencies:**
    Ensure you have Node.js and npm installed.
    ```bash
    npm install
    ```

3.  **Run the Vite Development Server:**
    ```bash
    npm run dev
    ```
    The Vite development server will typically start on a port like `http://localhost:5173` (check your terminal output). It often includes Hot Module Replacement (HMR) for a better development experience.

    **API Proxying with Vite:** To connect to your locally running backend from the Vite dev server, you'll need to configure proxying in `frontend/vite.config.js`. For example:
    ```javascript
    // frontend/vite.config.js
    export default defineConfig({
      plugins: [vue()],
      server: {
        proxy: {
          '/api': { // Or '/ws' if you want to proxy WebSockets directly
            target: 'http://localhost:8000', // Your local backend URL
            changeOrigin: true,
            // For WebSockets with Vite, you might need:
            // ws: true,
            // rewrite: (path) => path.replace(/^\/api/, '') // If backend doesn't expect /api prefix
          }
        }
      },
      build: {
        outDir: 'dist',
      }
    })
    ```
    Then, in your frontend JavaScript, you would make API calls to `/api/...` or connect WebSockets to `/ws` (or `/api/ws` depending on proxy config). The `frontend/src/script.js` currently uses `ws://localhost:8000/ws`, which would work directly with the local backend without Vite proxying if the browser can access that port.

#### c. Production-like Local Frontend
To test a production-like build of the frontend locally:
1.  Navigate to `frontend/`.
2.  Run `npm run build`. This will generate static assets in `frontend/dist/`.
3.  Serve the `frontend/dist/` directory using a local static file server (like `serve` - `npm install -g serve && serve -s dist`) or configure a local Nginx instance similar to `frontend/nginx.conf` to serve these files and proxy API requests to your local backend running on port 8000.

## Future Development

-   Implement full Postgres database integration for storing chat messages or other application data.
-   Integrate Ollama and Qwen3 (or other LLMs) for intelligent responses within the WebSocket service.
-   Develop a more feature-rich frontend application (e.g., using Vue.js components, Vue Router, state management).
-   Add user authentication and authorization.
-   Enhance logging, monitoring, and error handling.
-   Write comprehensive unit and integration tests.
```
