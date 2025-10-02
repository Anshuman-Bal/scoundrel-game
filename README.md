Scoundrel: A Dungeon Crawler Card Game 🃏
An interactive web-based version of the classic single-player rogue-like card game, Scoundrel, built with Streamlit. Dive into the dungeon, fight monsters, and try to escape with your life!

<!--
TODO: REPLACE THIS PLACEHOLDER WITH A REAL SCREENSHOT OR GIF OF YOUR APP!
A great way to get a GIF is to use a free tool like ScreenToGif or Giphy Capture.
-->

<p align="center">A GIF showing the game in action.</p>

✨ Features
Interactive Gameplay: A point-and-click interface to fight monsters, equip weapons, and drink potions.

Faithful Ruleset: Implements the core rules of Scoundrel, including the weapon-diminishing mechanic.

Merchant Variant: Includes the "Merchant" variant using Jokers, allowing you to sell weapons for health.

Clean UI: A simple and intuitive layout that keeps track of your health, weapon, and deck size in real-time.

No Installation Needed: Play directly in your browser thanks to Streamlit.

🛠️ How to Run Locally
Want to run the game on your own machine? No problem.

Prerequisites:

Python 3.9 or higher

Git

Setup Instructions:

Clone the repository:

git clone [https://github.com/your-username/scoundrel-streamlit-game.git](https://github.com/your-username/scoundrel-streamlit-game.git)
cd scoundrel-streamlit-game

Install the dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run scoundrel_app.py

The app should now be open in your web browser!

📂 Project Structure
The project is organized into two main parts: the game engine and the Streamlit user interface.

scoundrel-streamlit-game/
│
├── scoundrel_game/
│   ├── __init__.py         # Makes the folder a Python package
│   └── game_engine.py      # Core game logic (Card and GameState classes)
│
├── cards/
│   └── ... (All card images)
│
├── .gitignore              # Files to be ignored by Git
├── LICENSE                 # MIT License
├── README.md               # You are here!
├── requirements.txt        # Project dependencies
└── scoundrel_app.py        # Main Streamlit UI and app entry point
