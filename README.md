# ♜♞♝♛♚ Substrate Chess ♔♕♗♘♖

## Overview

This pallet provides a way to play on-chain chess. It benefits from [`cozy-chess`](https://crates.io/crates/cozy-chess) and its ability to compile to WASM out-of-the-box (`no_std` compatible).

The chess board is represented on-chain as a [*Forsyth–Edwards Notation* (FEN)](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) string, as well as the moves.

### Players

Each match has two players:
- Challenger (Whites)
- Opponent (Blacks)

### Match

When Challenger calls `create_match`, they establish the following parameters:
- Opponent Address
- Style (`Bullet`, `Blitz`, `Rapid`, or `Daily`)
- Bet Asset Id
- Bet Amount

A Match Id is calculated by hashing the tuple `(challenger, opponent, nonce)`, where the `nonce` is incremented for every new match created.

#### Match Style

Match styles define how much time each player has to make their move. Time is measured in blocks, and each style is defined as a `Config` type.

Assuming 6s per block, the following values are recommended:
- `BulletPeriod`: 10 blocks (~1 minute)
- `BlitzPeriod`: 50 blocks (~5 minutes)
- `RapidPeriod`: 150 blocks (~15 minutes)
- `DailyPeriod`: 14400 blocks (~1 day)

In case a player takes longer than the expected time for their move, they lose the match.

The first move of the match is the only exception (right after Opponent calls `join_match`). Challenger (who always makes the first move) can take 100x longer than the average move, and the match results in draw in case time runs out.

#### Match Bets

This pallet is loosely coupled with FRAME's `pallet-assets` (or any other pallet that implements `Inspect` + `Transfer` traits from `frame_support::traits::fungibles`).

In order to create a match, Challenger chooses an Asset Id and an amount. During the execution of `create_match`, a deposit of such asset amount is made from their account.

As soon as Opponent calls `join_match`, an equal deposit is made from their account.

The winner of the match receives both deposits as reward. In case of draws, both players get their deposits back.

### Extrinsic Weights

Although conveniently able to compile to WASM, `cozy_chess` crate wasn't written with Substrate in mind. That means that there is no guarantee that its execution will be linear. This has direct implications on how the extrinsic weights are calculated for this pallet.

The [`docs`](docs/) directory has a detailed description on the strategy used for benchmarking the extrinsic weights.