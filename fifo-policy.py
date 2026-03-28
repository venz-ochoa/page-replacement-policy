#algorithm for first in first out page replacement

#this is purely for clearing the OS cuz its annoying
import os

def fifo(pages, length, capacity):
    #basically this creates the empty frames for the memory like f0, f1, and etc where the pages will be stored
    frames = [''] * capacity

    #stores the history of each frame, for display purposes
    frame_history = [[] for _ in range(capacity)]
    #stores the history of page faults, for display purposes
    fault_history = []

    #page fault and hit counters
    page_faults = 0
    page_hits = 0

    #fifo pointer to track which frame to replace next
    #this gets replaced every time a page fault happens, and it always loops back to the oldest page
    replace_index = 0

    #the actual fifo
    for page in pages:
        #if the page is not in the frames, then we replace the oldest with the new page and mark it as a page fault
        if page not in frames:
            #page fault occurs
            frames[replace_index] = page
            replace_index = (replace_index + 1) % capacity
            page_faults += 1
            fault_history.append('*')
        else:
            #but if its already there then we just mark it as a page hit and dont do anything to the frames
            #page hit occurs
            page_hits += 1
            fault_history.append(' ')

        #snapshot the current state of memory and save it
        for i in range(capacity):
            frame_history[i].append(frames[i])

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

#main
if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')

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

    if length > 0 and capacity > 0:
        result = fifo(pages, length, capacity)
        
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

#This code is heavily guided by PranchalK 
#https://www.geeksforgeeks.org/dsa/program-page-replacement-algorithms-set-2-fifo/