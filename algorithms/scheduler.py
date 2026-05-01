SAMPLE_TASKS = [
    {"name": "Task 1", "start": 9, "end": 12, "duration": 3, "priority": 10},
    {"name": "Task 2", "start": 10, "end": 11, "duration": 1, "priority": 4},
    {"name": "Task 3", "start": 11, "end": 13, "duration": 2, "priority": 5},
    {"name": "Task 4", "start": 13, "end": 15, "duration": 2, "priority": 7},
    {"name": "Task 5", "start": 14, "end": 17, "duration": 3, "priority": 9},
    {"name": "Task 6", "start": 15, "end": 16, "duration": 1, "priority": 3},
    {"name": "Task 7", "start": 16, "end": 18, "duration": 2, "priority": 6},
    {"name": "Task 8", "start": 17, "end": 19, "duration": 2, "priority": 8},
    {"name": "Task 9", "start": 18, "end": 19, "duration": 1, "priority": 2},
    {"name": "Task 10", "start": 19, "end": 21, "duration": 2, "priority": 5},
]
DEFAULT_CAPACITY = 8


def greedy_scheduler(meetings):
    '''Finds the most amount of tasks to fit within schedule; Time Complexity: O(nlogn); Space Complexity: O(n)'''
    # Sort meetings by finish time
    meetings.sort(key=lambda m: m["end"]) # Ascending order by end time

    # Initialize result list and last finish time
    selected_items = [] 
    total_priority = 0
    last_finish = float('-inf') # empty 

    # Scan meetings in finish-time order
    for meeting in meetings:
        if meeting["start"] >= last_finish:
            selected_items.append(meeting)
            total_priority += meeting["priority"] 
            last_finish = meeting["end"] 

    return total_priority, selected_items



def knapsack(weights, values, capacity):
    '''Finds combination of tasks that give the most value; Time Complexity: O(n*W); Space Complexity: O(n*w)'''
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
    print("Greedy Scheduler: ")
    tasks = SAMPLE_TASKS.copy()

    total, items = greedy_scheduler(tasks)
    print("Maximum number of tasks:", len(items))
    print("Total Priority: ", total)
    print("Selected tasks:")
    for t in items:
        print(" - " + str(t))
    print()


    print("Knapsack: ")
    weights = [t["duration"] for t in SAMPLE_TASKS]
    values  = [t["priority"] for t in SAMPLE_TASKS]

    max_value, items = knapsack(weights, values, DEFAULT_CAPACITY)
    print("Maximum Priority:", max_value)
    print("Items in Knapsack: ")  
    for i in items:
        print(" - " + str(SAMPLE_TASKS[i]))
    print()

    
    return

if __name__ == "__main__":
    main()