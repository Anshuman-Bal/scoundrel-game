# Scoundrel: A Dungeon Crawler Card Game 🃏

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive web-based version of the classic single-player rogue-like card game, **Scoundrel**, built with Streamlit. Dive into the dungeon, fight monsters, and try to escape with your life!

---

![Scoundrel Gameplay Demo](https://i.imgur.com/7b2g7fJ.gif) 
*<p align="center">A GIF showing the game in action.</p>*


## ✨ Features

* **Interactive Gameplay:** A point-and-click interface to fight monsters, equip weapons, and drink potions.
* **Faithful Ruleset:** Implements the core rules of Scoundrel, including the weapon-diminishing mechanic.
* **Merchant Variant:** Includes the "Merchant" variant using Jokers, allowing you to sell weapons for health.
* **Clean UI:** A simple and intuitive layout that keeps track of your health, weapon, and deck size in real-time.
* **No Installation Needed:** Play directly in your browser thanks to Streamlit.

---

## 🚀 Live Demo

The game is deployed and ready to play on Streamlit Community Cloud.

**[➡️ Click here to play the game!](https://your-app-url.streamlit.app)** ---

## 🛠️ How to Run Locally

Want to run the game on your own machine? No problem.

**Prerequisites:**
* Python 3.9 or higher
* Git

**Setup Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/scoundrel-streamlit-game.git](https://github.com/your-username/scoundrel-streamlit-game.git)
    cd scoundrel-streamlit-game
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run scoundrel_app.py
    ```
    The app should now be open in your web browser!

---

## 📂 Project Structure

The project is organized into two main parts: the game engine and the Streamlit user interface.