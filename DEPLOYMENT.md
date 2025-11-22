# Deployment Guide: Deploying Matic Hub to the Web

While the Matic Hub is designed to be **local-first**, you may want to deploy the dashboard to the public web for remote access or to showcase the project.

> **⚠️ SECURITY WARNING:** Exposing a smart home controller to the public internet carries risks. Ensure you implement authentication (like Basic Auth or OAuth) if you plan to control real hardware remotely.

## Option 1: Render (Easiest for Demo)

Render can host the Python (FastAPI) app directly from your GitHub repository.

1.  **Push your code to GitHub**.
2.  Create a new **Web Service** on Render.
3.  Connect your GitHub repository.
4.  **Build Command:** `pip install -r requirements.txt`
5.  **Start Command:** `uvicorn matic_hub.main:app --host 0.0.0.0 --port $PORT`
6.  **Environment Variables:**
    *   `PYTHON_VERSION`: `3.11.0`

*Note: The MQTT broker (Mosquitto) will NOT run on Render's standard web service. This deployment is best for showcasing the UI/API with mock data.*

## Option 2: VPS (DigitalOcean / AWS / Hetzner)

For a fully functional production deployment including the MQTT broker:

1.  **Provision a VPS** (Ubuntu 22.04 recommended).
2.  **Install Docker & Docker Compose**:
    ```bash
    apt update
    apt install docker.io docker-compose-plugin
    ```
3.  **Clone your repo**:
    ```bash
    git clone https://github.com/yourusername/matic-ha-hub.git
    cd matic-ha-hub
    ```
4.  **Run the stack**:
    ```bash
    docker compose up -d
    ```
5.  **Setup Reverse Proxy (Caddy/Nginx)**:
    Use Caddy for automatic HTTPS.
    ```bash
    # Caddyfile
    your-domain.com {
        reverse_proxy localhost:8080
    }
    ```

## Option 3: Home Assistant Add-on

If you already run Home Assistant OS, you can package this as an Add-on.

1.  Create a `config.json` and `Dockerfile` following HA Add-on standards.
2.  Add the repository to your Home Assistant Add-on Store.
3.  Install and click "Start".

## Accessing Locally (The Intended Way)

Remember, this app shines on your local network!
*   **URL:** `http://home-server-ip:8080`
*   **Tailscale:** Use Tailscale to access it securely from anywhere without opening ports.
