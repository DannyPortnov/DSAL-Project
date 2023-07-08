class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


def distribute_items(items: list[Item], capacities):
    num_sacks = len(capacities)
    sacks = [[] for _ in range(num_sacks)]
    total_value = 0
    i = -1
    while len(items) != 0:
        for j, sack in enumerate(sacks):
            item = items[i % len(items)]
            sack_capacity = capacities[j]
            sack_weight = sum(item.weight for item in sack)

            if sack_weight + item.weight <= sack_capacity:
                sack.append(item)
                total_value += item.value
                items.remove(item)
                break

        i += 1

    return sacks, total_value


# Example usage
item_list = [
    Item('Item 1', 5, 10),
    Item('Item 2', 8, 15),
    Item('Item 3', 7, 12),
    Item('Item 4', 4, 8),
    Item('Item 5', 3, 6),
    Item('Item 6', 6, 11),
    Item('Item 7', 9, 18),
    Item('Item 8', 2, 5),
    Item('Item 9', 1, 4),
    Item('Item 10', 10, 20),
]
sack_capacities = [15, 20, 25]

result, total_value = distribute_items(item_list, sack_capacities)

for i, sack in enumerate(result):
    print(f"Sack {i+1}:")
    for item in sack:
        print(f"Item: {item.name}, Weight: {item.weight}, Value: {item.value}")
    print()

print("Total value:", total_value)
