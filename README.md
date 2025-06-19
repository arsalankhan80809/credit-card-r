# Credit Card Recommendation Agent

A web-based, agent-powered credit card recommendation system for Indian users. Built with Streamlit and LangChain.

Demo video link  https://drive.google.com/file/d/12YqrGpYYB78FeHWV4reboYO7JsW1hH0X/view?usp=drivesdk

## Features
- Conversational Q&A to understand user preferences
- Recommends best-fit Indian credit cards from a curated database
- Shows card images, perks, and reward simulations
- **Summary screen** with user profile and recommendations
- **Compare cards** side-by-side
- **Mobile responsive UI**
- Option to restart the journey

## Agent Flow & Prompt Design
- The agent guides the user through a series of questions:
  1. Monthly income
  2. Spending habits
  3. Preferred benefits
  4. Existing cards (optional)
  5. Credit score (or unknown)
- After collecting answers, the agent filters and ranks cards based on eligibility, benefits, and spending profile.
- Each recommendation includes reasons ("why recommended") and a reward simulation (estimated annual benefit).
- Users can compare selected cards in a table.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   Visit [http://localhost:8501](http://localhost:8501)


## Project Structure
- `app.py` — Main Streamlit app
- `card_data.json` — Credit card database
- `requirements.txt` — Python dependencies
- 

