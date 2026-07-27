# Implementation Plan: Blinkit Smart Discovery MVP

This document provides a step-by-step implementation plan to build the Smart Discovery MVP, derived from the original problem statement and the architectural plan.

## Phase 1: Project Setup & Data Mocking
**Objective:** Set up the foundational structure and mock the required data sources to simulate the Blinkit environment.

1. **Initialize Backend Structure:**
   - Setup a Python environment.
   - Install required packages: `fastapi`, `uvicorn`, `groq`, `pydantic`.
   - Create directories: `backend/`, `backend/services/`, `backend/data/`.

2. **Generate Synthetic Data (`backend/data/`):**
   - Create a Python script to populate a local SQLite database (`discovery_engine.db`).
   - Mock Blinkit product catalog (categories, items, descriptions, prices).
   - Synthetic customer profiles with exploration scores.
   - Purchase histories showing repetitive buying patterns.
   - Mock active carts representing different shopping intents.

## Phase 2: AI Engine & Backend API
**Objective:** Implement the 10-step AI workflow and expose it via API.

2. **Develop AI Service (`backend/services/ai_service.py`):**
   - Initialize Groq API client.
   - **Data Aggregation:** Functions to query the SQLite database for the catalog, user profile, history, and current cart.
   - **Intent & Gap Analysis:** Prompt Groq to analyze the cart for shopping intent, and cross-reference with purchase history to find categories the user rarely/never buys from.
   - **Recommendation Generation:** Prompt Groq to select *one* product from a *new* category that fits the current intent.
   - **Explanation Generation:** Prompt Groq to output a short, personalized reason (e.g., "Since you're buying flour and sugar for baking, you might want to try our new Silicone Baking Mats from the Kitchenware section!").

2. **Build API Endpoints (`backend/main.py`):**
   - `GET /api/cart/{user_id}`: Retrieves the user's active cart.
   - `POST /api/recommend/{user_id}`: Triggers the `ai_service` workflow and returns the recommendation payload.

## Phase 3: Premium Frontend Interface
**Objective:** Build a visually stunning checkout experience that integrates the recommendation.

1. **Initialize Frontend Repository:**
   - Scaffold a React application using Vite (`npx create-vite-app`).
   - Setup a Vanilla CSS design system focusing on rich aesthetics, sleek dark modes or vibrant brand colors, and smooth micro-animations.

2. **Build UI Components:**
   - **Cart Summary:** Displays current items in the cart.
   - **Smart Discovery Module:** A contextual widget that appears during the checkout flow.
     - Must display: Product Image, Name, Price, and the AI-generated Explanation.
     - Must include actions: "Add to Cart" and "Skip".
     - *Design Note:* Incorporate smooth entry animations and hover states to make it feel premium and engaging.

3. **API Integration:**
   - Connect the React app to the FastAPI backend.
   - Ensure graceful loading states (skeletons/spinners) while the AI generates the recommendation.

## Phase 4: Validation & Polish
**Objective:** Ensure the prototype is production-ready for demonstration.

1. **Workflow Validation:** Test with multiple synthetic profiles to verify the AI consistently suggests logical products from *new* categories.
2. **Aesthetic Polish:** Review the UI against modern web design standards to ensure a "WOW" factor.
3. **Final Delivery:** Document the local setup instructions in a `README.md`.
