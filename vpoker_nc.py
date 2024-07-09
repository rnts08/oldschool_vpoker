import curses
import random
from collections import Counter

# Define card suits and ranks
suits = ['♠', '♣', '♦', '♥']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Function to deal a poker hand
def deal_hand(deck, num_cards=5):
    return random.sample(deck, num_cards)

# Function to draw a card in curses, dynamically adjusting for terminal width
def draw_card(stdscr, y, x, rank, suit, max_width):
    card_width = 10  # Width of a card (including borders and symbols)
    terminal_width = max_width if max_width > 0 else 80
    card_display_width = min(card_width, terminal_width // 5)  # Calculate display width per card

    # Draw the top line of the card
    stdscr.addstr(y, x, '┌' + '─' * (card_display_width - 2) + '┐')

    # Draw the rank and suit symbol
    stdscr.addstr(y + 1, x, f'│ {rank:<2}{" " * (card_display_width - 4)}│')
    stdscr.addstr(y + 2, x, f'│{" " * ((card_display_width - 4) // 2)}{suit}{" " * ((card_display_width - 4) // 2)}│')
    stdscr.addstr(y + 3, x, f'│{" " * (card_display_width - 4)}│')

    # Draw the bottom line of the card
    stdscr.addstr(y + 4, x, '└' + '─' * (card_display_width - 2) + '┘')

# Function to display the poker hand in curses
def display_poker_hand(stdscr, hand, max_width):
    y, x = 0, 0
    for card in hand:
        draw_card(stdscr, y, x, card[0], card[1], max_width)
        x += 1 + (max_width // 5)  # Move to the next card position

# Function to score the poker hand
def score_hand(hand):
    rank_counts = Counter(rank for rank, suit in hand).values()

    if len(set(suit for rank, suit in hand)) == 1 and \
            sorted(ranks.index(rank) for rank, suit in hand) == list(range(ranks.index(hand[0][0]), ranks.index(hand[0][0]) + 5)):
        return "Straight Flush! You win!", 50
    elif 4 in rank_counts:
        return "Four of a Kind! You win!", 25
    elif 3 in rank_counts and 2 in rank_counts:
        return "Full House! You win!", 9
    elif len(set(suit for rank, suit in hand)) == 1:
        return "Flush! You win!", 6
    elif sorted(ranks.index(rank) for rank, suit in hand) == list(range(ranks.index(hand[0][0]), ranks.index(hand[0][0]) + 5)):
        return "Straight! You win!", 4
    elif 3 in rank_counts:
        return "Three of a Kind! You win!", 3
    elif list(rank_counts).count(2) == 2:
        return "Two Pair! You win!", 2
    elif 2 in rank_counts:
        return "Pair! You win!", 1
    else:
        return "No winning hand. Try again!", 0

# Main function to run the game using curses
def main(stdscr):
    curses.curs_set(0)  # Hide cursor

    # Initialize deck and shuffle
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)

    # Initialize balance and last bet
    balance = 100
    last_bet = 5

    while True:
        stdscr.clear()

        # Get terminal size
        max_y, max_x = stdscr.getmaxyx()

        # Display balance and get bet from player
        stdscr.addstr(0, 0, f"Your balance: {balance}")
        stdscr.addstr(max_y - 1, 0, f"Enter your bet (default is {last_bet}): ")
        stdscr.refresh()
        bet = stdscr.getstr(max_y - 1, 36, 2).decode()
        bet = int(bet) if bet.strip().isdigit() else last_bet
        last_bet = bet

        if bet > balance:
            stdscr.addstr(max_y - 3, 0, "You don't have enough balance to place this bet. Press any key to continue.")
            stdscr.getch()
            continue

        balance -= bet

        # Deal initial hand and display
        hand = deal_hand(deck)
        display_poker_hand(stdscr, hand, max_x)

        # Ask which cards to hold
        stdscr.addstr(max_y - 4, 0, "Enter the positions (1-5) of the cards you want to hold, separated by spaces: ")
        stdscr.refresh()
        hold_positions = list(map(int, stdscr.getstr(max_y - 4, 89, 10).decode().split()))

        # Draw new cards for positions that are not held
        for i in range(5):
            if i not in hold_positions:
                hand[i] = deck.pop()

        # Display final hand
        stdscr.clear()
        display_poker_hand(stdscr, hand, max_x)
        stdscr.refresh()

        # Score the hand
        result, multiplier = score_hand(hand)
        winnings = bet * multiplier
        balance += winnings

        # Print result and update balance
        stdscr.addstr(0, 0, f"Your final hand: {[f'{rank}{suit}' for rank, suit in hand]}")
        stdscr.addstr(max_y - 6, 0, result)
        stdscr.addstr(max_y - 5, 0, f"You win {winnings} credits!")
        stdscr.refresh()

        # Offer double or nothing
        if winnings > 0:
            stdscr.addstr(max_y - 7, 0, "Do you want to play double or nothing? (yes/no): ")
            stdscr.refresh()
            choice = stdscr.getstr(max_y - 7, 43, 3).decode().strip().lower()

            if choice == 'yes' or choice == 'y':
                winnings = double_or_nothing(stdscr, winnings)
                balance += winnings

        # Ask if player wants to continue
        stdscr.addstr(max_y - 8, 0, "Do you want to play another round? (yes/no): ")
        stdscr.refresh()
        choice = stdscr.getstr(max_y - 8, 42, 3).decode().strip().lower()

        if choice == 'no' or choice == 'n':
            stdscr.addstr(max_y - 10, 0, f"Thanks for playing! Your final balance is {balance}. Press any key to exit.")
            stdscr.refresh()
            stdscr.getch()
            break

# Function for double or nothing
def double_or_nothing(stdscr, winnings):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Double or Nothing!")
    stdscr.refresh()

    # Initialize deck and computer's card
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    computer_card = deck.pop()
    computer_value = ranks.index(computer_card[0])

    stdscr.addstr(2, 0, f"Computer's card: {computer_card[0]}{computer_card[1]}")
    stdscr.refresh()

    while True:
        hidden_cards = deal_hand(deck, 5)
        display_poker_hand(stdscr, hidden_cards, curses.COLS)
        stdscr.addstr(6, 0, "Pick a card (1-5): ")
        stdscr.refresh()
        pick = int(stdscr.getstr(6, 19, 1).decode())
        player_card = hidden_cards[pick - 1]
        player_value = ranks.index(player_card[0])

        stdscr.addstr(7, 0, f"Your card: {player_card[0]}{player_card[1]}")
        stdscr.refresh()

        if player_value > computer_value:
            winnings *= 2
            stdscr.addstr(8, 0, f"You win! Your new winnings are {winnings}. Press any key to continue.")
            stdscr.refresh()
            stdscr.getch()
            continue_double = stdscr.getstr(9, 0, 3).decode().strip().lower()
            if continue_double == 'no' or continue_double == 'n':
                break
            else:
                computer_card = deck.pop()
                computer_value = ranks.index(computer_card[0])
                stdscr.addstr(3, 0, f"Computer's new card: {computer_card[0]}{computer_card[1]}")
                stdscr.refresh()
        else:
            stdscr.addstr(8, 0, "You lose! You lost all your winnings. Press any key to continue.")
            stdscr.refresh()
            stdscr.getch()
            winnings = 0
            break

    stdscr.clear()
    return winnings

# Wrapper function to run the game
def run_game():
    curses.wrapper(main)

# Run the game
if __name__ == "__main__":
    run_game()

