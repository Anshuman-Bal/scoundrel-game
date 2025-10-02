<div align="center">

🃏 Scoundrel: A Dungeon Crawler Card Game 🃏
An interactive, web-based version of the classic single-player rogue-like card game.

</div>

🎮 Gameplay Screenshot
This version of Scoundrel was built with Python and Streamlit, creating a fully interactive point-and-click experience. Dive into the dungeon, fight monsters, equip weapons, and try to escape with your life!

<!--
TODO:

Take a screenshot of your running application.

Add the image to your repository (e.g., as screenshot.png).

Replace the placeholder URL below with the path to your image.
-->

<p align="center">
<img src="https://www.google.com/search?q=https://via.placeholder.com/800x450.png%3Ftext%3DYour%2BGame%2BScreenshot%2BHere" alt="Scoundrel Gameplay Screenshot" width="80%">
</p>

✨ Core Features
Feature

Description

Interactive UI

A point-and-click interface to fight, equip, drink potions, and run.

Faithful Ruleset

Implements the core Scoundrel rules, including the weapon-diminishing mechanic.

Merchant Variant

Includes the "Merchant" variant using Jokers, allowing you to sell weapons for health.

Real-time Stats

The UI keeps track of your health, weapon, slain monster values, and deck size.

Play Anywhere

Built to be deployed on the web, so you can play without any local installation.

🚀 How to Run Locally
Want to run the game on your own machine? Follow these simple steps.

Prerequisites:

Python 3.9 or higher

Git

Setup Instructions:

Clone the repository:

git clone [https://github.com/your-username/scoundrel-streamlit-game.git](https://github.com/your-username/scoundrel-streamlit-game.git)
cd scoundrel-streamlit-game


Install the required dependencies:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run scoundrel_app.py


The application will open in a new tab in your default web browser!

📂 Project Structure
The project code is cleanly separated into the game engine and the Streamlit user interface for better maintainability.

scoundrel-streamlit-game/
│
├── scoundrel_game/
│   ├── __init__.py         # Makes the folder a Python package
│   └── game_engine.py      # Core game logic (Card and GameState classes)
│
├── cards/
│   └── ... (All card images)
│
├── .gitignore              # Files and folders to be ignored by Git
├── LICENSE                 # MIT License
├── README.md               # You are here!
├── requirements.txt        # Project dependencies
└── scoundrel_app.py        # Main Streamlit UI and app entry point


🙏 Acknowledgements & License
Original Game Design: A huge thank you to Zach Gage and Kurt Bieg for creating the original Scoundrel.

Merchant (Joker) Variant: The idea for this variant was inspired by the Riffle Shuffle and Roll YouTube channel.

Streamlit App: Developed by anshumanbal.com.

This project is distributed under the MIT License. See the LICENSE file for more details.