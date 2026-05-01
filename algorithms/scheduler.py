SAMPLE_TASKS = [
    {"name": "MATH170A", "start": 9, "end": 12, "duration": 3, "priority": 10},
    {"name": "MATH170B", "start": 10, "end": 11, "duration": 1, "priority": 4},
    {"name": "CPSC250", "start": 11, "end": 13, "duration": 2, "priority": 5},
    {"name": "CPSC251", "start": 13, "end": 15, "duration": 2, "priority": 7},
    {"name": "CPSC315", "start": 14, "end": 17, "duration": 3, "priority": 9},
    {"name": "BIOL101", "start": 15, "end": 16, "duration": 1, "priority": 3},
    {"name": "PHYS225", "start": 16, "end": 18, "duration": 2, "priority": 6},
    {"name": "POSC100", "start": 17, "end": 19, "duration": 2, "priority": 8},
    {"name": "CHEM123", "start": 18, "end": 19, "duration": 1, "priority": 2},
    {"name": "AMST101", "start": 19, "end": 21, "duration": 2, "priority": 5},
]
DEFAULT_CAPACITY = 8


def greedy_scheduler():


    return


def knapsack(weights, values, capacity):
    n = len (weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Build DP table
    for i in range(1, n+1):
        for w in range(capacity + 1):
            if weights[i-1] > w:
                dp[i][w] = dp[i-1][w]
            else: 
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
    
    # Find selected items
    w = capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]

    selected_items.reverse()

    return dp[n][capacity], selected_items


def main():
    print("Knapsack: ")
    weights = [t["duration"] for t in SAMPLE_TASKS]
    values  = [t["priority"] for t in SAMPLE_TASKS]

    max_value, items = knapsack(weights, values, DEFAULT_CAPACITY)
    print("Maximum Profit:", max_value)
    print("Items in Knapsack: ")  
    for i in items:
        print(" - " + str(SAMPLE_TASKS[i]))
    return

if __name__ == "__main__":
    main()