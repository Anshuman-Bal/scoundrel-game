import streamlit as st
from scoundrel_game.game_engine import GameState, Card


# --- Streamlit UI and Application Logic ---

def get_card_image_path(card: Card) -> str:
    """Maps a Card object to its corresponding image file path."""
    if card.type == 'merchant':
        return f"cards/joker_{card.joker_id}.png"
    
    rank_map = {
        "J": "jack", "Q": "queen", "K": "king", "A": "ace"
    }
    rank_str = str(card.rank)
    if card.rank in rank_map:
        rank_str = rank_map[card.rank]
        
    return f"cards/{rank_str}_{card.suit}.png"

st.set_page_config(page_title="Scoundrel", layout="wide")

# --- Sidebar for Rules ---
st.sidebar.title("How to Play")
st.sidebar.markdown("""
### Scoundrel Rules
**Objective:** Clear the entire dungeon deck without letting your health drop to zero.
---
#### **Game Setup**
1.  **Deck:** Start with a standard 52-card deck plus two Jokers.
2.  **Remove Cards:** Before shuffling, remove all **red face cards (King, Queen, Jack)** and **red Aces** from the Hearts and Diamonds suits.
3.  **Health:** Your starting health is **20**.
4.  **The Dungeon:** Shuffle the remaining cards to form the dungeon deck.
5.  **The Room:** Draw the top 4 cards from the deck to form the first "room". A room will always be refilled to 4 cards as long as the deck has cards.
---
#### **Gameplay Actions**
* **Fighting Monsters:** You can fight barehanded (taking full damage) or with a weapon (reducing damage). After using a weapon, it can only be used on monsters with a strictly smaller value.
* **Running from a Room:** You can run from a room, which shuffles its cards back into the deck. **You cannot run from two rooms in a row.**
""")

# Initialize game state in session
if 'game' not in st.session_state:
    st.session_state.game = GameState()

game = st.session_state.game

# --- Main Page UI Rendering ---

st.title("Scoundrel: A Dungeon Crawler Card Game")

with st.expander("Credits"):
    st.markdown("""
    *A Single Player Rogue-like Card Game by* **Zach Gage** and **Kurt Bieg**.
    *Merchant (Joker) variant idea from* **[Riffle Shuffle and Roll](https://www.youtube.com/@riffleshuffleandroll)**.
    *Streamlit App by* **[anshumanbal.com](https://anshumanbal.com)**.
    """)

# Game Over Screen
game_over_info = game.is_game_over()
if game_over_info["over"]:
    st.header("Game Over!")
    st.subheader(game_over_info["message"])
    st.metric("Final Health", game.health)
    if st.button("Start New Game"):
        st.session_state.game = GameState()
        st.rerun()
    st.stop()

# Top Status Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Health", f"{game.health} / {GameState.MAX_HEALTH}")
col2.metric("Cards in Deck", len(game.deck))
weapon_name = repr(game.weapon) if game.weapon else "None"
col3.metric("Weapon", weapon_name)
if game.weapon_slain_values:
    col4.metric("Weapon Slain Values", ", ".join(map(str, game.weapon_slain_values)))
else:
    col4.metric("Weapon Slain Values", "None")

st.markdown("---")
st.subheader("Current Room")

# Room Display and Actions
if not game.room:
    st.write("The room is empty. This shouldn't happen unless you've won!")
else:
    cols = st.columns(len(game.room))
    for i, card in enumerate(game.room):
        with cols[i]:
            st.image(get_card_image_path(card), caption=repr(card), width=150)
            if card.type == 'monster':
                if st.button(f"Fight {card.short_name()} Barehanded", key=f"fight_bare_{i}"):
                    game.fight_monster(i, use_weapon=False)
                    st.rerun()
                if game.can_use_weapon_on(card):
                    if st.button(f"Fight with {game.weapon.short_name()}", key=f"fight_weapon_{i}"):
                        game.fight_monster(i, use_weapon=True)
                        st.rerun()
            elif card.type == 'weapon':
                if st.button(f"Equip {card.short_name()}", key=f"equip_{i}"):
                    game.equip_weapon(i)
                    st.rerun()
            elif card.type == 'potion':
                if st.button(f"Drink {card.short_name()}", key=f"drink_{i}"):
                    game.drink_potion(i)
                    st.rerun()
            elif card.type == 'merchant':
                if st.button(f"Sell to Merchant", key=f"sell_{i}", disabled=(not game.weapon)):
                    game.sell_to_merchant(i)
                    st.rerun()

st.markdown("---")

# General Actions and Log
bottom_col1, bottom_col2 = st.columns([1, 3])
with bottom_col1:
    st.subheader("Actions")
    if st.button("Run From Room", disabled=not game.can_run):
        game.run_from_room()
        st.rerun()
with bottom_col2:
    st.subheader("Last Action")
    st.info(game.last_action)