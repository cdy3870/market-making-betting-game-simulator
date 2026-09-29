"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
import numpy as np
def expected_value(values, probabilities):
    # TODO: return the expected value of the discrete distribution (values, probabilities).
    
    return np.array(values) @ np.array(probabilities)

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    # TODO: return {'value': expected winnings under optimal reroll policy, 'reroll_faces': sorted faces to reroll}
    values = [i + 1 for i in range(sides)]

    
    expected_val = expected_value(values, [1/sides for i in range(sides)])

    value = sum([max(f, expected_val) for f in values]) / sides

    reroll_faces = np.array(values)[np.where(np.array(values) < expected_val)].tolist()

    return {"value": value, "reroll_faces": reroll_faces}

    # return {"value": 0, "reroll_faces": [0]}

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    # TODO: return {'threshold': t, 'value': V} for the pay-per-reroll die game under the optimal threshold policy.
    
    max_v = 0
    smallest_t = 0
    for t in range(1, sides + 1):
        v_t = ((t + sides) / 2) - ((t - 1) / (sides - t + 1) * reroll_cost)

        if v_t > max_v:
            max_v = v_t
            smallest_t = t

    return {"threshold": smallest_t, "value": max_v}

# Step 4 - red_black_card_game_value
import functools

def red_black_card_game_value(num_red, num_black):
    # TODO: return {'value': expected payout under optimal stopping, 'stop_now': whether to stop immediately}.
    
    @functools.lru_cache(maxsize=None)       
    def V(num_red, num_black):
        if num_red == 0:
            return 0
        if num_black == 0:
            return num_red 

        return max(0, (num_red / (num_red + num_black)) * (1 + V(num_red - 1, num_black)) + (num_black / (num_red + num_black)) * (-1 + V(num_red, num_black - 1)))

    cont = V(num_red, num_black)

    value = max(0, cont)
    stop_now = (cont <= 0)

    return {"value": value, "stop_now": stop_now}

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    # TODO: return a dict with 'bid' and 'ask' symmetric around fair_value with total width spread_width
    
    half = spread_width / 2

    bid = fair_value - half

    ask = fair_value + half

    return {"bid": bid, "ask": ask}

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    # TODO: apply a counterparty trade against your bid/ask and return updated state
        if side == 'buy':
            cash = state["cash"] + size * ask
            inventory = state["inventory"] - size
        elif side == "sell":
            cash = state["cash"] - size * bid
            inventory = state["inventory"] + size

        return {"cash": cash, "inventory": inventory}

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    # TODO: return total P&L given cash, remaining inventory, and settlement value.
    
    return cash + inventory * settlement_value

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    # TODO: expected loss = E[(v-ask)*1{v>ask}] + E[(bid-v)*1{v<bid}] over informed_values.
    

    informed_values_array = np.array(informed_values)
    informed_prob_array = np.array(informed_probabilities)

    ask_side_excess = np.maximum(informed_values_array - ask, 0)
    bid_side_excess = np.maximum(bid - informed_values_array, 0)

    total = (ask_side_excess * informed_prob_array).sum() + (bid_side_excess * informed_prob_array).sum()

    return total

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    # TODO: choose a spread width that is at least base_spread and increases with uncertainty.
    
    return base_spread + 3 * uncertainty

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    # TODO: return {'bid', 'ask'} shifted against inventory around fair_value
    
    if inventory == 0 or skew_strength == 0:
        mid = fair_value
    else:
        mid = fair_value - 2 * inventory

    bid = mid - spread_width / 2 
    ask = mid + spread_width / 2

    return {"bid": bid, "ask": ask}

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    # TODO: Update the fair-value estimate after observing a counterparty trade on the given side.
    
    half_spread = (ask - bid) / 2

    if side == "buy":
        fair_value += adjustment * half_spread
    elif side == "sell":
        fair_value -=  adjustment * half_spread

    return fair_value

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    # TODO: decrement the revealed card, prune zero counts, and return updated deck + mean value.
    
    remaining_counts_copy = remaining_counts.copy()

    remaining_counts_copy[revealed_value] -= 1

    N = sum(remaining_counts_copy.values())



    if N == 0:
        expected_value = 0
    else:
        expected_value = sum([(n * v)/N for v, n in remaining_counts_copy.items()])

    if remaining_counts_copy[revealed_value] <= 0:
        del remaining_counts_copy[revealed_value]

    return {"remaining_counts": remaining_counts_copy, "expected_value": expected_value}

# Step 13 - run_market_making_episode
def run_market_making_episode(true_value, counterparty_sides, initial_fair_value, config):
    # TODO: loop over counterparty_sides, quote, trade, update beliefs, then settle at true_value.

    history = []
    base_spread = config.get("base_spread", 0)
    uncertainty = config.get("uncertainty", 0)
    skew_strength = config.get("skew_strength", 0)
    belief_adjustment = config.get("belief_adjustment", 0)
    
    cash_and_inv = {"cash": config.get("cash", 0), "inventory": config.get("inventory", 0)}
    outputs = {"pnl": 0, "cash": config.get("cash", 0), "inventory": config.get("inventory", 0), "history": history}

    new_fair_value = initial_fair_value

    # print(counterparty_sides)



    for side in counterparty_sides:
        spread_width = uncertainty_spread(base_spread, uncertainty)
        bid_and_ask = inventory_skewed_quotes(new_fair_value, spread_width, cash_and_inv["inventory"], skew_strength)
        cash_and_inv = execute_trade({"cash": cash_and_inv["cash"], "inventory": cash_and_inv["inventory"]}, side, bid_and_ask["bid"], bid_and_ask["ask"])
        new_fair_value = update_fair_value_from_trade(new_fair_value, side, bid_and_ask["bid"], bid_and_ask["ask"], belief_adjustment)

        history.append({"bid": bid_and_ask["bid"], "ask": bid_and_ask["ask"], "side": side, "cash": cash_and_inv["cash"], "inventory": cash_and_inv["inventory"], "fair_value": new_fair_value})

    pnl = mark_to_market_pnl(cash_and_inv["cash"], cash_and_inv["inventory"], true_value)
    
    outputs = {"pnl": pnl, "cash": cash_and_inv["cash"], "inventory": cash_and_inv["inventory"], "fair_value": new_fair_value, "history": history}

    return outputs

# Step 14 - summarize_episode_pnls
def summarize_episode_pnls(pnls):
    # TODO: return a dict with keys 'mean', 'std' (ddof=0), and 'worst' for the given P&L sequence.
    
    mean = np.array(pnls).mean()
    std = np.std(np.array(pnls))
    worst = min(pnls)

    return {"mean": mean, "std": std, "worst": worst}

