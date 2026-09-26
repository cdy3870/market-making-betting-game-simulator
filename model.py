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

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

