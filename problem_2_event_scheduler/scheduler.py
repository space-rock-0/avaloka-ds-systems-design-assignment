import heapq
 
 
def can_attend_all(events):
    sorted_events = sorted(events)
 
    for i in range(1, len(sorted_events)):
        if sorted_events[i - 1][1] > sorted_events[i][0]:
            return False
 
    return True
 
 
def min_rooms_required(events):
    if not events:
        return 0
 
    sorted_events = sorted(events)
    end_times = []
    maximum_rooms = 0
 
    for start, end in sorted_events:
        while end_times and end_times[0] <= start:
            heapq.heappop(end_times)
 
        heapq.heappush(end_times, end)
 
        maximum_rooms = max(
            maximum_rooms, len(end_times)
        )
 
    return maximum_rooms
 
 
if __name__ == "__main__":
    events = [(9, 10), (10, 11), (11, 12)]
 
    print("Can attend all meetings:",
          can_attend_all(events))
 
    print("Minimum rooms required:",
          min_rooms_required(events))
