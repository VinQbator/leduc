# leduc
OpenAI Gym environment for Leduc Hold'em

### Rules
+ The deck consists of (J, J, Q, Q, K, K).
+ Each player gets 1 card.
+ There are two betting rounds, and the total number of raises in each round is at most 2.
+ In the second round, one card is revealed on the table and this is used to create a hand.
+ There are two types of hands: pair and highest card.
+ There are three moves: call, raise, and fold.
+ Each of the two players antes 1.
+ In the first round, the betting amount is 2 (including the ante for the first bet). In the second round, it is 4.