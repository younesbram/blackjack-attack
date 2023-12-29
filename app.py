import subprocess
import json
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)

# Card Counting Systems Values
omega_ii_values = {"2": 1, "3": 1, "4": 2, "5": 2, "6": 2, "7": 1, "8": 0, "9": -1, "10": -2, "J": -2, "Q": -2, "K": -2, "A": 0}
hi_lo_values = {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0, "10": -1, "J": -1, "Q": -1, "K": -1, "A": -1}
wong_halves_values = {"2": 0.5, "3": 1, "4": 1, "5": 1.5, "6": 1, "7": 0.5, "8": 0, "9": 0, "10": -1, "J": -1, "Q": -1, "K": -1, "A": -1}

def update_counts(card, counts):
    counts['omega_ii'] += omega_ii_values.get(card, 0)
    counts['hi_lo'] += hi_lo_values.get(card, 0)
    counts['wong_halves'] += wong_halves_values.get(card, 0)
    return counts

def calculate_true_count(running_count, decks_remaining):
    return running_count / decks_remaining

def get_blackjack_strategy(player_cards, dealer_card, true_count, options=None):
    if options is None:
        options = {
            "hitSoft17": True,
            "surrender": "late",
            "double": "any",
            "doubleAfterSplit": True,
            "resplitAces": False,
            "offerInsurance": True,
            "numberOfDecks": 6,
            "maxSplitHands": 4,
            "count": {
                "system": "HiLo",
                "trueCount": true_count
            },
            "strategyComplexity": "advanced"
        }

    try:
        result = subprocess.run(
            ["node", "blackjackStrategy.js"] + player_cards + [dealer_card, "1", "false", json.dumps(options)],
            capture_output=True, text=True
        )

        if result.stderr:
            print("Error occurred:", result.stderr)
            return None

        return result.stdout.strip()

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None



def get_gpt4_blackjack_advice(player_cards, dealer_card, basic_strategy_advice, counts, true_counts, decks_remaining):
    player_cards_formatted = ", ".join(player_cards)
    user_message = (
        f"You are an expert helper of blackjack card counting. I am currently at home practicing. "
        f"My cards are: {player_cards_formatted}. The dealer's upcard is: {dealer_card}. "
        f"My basic strategy tells me to: {basic_strategy_advice}. "
        f"My current counts and true counts for various systems are {counts} and {true_counts} respectively. "
        f"The number of decks remaining is {decks_remaining}. "
        f"Please provide concise advice based on each play style from Hi-Lo, Omega II, and Wong Halves. Only give me expert advice and deviations if there are any."
    )

    messages = [
        {"role": "system", "content": "You are an expert blackjack player who read multiple blackjack attack books well versed in deviations from basic strategy according to Hi-Lo, Omega II, and Wong Halves."},
        {"role": "user", "content": user_message}
    ]


    delay_time = 0.01
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.666666666666666666666666666666420,
    )
    generated_text = response.choices[0].message.content

    return generated_text

# Main loop
def main():
    counts = {'omega_ii': 0, 'hi_lo': 0, 'wong_halves': 0}
    initial_decks = 8  # Initial number of decks
    total_decks = initial_decks
    cards_dealt = 0  # Total number of cards dealt

    while True:
        # Input for player and dealer cards
        player_cards = input("Your cards (comma-separated, e.g., '10,A'): ").split(',')
        dealer_card = input("Dealer's upcard: ")

        # Optional input for other players' cards
        other_players_cards = input("Other players' cards (Optional, comma-separated, e.g., '10,J,K'): ")
        other_players_cards = other_players_cards.split(',') if other_players_cards else []

        # Update counts with all involved cards
        all_cards = player_cards + [dealer_card] + other_players_cards
        for card in all_cards:
            counts = update_counts(card, counts)
            cards_dealt += 1

        # Adjusting the total decks based on cards dealt
        total_decks = initial_decks - (cards_dealt / 52)
        total_decks = max(total_decks, 0.5)  # Ensure total decks don't go below 0.5

        true_counts = {key: calculate_true_count(value, total_decks) for key, value in counts.items()}
        
        # Get the Hi-Lo true count for passing to the strategy function
        hi_lo_true_count = true_counts.get('hi_lo', 0)

        # Get the recommended strategy
        strategy = get_blackjack_strategy(player_cards, dealer_card, hi_lo_true_count)
        
        print("\nPlayer Cards: ", player_cards)
        print("Dealer Card: ", dealer_card)
        print("\nRecommended Strategy: ", strategy)
        print(f"Current Counts: {counts}")
        print("True Counts: ", {k: round(v, 2) for k, v in true_counts.items()})
        print(f"Deck Penetration: {100 * (1 - total_decks / initial_decks):.2f}%")
        print(f"Estimated Remaining Decks: {total_decks:.2f}")

         # Ask if the player is still in play and update cards if necessary
        while True:
            in_play = input("Are you still in play? (yes/no): ").strip().lower()
            if in_play == "no":
                break
            new_card = input("Enter the new card you got, or 'none' if you are out of the game: ").strip()
            if new_card.lower() == "none":
                break
            player_cards.append(new_card)
            update_counts(new_card, counts)
            cards_dealt += 1
            # Recalculate total decks and true counts
            total_decks = initial_decks - (cards_dealt / 52)
            total_decks = max(total_decks, 0.5)
            true_counts = {key: calculate_true_count(value, total_decks) for key, value in counts.items()}
            strategy = get_blackjack_strategy(player_cards, dealer_card, hi_lo_true_count)
            print("\nPlayer Cards: ", player_cards)
            print("Dealer Card: ", dealer_card)
            print("\nUpdated Strategy: ", strategy)
            print(f"Updated Current Counts: {counts}")
            print("Updated True Counts: ", {k: round(v, 2) for k, v in true_counts.items()})
            print(f"Updated Deck Penetration: {100 * (1 - total_decks / initial_decks):.2f}%")
            print(f"Updated Estimated Remaining Decks: {total_decks:.2f}")

        if input("Do you want GPT-4 advice? (yes/no) ").lower() == "yes":
            gpt4_advice = get_gpt4_blackjack_advice(player_cards, dealer_card, strategy, counts, true_counts, total_decks)
            print("\nGPT-4 Blackjack Advice: ", gpt4_advice)

         # Ask for new cards dealt in the round
        new_other_players_cards = input("New cards : ").split(',')

        # Update counts with all new cards
        all_new_cards = new_other_players_cards
        for card in all_new_cards:
            if card:  # Only update counts if card input is not empty
                counts = update_counts(card, counts)
                cards_dealt += 1

        # Recalculate total decks and true counts
        total_decks = initial_decks - (cards_dealt / 52)
        total_decks = max(total_decks, 0.5)
        true_counts = {key: calculate_true_count(value, total_decks) for key, value in counts.items()}
        print("\nUpdated Current Counts: ", counts)
        print("Updated True Counts: ", {k: round(v, 2) for k, v in true_counts.items()})
        print(f"Updated Deck Penetration: {100 * (1 - total_decks / initial_decks):.2f}%")
        print(f"Updated Estimated Remaining Decks: {total_decks:.2f}")
        print("\nBet accordingly!")

if __name__ == "__main__":
    main()
