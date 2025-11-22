# 🚀 Deployment Guide

Here is how to deploy your **Matic Home Hub** online so the co-founder can see the demo.

## Option 1: GitHub Pages (Recommended for Demo)

This will host the **Frontend UI** as a static site. The "Demo Mode" we added will automatically simulate robots so the UI looks alive even without a backend.

1.  **Initialize Git** (if you haven't already):
    ```bash
    git init
    git add .
    git commit -m "Initial commit with Matic Hub"
    ```

2.  **Create a Repo on GitHub**:
    *   Go to [GitHub.com/new](https://github.com/new).
    *   Name it `matic-ha-hub`.
    *   Make it **Public**.

3.  **Push Code**:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/matic-ha-hub.git
    git branch -M main
    git push -u origin main
    ```

4.  **Enable Pages**:
    *   Go to your Repo **Settings** > **Pages**.
    *   Under **Build and deployment**, select **Source** -> **Deploy from a branch**.
    *   Select Branch: `main`, Folder: `/docs` (This is important! We created the `docs` folder for this purpose).
    *   Click **Save**.

5.  **Get the Link**:
    *   Wait a minute, and GitHub will give you a link like `https://your-username.github.io/matic-ha-hub`.
    *   **Paste this link into your email draft!**

## Option 2: Running Locally

If you want to use it yourself:
1.  Install Docker Desktop.
2.  Run `docker compose up -d`.
3.  Open `http://localhost:8080`.
