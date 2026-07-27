# Blinkit Smart Discovery MVP

An AI-powered recommendation prototype that encourages Blinkit users to explore new product categories during checkout.

## Prerequisites
- Python 3.9+
- Node.js (v18+)

## 1. Backend Setup (FastAPI + Groq)

1. Open a terminal and navigate to the project directory:
   ```bash
   cd "c:\Blinkit MVP"
   ```
2. Activate the Python virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\activate
   ```
3. Add your Groq API Key:
   - Open `backend/.env`
   - Replace `your_groq_api_key_here` with your actual Groq API Key. 
   - *(Note: If you don't provide a key, the backend will gracefully fall back to a "Mock Mode" and still function so you can test the UI).*
4. Start the FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The backend will run on `http://localhost:8000`.

## 2. Frontend Setup (Next.js)

1. Open a second terminal and navigate to the frontend directory:
   ```bash
   cd "c:\Blinkit MVP\frontend"
   ```
2. Start the Next.js development server:
   ```bash
   npm run dev
   ```
3. Open the URL provided by Next.js in your browser (usually `http://localhost:3000`).

## 3. How to Test the MVP
1. When you load the frontend, you'll see a simulated "Cart" for a specific user.
2. Use the **"Simulating User" dropdown** at the top to switch between 20 different mock users. This will load different carts (e.g., "Movie Night Snacks", "Baking a cake").
3. Click **Proceed to Pay**. 
4. The Smart Discovery module will pop up. It will:
   - Send the cart and the user's past purchase history to Groq.
   - Groq will analyze the intent, find an unexplored category, and pick a single product.
   - You'll see a personalized, AI-generated explanation for why the product was recommended!

## 4. Deployment Guide

Because this repository contains two separate applications (`backend/` and `frontend/`), you need to deploy them as two separate services and specify their respective root directories.

### Backend Deployment (Railway)
1. Create a new service from the GitHub repository on Railway.
2. **CRITICAL:** Go to Settings -> Build -> **Root Directory** and set it to `/backend`.
3. Ensure the `PORT` environment variable is set or leave default.
4. Add your `GROQ_API_KEY` to the environment variables.

### Frontend Deployment (Vercel or Railway)
1. Create a new Next.js project pointing to the GitHub repository.
2. **CRITICAL:** Set the **Root Directory** to `/frontend`.
3. Add a new environment variable (e.g. `NEXT_PUBLIC_API_URL`) to point to your deployed backend URL so the frontend can communicate with the backend.

*Deployment trigger note updated.*
