from collections import deque

def johnson_algorithm(tasks):
    """
    Johnson's algorithm for 2-machine scheduling.
    Returns optimal job sequence.
    """
    n = len(tasks)
    remaining = tasks.copy()
    optimal_order = [None] * n
    left, right = 0, n - 1

    while remaining:
        min_task = None
        min_val = float('inf')
        machine = None

        for task in remaining:
            if task['A'] < min_val:
                min_val = task['A']
                min_task = task
                machine = 'A'
            if task['B'] < min_val:
                min_val = task['B']
                min_task = task
                machine = 'B'

        if machine == 'A':
            optimal_order[left] = min_task
            left += 1
        else:
            optimal_order[right] = min_task
            right -= 1

        remaining.remove(min_task)

    return optimal_order

def calculate_metrics(sequence):
    """Calculate makespan and machine B idle time."""
    time_A = 0
    time_B = 0
    idle_time_B = 0
    schedule = []

    for task in sequence:
        start_A = time_A
        finish_A = start_A + task['A']
        time_A = finish_A

        start_B = max(time_B, finish_A)
        idle = start_B - time_B
        if idle > 0:
            idle_time_B += idle

        finish_B = start_B + task['B']
        time_B = finish_B

        schedule.append({
            'id': task['id'],
            'start_A': start_A,
            'finish_A': finish_A,
            'start_B': start_B,
            'finish_B': finish_B,
            'idle': idle
        })

    return time_B, idle_time_B, schedule

def main():
    tasks = [
        {'id': 1, 'A': 3, 'B': 4},
        {'id': 2, 'A': 5, 'B': 2},
        {'id': 3, 'A': 2, 'B': 6},
        {'id': 4, 'A': 8, 'B': 3},
        {'id': 5, 'A': 4, 'B': 5},
        {'id': 6, 'A': 6, 'B': 1},
        {'id': 7, 'A': 1, 'B': 7}
    ]

    original_seq = tasks.copy()
    makespan_orig, idle_orig, _ = calculate_metrics(original_seq)

    optimal_seq = johnson_algorithm(tasks)
    makespan_opt, idle_opt, schedule_opt = calculate_metrics(optimal_seq)

    print("Original order:", [t['id'] for t in original_seq])
    print("Johnson's order:", [t['id'] for t in optimal_seq])

    print("\nSchedule (Johnson's optimal order):")
    print(f"{'Job':<4} | {'A start':<8} | {'A end':<8} | {'B start':<8} | {'B end':<8} | {'Idle B':<6}")
    for step in schedule_opt:
        print(f"{step['id']:<4} | {step['start_A']:<8} | {step['finish_A']:<8} | "
              f"{step['start_B']:<8} | {step['finish_B']:<8} | {step['idle']:<6}")

    print("\nCOMPARATIVE ANALYSIS:")
    print(f"Original makespan: {makespan_orig} minutes")
    print(f"Optimal makespan:  {makespan_opt} minutes")
    print(f"Improvement:       {makespan_orig - makespan_opt} minutes ({(makespan_orig - makespan_opt) / makespan_orig * 100:.1f}%)")
    print(f"Original machine B idle: {idle_orig} minutes")
    print(f"Optimal machine B idle:  {idle_opt} minutes")
    print(f"Idle reduction:          {idle_orig - idle_opt} minutes ({(idle_orig - idle_opt) / idle_orig * 100:.1f}%)")

if __name__ == "__main__":
    main()