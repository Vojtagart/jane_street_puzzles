import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import matplotlib.patheffects as PathEffects

class Solution:
    def __init__(self):
        self.grid = [
            [None, 8, 4, None, None, 11, None, None, None, 5, None],
            [None, None, None, None, None, None, None, 11, None, None, None],
            [None, None, 7, None, None, 1, None, None, None, None, 14],
            [28, None, None, 51, None, None, 1, None, 6, None, None],
            [None, 22, None, None, None, None, None, None, 4, None, 1],
            [None, None, None, 15, None, 10, None, 0, None, None, None],
            [11, None, 11, None, None, None, None, None, None, 9, None],
            [None, None, 17, None, 14, None, None, 10, None, None, 13],
            [30, None, None, None, None, 6, None, None, 45, None, None],
            [None, None, None, 10, None, None, None, None, None, None, None],
            [None, 26, None, None, None, 0, None, None, 77, 61, None]
        ]
        self.rows = 11
        
        self.state_grid = [[0 for _ in range(self.rows)] for _ in range(self.rows)]
        self.capital_grid = [[False for _ in range(self.rows)] for _ in range(self.rows)]

    def mark_state(self, row, col, state_id, is_capital=False):
        """Assigns a cell to a state and optionally flags it as the state's capital"""
        if state_id <= 0:
            raise ValueError(f"State id must be positive, got {state_id}")

        if 1 <= row <= self.rows and 1 <= col <= self.rows:
            self.state_grid[row - 1][col - 1] = state_id
            self.capital_grid[row - 1][col - 1] = is_capital
        else:
            raise IndexError(f"Position ({row}, {col}) is out of bounds")

    def visualize(self):
        """Renders the (partial) solution"""
        _, ax = plt.subplots(figsize=(8, 8))

        # Add state coloring
        colored_grid = np.array(self.state_grid, dtype=float)
        colored_grid[colored_grid <= 0] = np.nan  
        ax.imshow(colored_grid, cmap='tab20', vmin=0, vmax=20)

        # coinfigure axis
        ax.set_xlim(-0.5, self.rows - 0.5)
        ax.set_ylim(self.rows - 0.5, -0.5)
        ax.set_xticks(np.arange(self.rows))
        ax.set_yticks(np.arange(self.rows))

        # 1-based indexing
        ax.set_xticklabels(np.arange(1, self.rows + 1))
        ax.set_yticklabels(np.arange(1, self.rows + 1))
        
        ax.tick_params(which='major', labeltop=True, labelright=True, top=True, right=True)
        
        ax.set_xticks(np.arange(-0.5, self.rows, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
        ax.grid(which='minor', color='black', linewidth=1.5)
        ax.tick_params(which='minor', bottom=False, left=False, top=False, right=False)

        state_sizes = self._get_state_sizes()

        # draw grid cells
        for r in range(self.rows):
            for c in range(self.rows):
                # draw the distance clue
                dist = self.grid[r][c]
                if dist is not None:
                    ax.text(c, r, str(dist), va='center', ha='center', fontsize=14, fontweight='bold', color='black')

                # draw the state
                state_id = self.state_grid[r][c]
                if state_id > 0:
                    state_size = state_sizes[state_id]
                    txt = ax.text(c + 0.42, r - 0.42, str(state_size), va='top', ha='right', fontsize=10, fontweight='bold', color='black')
                    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='white')])
                
                # draw the capital
                if self.capital_grid[r][c]:
                    ax.plot(c - 0.35, r - 0.35, marker='o', markersize=6, color='red', markeredgecolor='black')

        plt.show()

    def get_final_answer(self):
        """Calculates the sum of squares of row sums"""
        state_sizes = self._get_state_sizes()

        answer = 0
        for r in range(self.rows):
            row_sum = sum(state_sizes[self.state_grid[r][c]] for c in range(self.rows))
            answer += row_sum**2

        return answer

    def _get_state_sizes(self):
        state_sizes = {}
        for r in range(self.rows):
            for c in range(self.rows):
                state_id = self.state_grid[r][c]
                if state_id > 0:
                    state_sizes[state_id] = state_sizes.get(state_id, 0) + 1
        return state_sizes


def fill_states(sol: Solution, states: List[Dict]):
    """Fills states into given solution"""
    for state in states:
        state_id = state["id"]
        capital = state["capital"]

        for r, c in state["cells"]:
            is_cap = (capital is not None) and (capital == (r, c))
            sol.mark_state(r, c, state_id, is_capital=is_cap)
