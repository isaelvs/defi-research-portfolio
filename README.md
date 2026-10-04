# DeFi and crypto strategy research

**English** · [Español](README.es.md)

I design investment and trading strategies for BTC and DeFi, validate them with backtests, and run them in automated paper trading before any real capital is involved. This repository documents that work as case studies, including the ideas that did not pass validation and why.

## Case studies

| | Case | What it shows |
|---|---|---|
| 01 | [Uniswap v3 concentrated liquidity bot](case-studies/01-uniswap-v3-lp-bot/README.md) | A live bot on Arbitrum with real money, measured against holding, and discarded. Includes a bug I found in my own metric. |
| 02 | [Systematic trading lab](case-studies/02-paper-trading-lab/README.md) | A backtester and 8 BTC systems in paper trading, validated across three market regimes. |
| 03 | [Copying a trading streamer](case-studies/03-copy-trading-validation/README.md) | A study of how a one-month sample misleads, built on 198 transcribed live streams. Figures are indicative; limitations are stated in the case. |
| 04 | [BTC halving-cycle strategy](case-studies/04-halving-cycle-strategy/README.md) | A calendar rule tested over three cycles, with seven entry and five exit variants, and a fourth cycle under way. |

## Live paper trading

[**Daily snapshot of the 8 systems versus holding**](live/README.md), regenerated automatically once a day. The commit history timestamps every snapshot, and results are published whether they are good or bad.

## How I work

- **Compare against holding, not against zero.** In a bull market almost any rule makes money and almost none beats doing nothing.
- **Reserve data the idea has never seen.** An idea only moves forward if it holds up out of sample, in bull and bear markets.
- **Paper trading before capital.** It checks that the live system does what the backtest did.
- **Know when to discard.** Two of the four cases here end with the idea being dropped.

Development is AI-assisted: the strategy design, the risk rules and the validation are mine.

*Nothing here is investment advice. Past and simulated results do not guarantee future results.*
