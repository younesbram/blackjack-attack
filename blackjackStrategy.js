const blackjackStrategy = require('blackjack-strategy');

const playerCards = process.argv.slice(2, 4).map(Number);
const dealerCard = Number(process.argv[4]);
const handCount = Number(process.argv[5]);
const dealerCheckedBlackjack = process.argv[6] === 'true';
const options = JSON.parse(process.argv[7]);

const action = blackjackStrategy.GetRecommendedPlayerAction(
    playerCards, dealerCard, handCount, dealerCheckedBlackjack, options);

console.log(action);
