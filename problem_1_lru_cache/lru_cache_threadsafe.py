from threading import Lock


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class ThreadSafeLRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.cache = {}
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = Lock()

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
        # The lock covers the lookup and usage-order update together.
        with self.lock:
            if key not in self.cache:
                return -1

            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value

    def put(self, key: int, value: int) -> None:
        # The lock protects all map and linked-list changes in this operation.
        with self.lock:
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


if __name__ == "__main__":
    cache = ThreadSafeLRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # 1
    cache.put(3, 3)     # Evicts key 2
    print(cache.get(2))  # -1
    cache.put(4, 4)     # Evicts key 1
    print(cache.get(1))  # -1
    print(cache.get(3))  # 3
    print(cache.get(4))  # 4
