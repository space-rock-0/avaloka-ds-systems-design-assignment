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
 
 
def assign_rooms(events):
    if not events:
        return []
 
    sorted_events = sorted(
        enumerate(events),
        key=lambda item: item[1][0]
    )
 
    occupied_rooms = []
    available_rooms = []
    assignments = [None] * len(events)
    next_room = 1
 
    for index, (start, end) in sorted_events:
        while (
            occupied_rooms
            and occupied_rooms[0][0] <= start
        ):
            _, room_number = heapq.heappop(
                occupied_rooms
            )
            heapq.heappush(
                available_rooms, room_number
            )
 
        if available_rooms:
            room_number = heapq.heappop(available_rooms)
        else:
            room_number = next_room
            next_room += 1
 
        assignments[index] = (
            events[index],
            f"Room {room_number}"
        )
 
        heapq.heappush(
            occupied_rooms, (end, room_number)
        )
 
    return assignments
 
 
if __name__ == "__main__":
    events = [(9, 10), (9, 11), (10, 12)]
 
    print("Can attend all meetings:",
          can_attend_all(events))
 
    print("Minimum rooms required:",
          min_rooms_required(events))
 
    print("Room assignments:")
    for event, room in assign_rooms(events):
        print(f"{event} -> {room}")
