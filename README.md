# Blackjack-Attack

Blackjack-Attack is a sophisticated blackjack strategy and card counting application that leverages several card counting systems to help users practice and refine their blackjack strategy. By utilizing the OpenAI GPT-4 model, it provides nuanced advice based on the user's hand, the dealer's upcard, and the current card counts.

## Features

- **Card Counting Systems**: Implements Omega II, Hi-Lo, and Wong Halves systems.
- **True Count Calculations**: Determines the true count based on the remaining decks and running count.
- **Strategy Guidance**: Provides basic strategy advice using the `blackjackStrategy.js` NodeJS module (with HiLo implemented).
```
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
```
- **Expert Advice with GPT-4**: For each hand, users can opt to receive advanced strategy advice from GPT-4 based on the current card count and true count.
- **Continuous Play Assessment**: Allows users to input new cards as they are dealt and updates strategy and counts in real-time.

## How to Use

1. Clone the repository to your local machine.
2. Ensure you have Node.js installed as the `blackjackStrategy.js` module requires it.
3. Install the required Python libraries by running `pip install -r requirements.txt`.
4. Run the script using `python app.py`.
5. Follow the on-screen prompts to input your cards, the dealer's upcard, and other players' cards.
6. Use the advice provided to make strategic decisions in your blackjack game.

## Future Enhancements & Contributions

Contributions are welcome, especially in the following areas:

- **VisionLM Integration**: Implement VisionLM to read cards as they come out of the shoe and update counts in real-time.
- **User Interface (UI)**: Develop a more user-friendly interface for desktop and mobile use. Probably going to make a webapp that allows pasting of screenshots of games in the future or a realtime VisionLM engine.
- **Strategy Customization**: Allow users to define their own card counting strategies and rules.
- **Statistical Analysis**: Add functionality to track long-term results and analyze statistical outcomes.

## Contributing

If you would like to contribute to the development of Blackjack-Attack, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Younes Brahimi - [@didntdrinkwater](https://twitter.com/didntdrinkwater)

Project Link: [https://github.com/your_username/blackjack-attack](https://github.com/your_username/blackjack-attack)

