import os
import random

# Defining cards
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Creating a deck
deck = [(rank, suit) for rank in ranks for suit in suits]

# Dealing cards
def deal_cards(num_players, num_cards_per_player):
    random.shuffle(deck)
    return [random.sample(deck, num_cards_per_player) for _ in range(num_players)]

# Dealing community cards
def deal_community_cards():
    random.shuffle(deck)
    flop = deck[:3]
    turn = deck[3:4]
    river = deck[4:5]
    return flop, turn, river

# Strength of a player's hand
def evaluate_hand(player_hand, community_cards):
    all_cards = player_hand + community_cards
    # Count the frequency of each rank and suit in the hand
    rank_counts = {rank: 0 for rank in ranks}
    suit_counts = {suit: 0 for suit in suits}
    for rank, suit in all_cards:
        rank_counts[rank] += 1
        suit_counts[suit] += 1

    # Check for flush
    is_flush = any(count >= 5 for count in suit_counts.values())
    # Check for straight
    rank_indices = [ranks.index(rank) for rank, _ in all_cards]
    rank_indices.sort()
    is_straight = any(rank_indices[i:i + 5] == list(range(rank_indices[i], rank_indices[i] + 5)) for i in range(len(rank_indices) - 4))

    # Check for straight flush and royal flush
    if is_flush and is_straight:
        # Find the highest rank in the straight flush
        straight_flush_rank = max(rank for rank, _ in all_cards if rank in ranks[:9])
        # Check for royal flush
        if straight_flush_rank == '10':
            return "Royal Flush", 10
        else:
            return "Straight Flush", straight_flush_rank

    # Four of a kind
    if 4 in rank_counts.values():
        four_of_a_kind_rank = next(rank for rank, count in rank_counts.items() if count == 4)
        return "Four of a Kind", four_of_a_kind_rank

    # Full house
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        three_of_a_kind_rank = next(rank for rank, count in rank_counts.items() if count == 3)
        pair_rank = next(rank for rank, count in rank_counts.items() if count == 2)
        return "Full House", three_of_a_kind_rank

    # Flush
    if is_flush:
        flush_suit = next(suit for suit, count in suit_counts.items() if count >= 5)
        return "Flush", flush_suit

    # Straight
    if is_straight:
        straight_rank = max(rank for rank, _ in all_cards)
        return "Straight", straight_rank

    # Three of a kind
    if 3 in rank_counts.values():
        three_of_a_kind_rank = next(rank for rank, count in rank_counts.items() if count == 3)
        return "Three of a Kind", three_of_a_kind_rank

    # Two pair
    if list(rank_counts.values()).count(2) == 2:
        pair_ranks = [rank for rank, count in rank_counts.items() if count == 2]
        return "Two Pair", max(pair_ranks)

    # One pair
    if 2 in rank_counts.values():
        pair_rank = next(rank for rank, count in rank_counts.items() if count == 2)
        return "One Pair", pair_rank

    # High card
    high_card_rank = max(rank for rank, _ in all_cards)
    return "High Card", high_card_rank

# Determine hand ranking
def hand_ranking(hand):
    rank_order = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }
    return rank_order[hand[0]]

# Main function to run the game
def main():
    num_players = int(input("Enter the number of players: "))
    num_cards_per_player = 2  # Each player gets 2 cards
    players = deal_cards(num_players, num_cards_per_player)
    flop, turn, river = deal_community_cards()
    player_balances = {i + 1: 1000 for i in range(num_players)}  # Player balances

    round_num = 1
    while True:
        print(f"\nRound {round_num}")

        # Betting time
        current_bet = 0
        bets = {player: 0 for player in range(1, num_players + 1)}
        while True:
            for player in range(1, num_players + 1):
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before displaying each player's turn
                print(f"\nRound {round_num}")

                # Display player's hand
                print(f"\nPlayer {player}'s hand:")
                for card in players[player - 1]:
                    print(f"{card[0]} of {card[1]}")

                # Display community cards
                if round_num == 1:
                    print("\nFlop:")
                    for card in flop:
                        print(f"{card[0]} of {card[1]}")
                elif round_num == 2:
                    print("\nTurn:")
                    for card in flop + turn:
                        print(f"{card[0]} of {card[1]}")
                elif round_num == 3:
                    print("\nRiver:")
                    for card in flop + turn + river:
                        print(f"{card[0]} of {card[1]}")

                print(f"\nPlayer {player}'s turn")
                print(f"Current bet: {current_bet}")
                print(f"Your balance: {player_balances[player]}")

                # Makes sure a valid action is written
                while True:
                    action = input("Enter your action (bet, raise, call, fold): ").lower()
                    if action in ["bet", "raise", "call", "fold"]:
                        break
                    else:
                        print("Invalid action. Please enter a valid action.")

                if action == "bet":
                    bet_amount = int(input("Enter your bet amount: "))
                    if bet_amount > player_balances[player]:
                        print("Not enough balance. Try again.")
                        continue
                    if bet_amount < current_bet:
                        print("Bet must be greater than or equal to the current bet. Try again.")
                        continue
                    current_bet = bet_amount
                    bets[player] = bet_amount
                elif action == "raise":
                    raise_amount = int(input("Enter your raise amount: "))
                    if raise_amount > player_balances[player]:
                        print("Not enough balance. Try again.")
                        continue
                    if raise_amount < current_bet:
                        print("Raise amount must be greater than or equal to the current bet. Try again.")
                        continue
                    current_bet += raise_amount
                    bets[player] = current_bet
                elif action == "call":
                    if player_balances[player] < current_bet:
                        print("Not enough balance to call. Try again.")
                        continue
                    bets[player] = current_bet
                elif action == "fold":
                    print("Player folded.")
                    bets[player] = 0

            # Check if all players have either folded or matched the highest bet
            if all(bet == 0 or bet == current_bet for bet in bets.values()):
                break

        print("\nHand evaluation:")
        player_hands = {}
        for player, hand in enumerate(players, start=1):
            player_hands[player] = evaluate_hand(hand, flop + turn + river)
            print(f"Player {player}'s hand: {hand}")
            print(f"Hand strength: {player_hands[player]}")

        # Determine winner
        winning_player = max(player_hands, key=lambda p: hand_ranking(player_hands[p]))
        print(f"\nPlayer {winning_player} wins this round with a {player_hands[winning_player][0]}")

        # Option to end the game
        end_game = input("Do you want to end the game? (yes/no): ").lower()
        if end_game == 'yes':
            print("Game ended.")
            break

        round_num += 1
        if round_num > 3:  # Rounds number, change this if you want more rounds (current: 3 rounds)
            break

if __name__ == "__main__":
    main()
























