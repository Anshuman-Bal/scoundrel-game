import random
import streamlit as st
from typing import List, Optional, Dict, Any

# --- Core Game Logic from scoundrel_engine.py ---
# (with minor modifications for Streamlit integration)

SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANKS = list(range(2, 11)) + ["J", "Q", "K", "A"]


class Card:
    """Represents a single playing card with Scoundrel-specific attributes."""

    def __init__(self, suit: str, rank, joker_id: Optional[int] = None):
        self.suit = suit
        self.rank = rank
        self.joker_id = joker_id  # For distinguishing joker_1.png from joker_2.png
        self.value = self._determine_value()
        self.type = self._determine_type()

    def _determine_value(self) -> Optional[int]:
        """Determines the card's value based on its rank."""
        if self.suit == "joker":
            return None
        if isinstance(self.rank, int):
            return self.rank
        value_map = {"J": 11, "Q": 12, "K": 13, "A": 14}
        return value_map.get(self.rank)

    def _determine_type(self) -> Optional[str]:
        """Determines the card's type (monster, weapon, etc.) based on its suit."""
        if self.suit == "joker":
            return "merchant"
        if self.suit in ("spades", "clubs"):
            return "monster"
        if self.suit == "diamonds":
            return "weapon"
        if self.suit == "hearts":
            return "potion"
        return None

    def short_name(self) -> str:
        """Returns a short, user-friendly name for the card."""
        if self.suit == "joker":
            return "Joker"
        return f"{self.rank}{self.suit[0].upper()}"

    def __repr__(self) -> str:
        """Returns a string representation of the card."""
        if self.suit == "joker":
            return f"Joker ({self.joker_id})"
        return f"{self.rank} of {self.suit}"


class GameState:
    """Manages all the state and rules for a game of Scoundrel."""
    MAX_HEALTH = 20

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.health: int = GameState.MAX_HEALTH
        self.deck: List[Card] = self._build_deck()
        self.discard: List[Card] = []
        self.weapon: Optional[Card] = None
        self.weapon_slain_values: List[int] = []
        self.room: List[Card] = []
        self.last_action: str = "Game started. Welcome to the dungeon!"
        self.can_run: bool = True
        self.draw_room()

    def _build_deck(self) -> List[Card]:
        """Creates and shuffles the initial deck according to Scoundrel rules."""
        deck = []
        for suit in SUITS:
            for rank in RANKS:
                if suit in ("hearts", "diamonds") and rank in ("J", "Q", "K", "A"):
                    continue
                deck.append(Card(suit, rank))
        deck.append(Card("joker", None, joker_id=1))
        deck.append(Card("joker", None, joker_id=2))
        random.shuffle(deck)
        return deck

    def draw_room(self):
        """Draws cards from the deck to fill the room up to 4 cards."""
        while len(self.room) < 4 and self.deck:
            self.room.append(self.deck.pop(0))

    def _refill_if_needed(self):
        """If the room is small, refills it from the deck and re-enables running."""
        if len(self.room) <= 1 and self.deck:
            # A new room is being generated, so the player should be allowed to run from it.
            self.can_run = True
            self.draw_room()

    def _card_in_room(self, index: int) -> Card:
        """Safely gets a card from the room by its index."""
        if not (0 <= index < len(self.room)):
            raise IndexError("Card index out of range in room.")
        return self.room[index]
    
    def can_use_weapon_on(self, monster_card: Card) -> bool:
        """Checks if the current weapon can be used on a specific monster."""
        if not self.weapon or monster_card.type != 'monster':
            return False
        if not self.weapon_slain_values:
            return True  # Weapon is fresh, can be used on anything
        last_killed_value = self.weapon_slain_values[-1]
        return monster_card.value < last_killed_value

    def fight_monster(self, index: int, use_weapon: bool = False) -> None:
        card = self._card_in_room(index)
        if card.type != "monster":
            self.last_action = f"Cannot fight {card}; it is not a monster."
            return

        damage_taken = card.value
        used_weapon = False
        if use_weapon and self.can_use_weapon_on(card):
            used_weapon = True
            damage_taken = max(0, card.value - self.weapon.value)

        self.health -= damage_taken
        self.room.pop(index)
        action = f"Fought {card}"
        if used_weapon:
            action += f" with {self.weapon} (blocked {self.weapon.value})"
            self.weapon_slain_values.append(card.value)
        else:
            action += " barehanded"
        action += f". Took {damage_taken} damage. Health = {self.health}."
        self.last_action = action
        self._refill_if_needed()

    def equip_weapon(self, index: int) -> None:
        card = self._card_in_room(index)
        if card.type != "weapon":
            self.last_action = f"Cannot equip {card}; it is not a weapon."
            return
        if self.weapon:
            self.discard.append(self.weapon)
        self.weapon = self.room.pop(index)
        self.weapon_slain_values = []
        self.last_action = f"Equipped {self.weapon}."
        self._refill_if_needed()

    def drink_potion(self, index: int) -> None:
        card = self._card_in_room(index)
        if card.type != "potion":
            self.last_action = f"Cannot drink {card}; it is not a potion."
            return
        healed = card.value
        old_hp = self.health
        self.health = min(GameState.MAX_HEALTH, self.health + healed)
        self.room.pop(index)
        self.last_action = f"Drank {card}. Health: {old_hp} -> {self.health}."
        self._refill_if_needed()

    def sell_to_merchant(self, index: int) -> None:
        card = self._card_in_room(index)
        if card.type != "merchant":
            self.last_action = f"Card {card} is not a Merchant."
            return
        if not self.weapon:
            self.last_action = "Merchant appears but you have no weapon to sell."
            return
        if self.weapon_slain_values:
            heal = min(self.weapon_slain_values)
        else:
            heal = self.weapon.value
        old_hp = self.health
        self.health = min(GameState.MAX_HEALTH, self.health + heal)
        self.last_action = f"Sold {self.weapon} to Merchant for {heal} HP. Health: {old_hp} -> {self.health}."
        self.weapon = None
        self.weapon_slain_values = []
        self.room.pop(index)
        self._refill_if_needed()

    def run_from_room(self) -> None:
        if not self.can_run:
            self.last_action = "You cannot run twice in a row!"
            return
        random.shuffle(self.room)
        self.deck.extend(self.room)
        self.room = []
        self.draw_room()
        self.last_action = "Ran from the room. A new room is drawn. You cannot run from the next room."
        self.can_run = False

    def is_game_over(self) -> Dict[str, Any]:
        if self.health <= 0:
            return {"over": True, "result": "dead", "message": "You died."}
        if not self.deck and not self.room:
            return {"over": True, "result": "victory", "message": "Dungeon cleared — you win!"}
        return {"over": False}


# --- Streamlit UI and Application Logic ---

def get_card_image_path(card: Card) -> str:
    """Maps a Card object to its corresponding image file path."""
    if card.type == 'merchant':
        return f"cards/joker_{card.joker_id}.png"
    
    rank_map = {
        "J": "jack", "Q": "queen", "K": "king", "A": "ace"
    }
    # Use rank directly if it's a number, otherwise map it from the dictionary
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

#### **Card Types & Values**

* **Monsters (Clubs ♣ & Spades ♠):**
    * These are enemies you must fight.
    * **Value:** Number cards are worth their face value (2-10). Jack is 11, Queen is 12, King is 13, and Ace is 14.

* **Weapons (Diamonds ♦):**
    * Used to reduce the damage you take from monsters.
    * **Value:** Number cards are worth their face value (2-10).
    * You can only have one weapon equipped at a time. Equipping a new one discards the old one.

* **Potions (Hearts ♥):**
    * Drinking a potion restores health equal to its value.
    * **Value:** Number cards are worth their face value (2-10).
    * Your health cannot exceed the maximum of 20.

* **Merchants (Jokers):**
    * Allow you to sell your currently equipped weapon in exchange for health.
    * If the weapon **has not been used** to fight a monster, you gain health equal to its value.
    * If the weapon **has been used**, you gain health equal to the value of the *smallest monster it has defeated*.

---

#### **Gameplay Actions**

1.  **Fighting Monsters:**
    * **Barehanded:** You take damage equal to the monster's full value.
    * **With a Weapon:** The damage you take is the monster's value *minus* your weapon's value.
    * **IMPORTANT WEAPON RULE:** After you defeat a monster with a weapon, that weapon can **only** be used on monsters with a value *strictly smaller* than the one you just defeated.

2.  **Equipping a Weapon:** Select a weapon from the room to equip it.

3.  **Drinking a Potion:** Select a potion from the room to gain health.

4.  **Selling to a Merchant:** If you have a weapon equipped, you can sell it.

5.  **Running from a Room:**
    * You can choose to "run" from the current room. All cards in the room are shuffled and placed at the bottom of the deck. A new room is then drawn.
    * **You cannot run from two rooms in a row.**
""")


# Initialize game state in session
if 'game' not in st.session_state:
    st.session_state.game = GameState()

game = st.session_state.game

# --- Main Page UI Rendering ---

st.title("Scoundrel: A Dungeon Crawler Card Game")

# Credits Expander at the top
with st.expander("Credits"):
    st.markdown("*A Single Player Rogue-like Card Game by* **Zach Gage** and **Kurt Bieg**.")
    st.markdown("*Merchant (Joker) variant idea from* **[Riffle Shuffle and Roll](https://www.youtube.com/@riffleshuffleandroll)**.")
    st.markdown("*Streamlit App by* **[Anshuman Bal](https://anshumanbal.com)**.")

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
    # Create columns for the cards in the room
    cols = st.columns(len(game.room))
    for i, card in enumerate(game.room):
        with cols[i]:
            # Set a fixed width for the card images to make them smaller
            st.image(get_card_image_path(card), caption=repr(card), width=150)

            # Action buttons based on card type
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


