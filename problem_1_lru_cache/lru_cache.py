class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.cache = {}

        # Dummy nodes make insertion and removal simpler.
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, node: Node) -> None:
        """Insert a node immediately after the head."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def _remove(self, node: Node) -> None:
        """Remove a node from its current position."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
            return

        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self._add(new_node)
        self.cache[key] = new_node

    def display(self) -> None:
        """Display the current cache contents."""
        current = self.head.next
        items = []

        while current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next

        print(" -> ".join(items) if items else "Empty")


if __name__ == "__main__":
    cache = LRUCache(2)

    cache.put(1, 1)
    print("put(1, 1)")
    cache.display()

    cache.put(2, 2)
    print("put(2, 2)")
    cache.display()

    print("get(1):", cache.get(1))
    cache.display()

    cache.put(3, 3)
    print("put(3, 3) — key 2 is evicted")
    cache.display()

    print("get(2):", cache.get(2))

    cache.put(4, 4)
    print("put(4, 4) — key 1 is evicted")
    cache.display()

    print("get(1):", cache.get(1))
    print("get(3):", cache.get(3))
    print("get(4):", cache.get(4))