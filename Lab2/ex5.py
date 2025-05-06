import math

def count_shortest_paths(horizontal_steps: int, vertical_steps: int) -> int:
    n = horizontal_steps + vertical_steps
    k = horizontal_steps
    return math.comb(n, k)


def count_restricted_paths(horizontal_steps: int, vertical_steps: int) -> int:
    dp = [[[0, 0] for _ in range(vertical_steps + 1)] for _ in range(horizontal_steps + 1)]
    dp[0][0][0] = 1  
    for h in range(horizontal_steps + 1):
        for v in range(vertical_steps + 1):
            if h == 0 and v == 0:
                continue
            if h > 0:
                dp[h][v][0] = dp[h-1][v][0] + dp[h-1][v][1]
            if v > 0:
                dp[h][v][1] = dp[h][v-1][0]

    return dp[horizontal_steps][vertical_steps][0] + dp[horizontal_steps][vertical_steps][1]



if __name__ == "__main__":
    horizontal_steps = 18
    vertical_steps = 17

    print(f"Общее количество кратчайших путей: {count_shortest_paths(horizontal_steps, vertical_steps)}")
    print(f"Количество кратчайших путей с ограничением: {count_restricted_paths(horizontal_steps, vertical_steps)}")