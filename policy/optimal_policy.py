# optimal algorithm

def optimal(pages, length, capacity):
    # create empty frames (like F0, F1, F2...)
    frames = [''] * capacity

    # this will store the history of each frame (for table display later)
    frame_history = []
    for _ in range(capacity):
        frame_history.append([])

    # this stores whether each step is a fault (*) or hit ( )
    fault_history = []

    # counters for tracking performance
    page_faults = 0
    page_hits = 0

    # main OPTIMAL algorithm loop
    for i in range(length):
        page = pages[i]

        # if page is NOT in memory then page fault
        if page not in frames:
            page_faults += 1
            fault_history.append('*')

            # if there is still space in frames, just insert it
            if '' in frames:
                empty_index = frames.index('')
                frames[empty_index] = page
            else:
                # otherwise, we need to replace something (this is the OPTIMAL part)

                # track the page that will be used farthest in the future
                farthest = -1
                replace_index = -1

                for j in range(capacity):
                    try:
                        # check when this page will be used again
                        next_use = pages[i+1:].index(frames[j])
                    except ValueError:
                        # if the page is NEVER used again then best one to replace
                        replace_index = j
                        break

                    # keep the page that is used farthest in the future
                    if next_use > farthest:
                        farthest = next_use
                        replace_index = j

                # replace the chosen page with the new one
                frames[replace_index] = page
        else:
            # if page is already in memory then page hit
            page_hits += 1
            fault_history.append(' ')

        # save the current state of frames (snapshot for table)
        for k in range(capacity):
            frame_history[k].append(frames[k])

    # compute stats
    total_requests = len(pages)
    failure_rate = (page_faults / total_requests) * 100
    success_rate = (page_hits / total_requests) * 100

    # return everything needed for display
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

# converts input into usable values (int if possible, otherwise string)
def parse(token):
    token = token.strip()

    # ignore empty inputs
    if token == "":
        return None

    try:
        # try converting to integer
        return int(token)
    except ValueError:
        # if not a number, just keep it as string
        return token

# main program ito
if __name__ == "__main__":

    # ask user for number of frames
    capacity = int(input("Enter the number of memory frames: "))

    # ask for page reference string
    pages_input = input("Enter the sequence of requested pages (space-separated): ")

    # convert input into a list of usable values
    pages = []
    for token in pages_input.split():
        token = token.strip()
        if token != "":
            page = parse(token)
            pages.append(page)

    length = len(pages)

    # basic validation check
    if length > 0 and capacity > 0:
        result = optimal(pages, length, capacity)

        col_width = 4

        # print header (page sequence)
        header = "Pages".ljust(6) + "| " + " | ".join(str(p).center(col_width) for p in result['pages']) + " |"
        print("\n" + "=" * len(header))
        print(header)
        print("=" * len(header))

        # print frame rows (F0, F1, etc.)
        for i in range(result['capacity']):
            row_str = f"F{i}".ljust(6) + "| " + " | ".join(str(f).center(col_width) for f in result['frame_history'][i]) + " |"
            print(row_str)

        # print page interrupt row (faults/hits)
        print("-" * len(header))
        pi_row = "PI".ljust(6) + "| " + " | ".join(str(mark).center(col_width) for mark in result['fault_history']) + " |"
        print(pi_row)
        print("=" * len(header))

        # print final stats
        print(f"\nTotal Page Faults (Failures): {result['page_faults']}")
        print(f"Total Page Hits (Successes): {result['page_hits']}")
        print(f"Failure Rate: {result['failure_rate']:.2f}%")
        print(f"Success Rate: {result['success_rate']:.2f}%")
    else:
        print("Please enter valid frames and a sequence.")
        
# This code is heavily guided by the source code created by ishankhandelwals and Suman Adhikari
# https://www.geeksforgeeks.org/dsa/implementation-of-optimal-page-replacement-algorithm-in-os/
# https://github.com/int-main/Page-Replacement-Algorithms-in-Python
