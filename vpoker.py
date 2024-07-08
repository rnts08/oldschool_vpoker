import random
from collections import Counter

# Define card suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a standard deck of 52 cards
deck = [(rank, suit) for suit in suits for rank in ranks]

def deal_hand(deck, num_cards=5):
    return random.sample(deck, num_cards)

def display_hand(hand):
    return ', '.join([f"{rank} of {suit}" for rank, suit in hand])

def get_hand_ranks(hand):
    return [rank for rank, suit in hand]

def get_hand_suits(hand):
    return [suit for rank, suit in hand]

def is_flush(hand):
    suits = get_hand_suits(hand)
    return len(set(suits)) == 1

def is_straight(hand):
    rank_values = sorted(ranks.index(rank) for rank, suit in hand)
    return rank_values == list(range(rank_values[0], rank_values[0] + 5))

def score_hand(hand):
    rank_counts = Counter(get_hand_ranks(hand)).values()
    
    if is_flush(hand) and is_straight(hand):
        return "Straight Flush! You win!", 50
    elif 4 in rank_counts:
        return "Four of a Kind! You win!", 25
    elif 3 in rank_counts and 2 in rank_counts:
        return "Full House! You win!", 9
    elif is_flush(hand):
        return "Flush! You win!", 6
    elif is_straight(hand):
        return "Straight! You win!", 4
    elif 3 in rank_counts:
        return "Three of a Kind! You win!", 3
    elif list(rank_counts).count(2) == 2:
        return "Two Pair! You win!", 2
    elif 2 in rank_counts:
        pairs = [rank for rank, count in Counter(get_hand_ranks(hand)).items() if count == 2]
        if any(rank in pairs for rank in ['Jack', 'Queen', 'King', 'Ace']):
            return "Pair of Jacks or Better! You win!", 1
        else:
            return "Pair! You win!", 1
    else:
        return "No winning hand. Try again!", 0

def double_or_nothing(winnings):
    print("\nWelcome to Double or Nothing!")
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    computer_card = deck.pop()
    computer_value = ranks.index(computer_card[0])
    print(f"Computer's card: {computer_card[0]} of {computer_card[1]}")
    
    while True:
        hidden_cards = deal_hand(deck, 5)
        print("Pick a card (1-5):")
        pick = int(input())
        player_card = hidden_cards[pick - 1]
        player_value = ranks.index(player_card[0])
        print(f"Your card: {player_card[0]} of {player_card[1]}")
        
        if player_value > computer_value:
            winnings *= 2
            print(f"You win! Your new winnings are {winnings}.")
            continue_double = input("Do you want to continue to double or nothing? (yes/no): ").strip().lower()
            if continue_double == 'no' or continue_double == 'n':
                break
            else:
                computer_card = deck.pop()
                computer_value = ranks.index(computer_card[0])
                print(f"Computer's new card: {computer_card[0]} of {computer_card[1]}")
        else:
            print("You lose! You lost all your winnings.")
            winnings = 0
            break
    
    return winnings

def play_video_poker():
    print("Welcome to Video Poker!")
    balance = 100  # Starting balance for the player
    last_bet = 5
    while True:
        print(f"\nYour balance: {balance}")
        
        # Get the bet from the player
        bet = input(f"Enter your bet (default is {last_bet}): ")
        bet = int(bet) if bet.strip() else last_bet
        last_bet = bet
        
        if bet > balance:
            print("You don't have enough balance to place this bet. Try again.")
            continue

        balance -= bet
        
        # Shuffle and deal initial hand
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        hand = deal_hand(deck)
        print("Your hand:", display_hand(hand))
        
        # Ask player which cards to hold
        hold_input = input("Enter the positions (1-5) of the cards you want to hold, separated by spaces: ")
        hold_positions = [int(pos) - 1 for pos in hold_input.split()]
        
        # Draw new cards for positions that are not held
        new_hand = [hand[i] if i in hold_positions else deck.pop() for i in range(5)]
        
        print("Your final hand:", display_hand(new_hand))
        
        # Score the hand
        result, multiplier = score_hand(new_hand)
        winnings = bet * multiplier
        balance += winnings
        print(result)
        print(f"You win {winnings} credits!")
        
        # If player wins, offer double or nothing
        if winnings > 0:
            double_nothing = input("Do you want to play double or nothing? (yes/no): ").strip().lower()
            if double_nothing != 'no' and double_nothing != 'n':
                winnings = double_or_nothing(winnings)
                balance += winnings
        
        # Check if the player wants to continue
        continue_playing = input("Do you want to play another round? (yes/no): ").strip().lower()
        if continue_playing == 'no' or continue_playing == 'n':
            print(f"Thanks for playing! Your final balance is {balance}")
            break

# Run the game
if __name__ == "__main__":
    play_video_poker()
