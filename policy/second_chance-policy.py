# second chance algorithm

def second_chance(pages, length, capacity):
    # create empty frames (like F0, F1, F2...)
    frames = [''] * capacity

    # keeps track of "second chance" bits (True = recently used)
    second_chance_bits = [False] * capacity

    # this stores the history of each frame (for table display)
    frame_history = []
    for _ in range(capacity):
        frame_history.append([])

    # this stores page faults (*) and hits ( )
    fault_history = []

    # counters
    page_faults = 0
    page_hits = 0

    # pointer acts like a clock hand (cycles through frames)
    pointer = 0

    # main loop
    for i in range(length):
        page = pages[i]

        # check if page already exists in frames
        if page in frames:
            page_hits += 1
            fault_history.append(' ')

            # give this page a "second chance"
            index = frames.index(page)
            second_chance_bits[index] = True
        else:
            # page fault occurs
            page_faults += 1
            fault_history.append('*')

            while True:
                # if this frame has NO second chance → replace it
                if not second_chance_bits[pointer]:
                    frames[pointer] = page

                    # newly inserted page gets no second chance yet
                    second_chance_bits[pointer] = False

                    # move pointer forward (circular)
                    pointer = (pointer + 1) % capacity
                    break
                else:
                    # if it has a second chance → remove it and skip
                    second_chance_bits[pointer] = False
                    pointer = (pointer + 1) % capacity

        # save snapshot of frames
        for k in range(capacity):
            frame_history[k].append(frames[k])

    # compute stats
    total_requests = len(pages)
    failure_rate = (page_faults / total_requests) * 100
    success_rate = (page_hits / total_requests) * 100

    # return results (same format as your other algorithms)
    return {
        'page_faults': page_faults,
        'page_hits': page_hits,
        'failure_rate': failure_rate,
        'success_rate': success_rate,
        'frame_history': frame_history,
        'fault_history': fault_history,
        'pages': pages,
        'capacity': capacity
    }

# converts input into usable values (int or string)
def parse(token):
    token = token.strip()

    if token == "":
        return None

    try:
        return int(token)
    except ValueError:
        return token

# main program na to
if __name__ == "__main__":

    # ask user for number of frames
    capacity = int(input("Enter the number of memory frames: "))

    # ask for page sequence
    pages_input = input("Enter the sequence of requested pages (space-separated): ")

    # convert input into list
    pages = []
    for token in pages_input.split():
        token = token.strip()
        if token != "":
            page = parse(token)
            pages.append(page)

    length = len(pages)

    # validation check
    if length > 0 and capacity > 0:
        result = second_chance(pages, length, capacity)

        col_width = 4

        # print header (page sequence)
        header = "Pages".ljust(6) + "| " + " | ".join(str(p).center(col_width) for p in result['pages']) + " |"
        print("\n" + "=" * len(header))
        print(header)
        print("=" * len(header))

        # print frames (F0, F1, ...)
        for i in range(result['capacity']):
            row_str = f"F{i}".ljust(6) + "| " + " | ".join(str(f).center(col_width) for f in result['frame_history'][i]) + " |"
            print(row_str)

        # print page interrupts row
        print("-" * len(header))
        pi_row = "PI".ljust(6) + "| " + " | ".join(str(mark).center(col_width) for mark in result['fault_history']) + " |"
        print(pi_row)
        print("=" * len(header))

        # print results
        print(f"\nTotal Page Faults (Failures): {result['page_faults']}")
        print(f"Total Page Hits (Successes): {result['page_hits']}")
        print(f"Failure Rate: {result['failure_rate']:.2f}%")
        print(f"Success Rate: {result['success_rate']:.2f}%")
    else:
        print("Please enter valid frames and a sequence.")
        
# The code is heavily guided by this page:
# https://www.geeksforgeeks.org/operating-systems/second-chance-or-clock-page-replacement-policy/