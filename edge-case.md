# Edge Cases: Blinkit Smart Discovery MVP

This document outlines the critical edge cases identified for the AI-powered recommendation system, and how they are handled across the frontend and backend.

## 1. Data & State Anomalies

### 1.1 Empty Cart Checkout
* **Scenario:** A user attempts to trigger the Smart Discovery module with 0 items in their cart.
* **Handling (Frontend):** The "Proceed to Pay" button is disabled if `cart.items.length === 0`. 
* **Handling (Backend):** The `get_recommendation` function will raise an error if the cart payload is empty.

### 1.2 "The Power User" (No Unexplored Categories)
* **Scenario:** A user has purchased from *every single* category in the `product_catalog` historically. The calculation `unexplored = categories - frequent` results in an empty array.
* **Handling (Backend):** 
  ```python
  if not unexplored_categories:
      unexplored_categories = CATEGORIES # Fallback: Treat all categories as valid options
  ```

### 1.3 Brand New User (Cold Start)
* **Scenario:** A user has absolutely no purchase history.
* **Handling (Backend):** The history fetch defaults to an empty set (`history.get("categories", set())`). Consequently, the entire catalog is treated as "unexplored," allowing the AI to recommend purely based on the current cart's intent.

### 1.4 Invalid User ID 
* **Scenario:** The frontend passes a `user_id` that does not exist in the mock JSON databases.
* **Handling (Backend):** `get_recommendation` raises a `ValueError("User data not found")`, which the FastAPI endpoint catches and returns as a standard HTTP `404 Not Found`.

## 2. LLM & AI Engine Anomalies

### 2.1 Groq API Key Missing or Invalid
* **Scenario:** The environment variable `GROQ_API_KEY` is not set, or the key is invalid.
* **Handling (Backend):** The code detects the missing key during initialization and seamlessly switches to a **Mock Mode**. In this mode, it randomly picks an unexplored category and generates a generic placeholder explanation, ensuring the UI flow never breaks for demonstration purposes.

### 2.2 LLM Hallucinations / Invalid JSON Output
* **Scenario:** The Groq LLM ignores the system prompt and returns conversational text instead of the requested strict JSON format (e.g., `{"intent": "...", "recommended_category": "...", "explanation": "..."}`).
* **Handling (Backend):** The `json.loads(response.choices[0].message.content)` call is wrapped in a `try...except` block. If parsing fails due to a hallucination, the backend gracefully falls back to the Mock Mode logic.

### 2.3 LLM Hallucinates a Fake Category
* **Scenario:** The LLM recommends a category that does not actually exist in the Blinkit catalog (e.g., "Space Rockets").
* **Handling (Backend):** After parsing the LLM response, the Python service validates the category:
  ```python
  if rec_category not in CATEGORIES:
      rec_category = random.choice(unexplored_categories)
  ```
  This guarantees the system never attempts to look up a non-existent category.

## 3. Performance & UI Edge Cases

### 3.1 High AI Latency
* **Scenario:** The Groq API takes >3 seconds to respond, which could frustrate a user trying to check out quickly.
* **Handling (Frontend):** Smooth skeleton loaders (`.skeleton-box`, `.skeleton-line`) are immediately displayed when the modal opens, providing visual feedback that something premium is happening. 
* **Future Recommendation:** Implement a strict 1.5-second timeout on the backend API call. If the LLM doesn't respond in time, immediately return a cached recommendation or skip the discovery module to unblock the checkout flow.

### 3.2 Frontend Network Failure
* **Scenario:** The user loses internet connectivity exactly when they click "Proceed to Pay," causing the API call to fail.
* **Handling (Frontend):** The `fetch` catch block logs the error, sets the error state, and the modal immediately calls `onClose()`. The system "fails silently" from the user's perspective, dropping them directly into the standard checkout flow without friction.
