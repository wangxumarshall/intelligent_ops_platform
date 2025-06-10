# Full-Stack Application with FastAPI Backend and Vue/Vite Frontend

This project demonstrates a full-stack application architecture featuring a Python FastAPI backend and a Vue.js/Vite frontend, containerized using Docker and orchestrated with Docker Compose. The backend is structured for modularity, and the frontend provides a modern SPA experience.

## Features (Current & Planned)

-   **Backend**:
    -   FastAPI for robust and fast API development, structured into modules (API endpoints, core logic, DB operations, LLM integration placeholders, services, schemas).
    -   Placeholder WebSocket endpoint for real-time communication.
    -   Gunicorn with Uvicorn workers for production-ready serving.
    -   Configuration management using Pydantic settings and `.env` files.
    -   Containerized with Docker.
    -   (Planned) LLM integration for intelligent responses.
    -   (Planned) Postgres database integration for data persistence.
-   **Frontend**:
    -   Vue.js with Vite for a modern, fast Single Page Application (SPA).
    -   Standardized project structure (`public`, `src/assets`, `src/components`, `src/views`, `src/router`, `src/store`, `src/services`).
    -   Tailwind CSS for utility-first styling.
    -   Static assets served by Nginx in production.
    -   Nginx configured for SPA routing and API proxying to the backend.
    -   Containerized with Docker, using a multi-stage build.
    -   Portal-style `index.html` (now `frontend/public/index.html` as a template for Vue).
-   **Overall**:
    -   Docker Compose for easy multi-container application management.
    -   Separation of concerns between backend and frontend services.
    -   `.env.example` provided for environment variable configuration.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py              # Aggregates v1 routers
│   │   │       └── endpoints/          # API endpoint modules (e.g., health.py)
│   │   │           ├── __init__.py
│   │   │           └── health.py
│   │   ├── core/                     # Core logic, configuration
│   │   │   ├── __init__.py
│   │   │   └── config.py             # Pydantic settings
│   │   ├── db/                       # Database interaction layer
│   │   │   ├── __init__.py
│   │   │   ├── crud/                 # CRUD operations
│   │   │   └── models/               # SQLAlchemy models
│   │   ├── llm/                      # LLM integration
│   │   │   ├── __init__.py
│   │   │   └── clients/              # LLM client implementations
│   │   ├── schemas/                  # Pydantic schemas for request/response validation
│   │   │   └── __init__.py
│   │   ├── services/                 # Business logic services
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── main.py                 # FastAPI application entry point
│   ├── Dockerfile                  # Dockerfile for the FastAPI backend
│   ├── requirements.txt            # Python dependencies
│   └── tests/                      # Backend tests
│       └── __init__.py
├── frontend/
│   ├── public/                     # Static assets served directly by Vite/Nginx
│   │   └── index.html              # Main HTML shell for Vite
│   ├── src/
│   │   ├── assets/                 # Static assets processed by Vite (CSS, images, fonts)
│   │   │   ├── script.js           # Old script (for review)
│   │   │   ├── styles.css          # Old styles (for review)
│   │   │   └── tailwind.css        # Tailwind CSS entry point
│   │   ├── components/             # Reusable Vue components
│   │   ├── router/                 # Vue Router configuration (if used)
│   │   ├── services/               # API service functions
│   │   ├── store/                  # State management (Pinia/Vuex)
│   │   ├── views/                  # Vue components for different pages/routes
│   │   ├── App.vue                 # Root Vue component
│   │   └── main.js                 # Vue application entry point
│   ├── Dockerfile                  # Dockerfile for Nginx + Frontend App (Vue/Vite build)
│   ├── nginx.conf                  # Nginx configuration for serving frontend and proxying API
│   ├── package.json                # Frontend Node.js dependencies and scripts
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── postcss.config.js           # PostCSS configuration
├── .env.example                    # Example environment variables
├── docker-compose.yml              # Docker Compose file for orchestrating services
└── README.md                       # This file
```

## Running the Application

### 1. Running with Docker Compose (Recommended)

This method builds and runs both the backend and frontend services as defined in `docker-compose.yml`.

1.  **Prerequisites:**
    -   Ensure Docker and Docker Compose are installed on your system.

2.  **Environment Configuration:**
    -   Copy the `.env.example` file to `.env` in the project root:
        ```bash
        cp .env.example .env
        ```
    -   Review and update the variables in the `.env` file as needed for your environment (e.g., database credentials if you're connecting to an external DB, though the default Docker setup will use the values for containerized services if applicable). The `backend/app/core/config.py` will load these settings.

3.  **Build and Run Containers:**
    Navigate to the project root directory and run:
    ```bash
    docker-compose up -d --build
    ```
    -   `--build`: Forces Docker to build the images before starting the containers.
    -   `-d`: Runs the containers in detached mode.

4.  **Accessing the Application:**
    Once the containers are up, the frontend should be accessible at `http://localhost`.
    The Nginx service in the `frontend` container serves the Vue app and proxies requests starting with `/api/` to the `backend` service (e.g., `/api/v1/health/ping`).

5.  **Stopping the Application:**
    ```bash
    docker-compose down
    ```

### 2. Running Locally (for Development)

This method allows you to run the backend and frontend services directly on your machine.

#### a. Running the Backend (FastAPI)

1.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

2.  **Environment Configuration (Backend):**
    -   Ensure a `.env` file exists in the project root, or create one in the `backend/` directory if you prefer to manage it separately for local backend runs. `backend/app/core/config.py` is configured to load `.env` from the current working directory of the process. If running `gunicorn` from `backend/`, it will look for `backend/.env`.
    -   Update `.env` with your local database settings, LLM API endpoints, etc.

3.  **Install Python Dependencies:**
    Using a Python virtual environment is highly recommended.
    ```bash
    # python -m venv venv
    # source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Run the FastAPI Application with Gunicorn:**
    From the `backend/` directory:
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app
    ```
    The backend API will be available at `http://localhost:8000`. For example, `http://localhost:8000/api/v1/health/ping`.

#### b. Running the Frontend (Vue/Vite Dev Server)

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js Dependencies:**
    Ensure Node.js and npm (or yarn/pnpm) are installed.
    ```bash
    npm install
    ```

3.  **Run the Vite Development Server:**
    ```bash
    npm run dev
    ```
    The Vite development server will typically start on a port like `http://localhost:5173` (check terminal output).
    It includes Hot Module Replacement (HMR) and will proxy API requests as configured in `frontend/vite.config.js` (e.g., `/api` requests to `http://localhost:8000/api`).

## Future Development

-   Implement full Postgres database integration (models, CRUD operations, migrations).
-   Integrate Ollama and Qwen3 (or other LLMs) for intelligent responses via WebSocket or other API endpoints.
-   Develop a more feature-rich frontend application using Vue components, Vue Router for navigation, and Pinia/Vuex for state management.
-   Add user authentication and authorization.
-   Enhance logging, monitoring, and error handling across services.
-   Write comprehensive unit, integration, and end-to-end tests.
-   Further refine the Nginx configuration for production hardening (SSL, security headers, etc.).
```
