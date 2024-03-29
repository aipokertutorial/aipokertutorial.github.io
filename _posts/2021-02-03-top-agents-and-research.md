---
title: "AIPT Section 5.1: Top Poker Agents -- Top Agents and Research"
date: 2021-02-03
sidebar:
  nav: "nav"
toc: true
toc_sticky: true
toc_label: "TOC"
author_profile: false
---
# Top Poker Agents - Top Agents and Research
The biggest breakthroughs in AI poker primarily came from research groups at Carnegie Mellon University (CMU) and the University of Alberta's Computer Poker Research Group (CPRG). We previously discussed the "Heads-up Limit Hold'em Poker is Solved" paper by the CPRG that came out in 2015 and solved Limit Hold'em Poker with an agent called Cepheus. This was a big result, but most human players play No Limit Hold'em poker, so we focus this section on the most recent important results in no limit: 

1. 2017 DeepStack: Expert-Level Artificial Intelligence in No-Limit Poker by the CPRG (DeepMind)
2. 2018 Superhuman AI for heads-up no-limit poker by CMU (Libratus)
3. 2019 Superhuman AI for multiplayer poker by CMU and Facebook (Pluribus)
4. 2020 Unlocking the Potential of Deep Counterfactual Networks by Minimal AI (Supremus)
5. 2020 Combining Deep Reinforcement Learning and Search for Imperfect-Information Games by Facebook (ReBeL)  -- not yet included 

As agents get stronger and stronger, it will be exciting to see what comes next. 

## [DeepStack](https://www.deepstack.ai/)
In 2017, a new paper called DeepStack was released by DeepMind that showed a
completely new framework for approximately solving poker games and possibly the first to make use of neural networks. Although they claimed that it
was the first NLHE agent to defeat human players with competitions that occurred in late 2016. the selected players were mostly
unknown and at most played 3,000 hands against DeepStack (there was a total of 44,000
hands against 33 players from 17 countries), making this less impressive
than the recent Libratus (CMU agent) victory that had occurred in 2017 in a major AI vs. humans competition against top professionals (see Section 5.2). 

Variance reduction measures were taken, which makes the relatively low sample size more statistically significant -- the AIVAT variance reduction algorithm reduced the standard deviation in the experiments by 85% (see below for more details). However, human players do better after getting used to how opponents play and getting used to the game software/setup, so small hand samples seem biased in favor of the AI agent. 

That said, DeepStack won 49 big blinds per 100 hands, which is an absolutely huge winrate, over four standard deviations from zero. However, I would have been more impressed with a strong, but lower winrate, against professional players over bigger samples. (The players who played against DeepStack did actually consider themselves professionals, but there is a vast difference between top players in the world and average professional players -- I would know!) Players were incentivized with prizes of \\$5,000, \\$2,500, and \\$1,250 to the top three best results. 

The agent effectively solves for actions as the situations arise, rather than solving the
entire tree offline as was the standard paradigm with abstracting the game and solving the abstracted game in full and then translating the solution back to the full game. 

It is made up of three components: "A local strategy computation for
the current public state, depth-limited lookahead using a learned value function, and a
restricted set of lookahead actions", which together describe heuristic search, which is implemented cleverly to work effectively in the imperfect information setting.  

DeepStack uses re-solving to locally solve for strategies as they come up in play. With this technique, the agent is able to avoid abstracting the game because it doesn't need to compute a full strategy in advance, as is standard in CFR implementations, which compute a fixed strategy offline. 

Re-solving is essentially solving locally with a strategy going forward in the game, not taking into account the previous parts of the gam. To re-solve at any public state, DeepStack keeps track of its own range and a vector of
opponent counterfactual values. It does use recursion like CFR, but does not store a
complete strategy prior to play. Instead of abstraction, it uses a neural network to “guess” where each play will end up,
which was trained using a very large amount of random poker hands. This is an interesting technique, but would seem to make the algorithm less generalizable than if it was able to learn completely from scratch as standard CFR methods do. 

It effectively uses a fast
approximation estimate, rather than computing all possibilities beyond a certain depth,
which the paper refers to as what a poker player would call a “gut feeling” or intuition. It also uses action abstraction with only fold, call, 2-3 bet actions, and all-in. The restricted set of lookahead actions are used so that DeepStack can act very fast (normally within about 5 seconds). 

They showed that this agent is significantly less exploitable than the abstraction-based
techniques, which makes sense given how much abstraction is required to reduce No Limit Hold'em to a tractable size. 

### AIVAT Variance Reduction
DeepStack was measured against opponents using [AIVAT (A New Variance Reduction Technique for Agent Evaluation in Imperfect
Information Games)](https://arxiv.org/pdf/1612.06915.pdf) to substantially reduce the variance in the games by 85%, which can reduce the required number of games by a factor of 10. AIVAT stands for action informed value assessment tool and is proven to be unbiased. 

During the first No Limit Hold'em competition in 2015, the humans beat CMU's AI over 80,000 hands, but there were still uncertainties about whether the match was statistically significant. 

AIVAT effectively uses the known expected value changes of chance (cards that come onto the board) and the strategies of a known agent to reduce the variance. Poker players are familiar with a version of expected value that is called "All-in expected value". In normal games with humans there is no known agent strategy, but we can use a variance reduction measure strictly for all-in situations. When a player is involved in an all-in, the all-in EV calculation measures the value of the all-in according to the player's equity (chance of winning the pot multiplied by the pot size). 

For example, if two players got allin with AA against JJ, AA is approximately an 80% favorite, so if they each put in \\$100 for the allin, then the pot would be \\$200 and AA would have \\$160 equity, for an all-in expected value of +\\$60. However, the true outcome will be either +\\$100 or -\\$100. Many poker sites now have the option to "run it twice", to run out an all-in twice to help reduce the variance. 

Another common variance reduction technique is using duplicate games, where each hand is played with the reverse cards. For example, we would play 100 hands where I get dealt a specific set of cards and opponent gets a dealt specific set of cards and then repeat the hands where the cards are swapped. This isn't practical with only humans since we would remember cards and hands, but is practical with agent vs. agent since memories can be reset and is also possible with agents vs. humans whereby one agent can play two humans simultaneously where in one game the human is getting X cards and the agent is getting Y cards and on the other the human is getting Y cards and the agent is getting X cards. 

AIVAT uses correction terms that are "constructed in a fashion that shifts an estimate of the expected value after a choice was made towards an estimate of
the expected value before the choice. These terms have expected value of zero and are combined with an unbiased estimate of player value."

Using an abstracted form of Heads Up No Limit Hold'em with 1 and 2 chip blinds and 200 chip starting stacks for experiments over 1 million hands, AIVAT resulted in about a 68% reduction in standard deviation. This was superior in DeepStack because in this experiment, the abstracted game was quite small (8 million information set states), it does a poor job of distinguishing the value of cards since the abstraction is very coarse. 

## Libratus
Libratus was CMU's agent from 2017 that beat four of the best poker players in the world in a 120,000 hand match. It was created by Noam Brown and Tuomas Sandholm. 

The agent, like DeepStack, has three main components, where the latter two are the real keys to success for Libratus:

1. Game abstraction. This part follows the standard solving paradigm of solving an abstracted game and translating the play back into the full game. Their abstraction is what they call the "blueprint strategy", which gets less sophisticated deeper into the game tree (recall that preflop only has 169 independent game states). In practice, this involved abstracting both bet sizes and hand possibilities, both of which were performed algorithmically. Given the abstraction, the agent ran Monte Carlo CFR, which was sped up by a factor of three by pruning actions that seemed very unlikely to be useful. 

2. Real-time solver. Since the abstractions are not as sharp later in the game, a real-time solver is called, which works in conjunction with the blueprint strategy from the first component. Additionally, actions outside of the main blueprint are solved specifically with that action included (called "nested subgame solving"), eliminating the need for what can be a messy translation process to interpret off-abstraction bets in the full game. 

3. Self-improver. Since the real-time solver is periodically working to solve subgames that were not included in the initial abstraction, this component inserts those into the blueprint to strengthen the blueprint. This is valuable because rather than randomly filling in parts of the tree, specifically parts of the tree that are actually seen in practice are filled in, which makes sense because on average these situations or situations similar to these are going to happen more frequently (which is why for poker players, many hands are so routine because they've seen the similar situation so frequently in the past). 

Libratus was tested against 2016 agent Baby Tartanian8, the winner of the most recent ACPC tournament. Using only the game abstraction, Libratus lost to this agent, but after adding in the real-time solver, Libratus soundly won. It also won soundly against four of the best human players in the world in a 2017 "Brains vs. Artificial Intelligence" three week competition that is detailed in the section on AI vs. Human competitions. 

## [Pluribus](https://science.sciencemag.org/content/365/6456/885)
Pluribus made major headlines in 2019 when it showed that it could compete with top human players in multiplayer No Limit Hold'em poker, which was not only a landmark result for poker, but also for multiplayer games in general. Details about the matches against the human opponents are in the AI vs. Human Competitions section. 

The first problem when creating a system for multiplayer poker is that it's unclear what the ideal model is for how the system should work. Players independently playing Nash equilibrium strategies in a multiplayer game does not necessarily result in an overall equilibrium and players could have incentive to deviate. They give an example of the Lemonade Stand Game, where the equilibrium is for all players to be equally spaced out in a circle and there are infinite placements that would result in equilibrium, but if each player picked their own equilibrium independently, then the result would not be equilibrium. They conclude that the goal should essentially just to be to create a strong agent and suggest that the best way to test this is against humans, given the lack of AI agents that existed that could play multiplayer. 

Pluribus's development is very similar to previous poker agents. They use the following main pieces: 
1. Bet and card abstractions, which include up to 14 different bet options and card abstractions only for future rounds such that the current round can understand exactly what the hand strengths are. 

2. Monte Carlo CFR. Like with Libratus, the initial abstracted solution is referred to as the "blueprint strategy" and is computed using Monte Carlo CFR for 8 days and 12,400 CPU core hours. Surprisingly, this cost only about \\$150 in cloud computing fees. Pluribus uses mostly standard CFR techniques, but does use "Linear CFR", which assigns more weight to later iterations in proportion to their iteration timestep, but only for early iterations since there is more value in discounting there. They also do epsilon pruning to remove very unlikely actions in 95% of iterations (i.e. an action with negative regret beyond some threshold only would be sampled 5% of the time). 

3. Depth-limited search. As in Libratus, the agent only plays based on the blueprint in the preflop betting round and in later rounds uses "real-time search". The search uses a method that assumes that each player chooses between four different strategies for the remainder of the game, which are all related to the blueprint strategy. There is the default one and the other three that have biases towards folding, calling, and raising. 

Pluribus tracks the probability of reaching the current situation with each possible hand in its strategy. This is the equivalent of being awards of its range of hands, an important principle in human poker. By doing so, we can play a balanced strategy that carefully weights bets and bluffs and is not predictable. 

The paper says that Pluribus plays at about 20 seconds per hand at a table full of Pluribii, which is actually quite fast, but I am curious to know its average thinking time to see how that aligns with time that humans are allowed at a poker table. 

## [Supremus](https://arxiv.org/pdf/2007.10442.pdf )
This paper -- Unlocking the Potential of Deep Counterfactual Value Networks -- was a collaboration by the Minimal AI group and Noam Brown. This agent essentially first implements the DeepStack algorithm and then improves on it by using a modified CFR method called DCFR+ that solves the "sparse lookahead tree with continual resolving", "custom hyper optimized kernals in CUDA", and neural networks on all lookahead trees instead of a standard abstraction. 

DCFR stands for Discounted Counterfactual Regret Minimization from the 2019 paper [Solving Imperfect-Information Games via Discounted Regret Minimization](https://arxiv.org/pdf/1809.04040.pdf) and involves discounting regrets in earlier iterations of CFR and counting them as less useful than more recent regrets in order to speed up convergence. 

DCFR+, introduced in the Supremus paper, has the key insight that it "delays the starting point at which the average policy is tracked" and by "using a linear weighting scheme for the average policy rather than quadratic". In their case, they used a constant of 100 to assign weight of 0 to the first 100 iteration weights and then linearly begin at 0 for future weights. 

### Compared to DeepStack
The reimplementation of DeepStack resulted in lower error rates for the turn (.016 compared to 0.026) and flop (0.028 compared to 0.034) networks. This resulted in a reimplemented agent that won 536 +/- 68 mbb per hand compared to the original DeepStack winning 428 +/- 87 mbb/g against a local best response function that plays only fold and call. The Supremus agent did significantly better, winning 951 +/- 96 mbb/g. 

The algorithm is able to complete 1000 tree iterations in 0.8 seconds, about 6x faster than DeepStack, thanks to the more efficient GPU implementation. 

### Compared to Slumbot
The 2018 ACPC winner was the Slumbot agent, a strong abstraction-based agent. The DeepStack reimplementation lost to Slumbot by 63 mbb/g +/- 40 with all-in expected value variance reduction. Supremus thoroughly beat Slumbot a rate of 176 mbb per hand +/- 44 in the same 150,000 hand sample. 

<!-- ## ReBeL
https://arxiv.org/pdf/2007.13544.pdf 
https://www.youtube.com/watch?v=BhUWvQmLzSk 
https://ai.facebook.com/blog/rebel-a-general-game-playing-ai-bot-that-excels-at-poker-and-more/ -->

## What's next? 
I'm excited to see agents that might work more on opponent exploitation rather than optimal play. For example, updating strategies according to opponents or testing small changes to strategies to see if they perform better. While both multiplayer games and opponent exploitation have seen relatively little research compared to one on one games, it might be especially interesting to see them combined. In a sense, this might come automatically in multiplayer games since it makes less sense to solve them from a game theoretically optimal perspective. 