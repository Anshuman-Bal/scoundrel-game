import random
from typing import List, Optional, Dict, Any

SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANKS = list(range(2, 11)) + ["J", "Q", "K", "A"]


class Card:
    """Represents a single playing card with Scoundrel-specific attributes."""

    def __init__(self, suit: str, rank, joker_id: Optional[int] = None):
        self.suit = suit
        self.rank = rank
        self.joker_id = joker_id
        self.value = self._determine_value()
        self.type = self._determine_type()

    def _determine_value(self) -> Optional[int]:
        if self.suit == "joker": return None
        if isinstance(self.rank, int): return self.rank
        value_map = {"J": 11, "Q": 12, "K": 13, "A": 14}
        return value_map.get(self.rank)

    def _determine_type(self) -> Optional[str]:
        if self.suit == "joker": return "merchant"
        if self.suit in ("spades", "clubs"): return "monster"
        if self.suit == "diamonds": return "weapon"
        if self.suit == "hearts": return "potion"
        return None

    def short_name(self) -> str:
        if self.suit == "joker": return "Joker"
        return f"{self.rank}{self.suit[0].upper()}"

    def __repr__(self) -> str:
        if self.suit == "joker": return f"Joker ({self.joker_id})"
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
        while len(self.room) < 4 and self.deck:
            self.room.append(self.deck.pop(0))

    def _refill_if_needed(self):
        if len(self.room) <= 1 and self.deck:
            self.can_run = True
            self.draw_room()

    def _card_in_room(self, index: int) -> Card:
        if not (0 <= index < len(self.room)):
            raise IndexError("Card index out of range in room.")
        return self.room[index]
    
    def can_use_weapon_on(self, monster_card: Card) -> bool:
        if not self.weapon or monster_card.type != 'monster':
            return False
        if not self.weapon_slain_values:
            return True
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