#algorithm for least recently used page replacement

import os

def lru(pages, n, capacity):
    #basically this creates the empty frames for the memory like f0, f1, and etc where the pages will be stored
    frames = [''] * capacity

    #stores the history of each frame, for display purposes
    frame_history = []
    #_ is a placeholder variable, we just want to make empty lists for now so we can fill it in later
    for _ in range(capacity):
        frame_history.append([])
        
    #stores the history of page faults, for display purposes
    fault_history = []

    #page fault and hit counters
    page_faults = 0
    page_hits = 0

    #to store last used index of each page
    #its a dictionary, basically the key is the page and the value is the last index it was used
    #like 'A': 3, means that page A was last used at index 3
    last_used = {}

    #the actual lru
    for i in range(n):
        page = pages[i]
        if page in frames:
            # page hit occurs
            page_hits += 1
            fault_history.append(' ')
        else:
            #page fault occurs
            page_faults += 1
            fault_history.append('*')
            #no need to replace anything if theres an empty slot, just add new page
            if '' in frames:
                # find empty slot
                idx = frames.index('')
                frames[idx] = page
            else:
                #find LRU
                #the last used.get thing is to get the last used index of the page
                #if the page is not there, then return -1 meaning it hasnt been used yet
                #then we find the index with the smallest last used index, which would be our LRU page
                #hence the use of min
                lru_idx = min(range(capacity), key=lambda x: last_used.get(frames[x], -1))
                frames[lru_idx] = page

        #this is to update the last used index of the page
        last_used[page] = i

        #snapshot the current state of memory and save it
        for j in range(capacity):
            frame_history[j].append(frames[j])

    #calculating for success and failure rates
    total_requests = len(pages)
    failure_rate = (page_faults / total_requests) * 100
    success_rate = (page_hits / total_requests) * 100

    #return the results as a dictionary
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

#we get the unique values from the sequence
#this is to convert the numerical sequence into tokens (integer)
def parse(token):
    token = token.strip()
    #this is the space between each number, we ignore it
    if token == "":
        return None
    try:
        #if it isnt empty and is a number, return it as a token, and try to convert it to an integer
        return int(token)
        #if the user inputs string based sequence, it throws this error and we just return the string token instead of converting it to an integer
    except ValueError:
        return token

# main
if __name__ == "__main__":
    os.system('clear')

    #ask user for number of memory frames
    capacity = int(input("Enter the number of memory frames: "))
    #ask user for the requested pages sequence
    pages_input = input("Enter the sequence of requested pages (space-separated): ")

    #convert the sequence into tokens and call the fifo function
    #this is for string based sequence input, the parse thing is for converting it into int
    pages = []
    for token in pages_input.split():
        token = token.strip()
        if token != "":
            page = parse(token)
            pages.append(page)

    #holds the unique job pages
    jobs = list(set(pages))
    length = len(pages)

    #this just checks if its valid before running the function
    if length > 0 and capacity > 0:
        result = lru(pages, length, capacity)

        #formatting and printing the output table
        col_width = 4

        #this prints the sequence header row
        header = "Pages".ljust(6) + "| " + " | ".join(str(p).center(col_width) for p in result['pages']) + " |"
        print("\n" + "=" * len(header))
        print(header)
        print("=" * len(header))

        #this prints the history of each frame
        for i in range(result['capacity']):
            row_str = f"F{i}".ljust(6) + "| " + " | ".join(str(f).center(col_width) for f in result['frame_history'][i]) + " |"
            print(row_str)

        #this prints the page interruption row
        print("-" * len(header))
        pi_row = "PI".ljust(6) + "| " + " | ".join(str(mark).center(col_width) for mark in result['fault_history']) + " |"
        print(pi_row)
        print("=" * len(header))

        print(f"\nTotal Page Faults (Failures): {result['page_faults']}")
        print(f"Total Page Hits (Successes): {result['page_hits']}")
        print(f"Failure Rate: {result['failure_rate']:.2f}%")
        print(f"Success Rate: {result['success_rate']:.2f}%")
    else:
        print("Please enter valid frames and a sequence.")

#This code is heavily guided by the one created by ishankhandelwals
#https://www.geeksforgeeks.org/dsa/program-for-least-recently-used-lru-page-replacement-algorithm/