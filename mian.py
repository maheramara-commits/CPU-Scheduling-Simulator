from collections import deque

# =====================================
# CPU SCHEDULING SIMULATOR
# Group: YWAV
# Algorithms: FCFS and Round Robin
# =====================================

# 1. Process Data

processes = [
    {"name": "P1", "arrival": 0, "burst": 1, "priority": 2},
    {"name": "P2", "arrival": 1, "burst": 9, "priority": 2},
    {"name": "P3", "arrival": 2, "burst": 2, "priority": 5},
    {"name": "P4", "arrival": 3, "burst": 3, "priority": 5},
    {"name": "P5", "arrival": 5, "burst": 1, "priority": 2},
    {"name": "P6", "arrival": 7, "burst": 5, "priority": 3}
]

quantum = 2


# 2. FCFS Algorithm

def fcfs(processes):

    ordered = sorted(
        processes,
        key=lambda p: p["arrival"]
    )

    current_time = 0
    gantt = []
    results = {}

    for p in ordered:

        name = p["name"]
        arrival = p["arrival"]
        burst = p["burst"]

        if current_time < arrival:
            gantt.append(
                ("IDLE", current_time, arrival)
            )
            current_time = arrival

        start = current_time
        current_time += burst

        completion = current_time
        turnaround = completion - arrival
        waiting = turnaround - burst
        response = start - arrival

        results[name] = {
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response
        }

        gantt.append((name, start, current_time))

    return gantt, results


# 3. Round Robin Algorithm

def round_robin(processes, quantum):

    ordered = sorted(
        processes,
        key=lambda p: p["arrival"]
    )

    ready_queue = deque()

    remaining = {
        p["name"]: p["burst"]
        for p in ordered
    }

    first_start = {}
    completion_time = {}

    current_time = 0
    next_process = 0
    completed = 0

    n = len(ordered)
    gantt = []

    while completed < n:

        # Add arrived processes

        while (
            next_process < n
            and ordered[next_process]["arrival"] <= current_time
        ):

            ready_queue.append(
                ordered[next_process]["name"]
            )

            next_process += 1

        # CPU is idle

        if not ready_queue:

            if next_process < n:

                next_arrival = ordered[next_process]["arrival"]

                gantt.append(
                    ("IDLE", current_time, next_arrival)
                )

                current_time = next_arrival

            continue

        # Select process

        name = ready_queue.popleft()

        if name not in first_start:
            first_start[name] = current_time

        # Execute process

        execution = min(
            quantum,
            remaining[name]
        )

        start = current_time

        current_time += execution

        remaining[name] -= execution

        gantt.append(
            (name, start, current_time)
        )

        # Add newly arrived processes

        while (
            next_process < n
            and ordered[next_process]["arrival"] <= current_time
        ):

            ready_queue.append(
                ordered[next_process]["name"]
            )

            next_process += 1

        # Check completion

        if remaining[name] == 0:

            completion_time[name] = current_time
            completed += 1

        else:

            ready_queue.append(name)

    # Calculate results

    results = {}

    for p in ordered:

        name = p["name"]
        arrival = p["arrival"]
        burst = p["burst"]

        completion = completion_time[name]

        turnaround = completion - arrival
        waiting = turnaround - burst
        response = first_start[name] - arrival

        results[name] = {
            "start": first_start[name],
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response
        }

    return gantt, results


# 4. Display Gantt Chart

def display_gantt(gantt):

    print("\nGANTT CHART")
    print("-" * 60)

    for name, start, end in gantt:

        print(
            f"| {name} ({start}-{end}) ",
            end=""
        )

    print("|")
    print("-" * 60)


# 5. Display Results

def display_results(title, processes, gantt, results):

    print("\n")
    print("=" * 75)
    print(title)
    print("=" * 75)

    display_gantt(gantt)

    print("\nPROCESS TABLE")

    print(
        f"{'Name':<8}"
        f"{'Arrival':<10}"
        f"{'Burst':<10}"
        f"{'Start':<10}"
        f"{'Finish':<10}"
        f"{'Waiting':<10}"
        f"{'Turnaround':<13}"
        f"{'Response':<10}"
    )

    for p in processes:

        name = p["name"]
        r = results[name]

        print(
            f"{name:<8}"
            f"{p['arrival']:<10}"
            f"{p['burst']:<10}"
            f"{r['start']:<10}"
            f"{r['completion']:<10}"
            f"{r['waiting']:<10}"
            f"{r['turnaround']:<13}"
            f"{r['response']:<10}"
        )

    n = len(processes)

    avg_waiting = sum(
        r["waiting"] for r in results.values()
    ) / n

    avg_turnaround = sum(
        r["turnaround"] for r in results.values()
    ) / n

    avg_response = sum(
        r["response"] for r in results.values()
    ) / n

    print("\nAVERAGES")

    print("Average Waiting Time:", round(avg_waiting, 2))
    print("Average Turnaround Time:", round(avg_turnaround, 2))
    print("Average Response Time:", round(avg_response, 2))

    return {
        "waiting": avg_waiting,
        "turnaround": avg_turnaround,
        "response": avg_response
    }


# 6. Compare Algorithms

def compare_algorithms(fcfs_avg, rr_avg):

    print("\n")
    print("=" * 65)
    print("ALGORITHM COMPARISON")
    print("=" * 65)

    print(
        f"{'Metric':<25}"
        f"{'FCFS':<18}"
        f"{'Round Robin':<18}"
    )

    print("-" * 65)

    for metric in [
        "waiting",
        "turnaround",
        "response"
    ]:

        print(
            f"{metric:<25}"
            f"{fcfs_avg[metric]:<18.2f}"
            f"{rr_avg[metric]:<18.2f}"
        )

    print("=" * 65)


# 7. Main Program

def main():

    print("\n")
    print("*" * 60)
    print("       CPU SCHEDULING SIMULATOR")
    print("              GROUP YWAV")
    print("*" * 60)

    print("\nNumber of Processes:", len(processes))
    print("Round Robin Quantum:", quantum)

    # Run FCFS

    fcfs_gantt, fcfs_results = fcfs(processes)

    fcfs_avg = display_results(
        "FCFS SCHEDULING",
        processes,
        fcfs_gantt,
        fcfs_results
    )

    # Run Round Robin

    rr_gantt, rr_results = round_robin(
        processes,
        quantum
    )

    rr_avg = display_results(
        "ROUND ROBIN SCHEDULING",
        processes,
        rr_gantt,
        rr_results
    )

    # Compare results

    compare_algorithms(
        fcfs_avg,
        rr_avg
    )

    print("\nPROGRAM FINISHED SUCCESSFULLY!")


# Start Program

if __name__ == "__main__":
    main()








    