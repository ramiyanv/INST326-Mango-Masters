# AI Usage Disclosure:
# I used ChatGPT to help write docstrings 
# and understand how parts of the code should work.
# I reviewed and tested the code to ensure I understand how it works.

class GameCharacter:
    """
    A class to represent a game character with position, resources, and inventory.
    """

    def __init__(self, character_id):
        """
        Initialize the character with an ID, default position, resources, and inventory.
        """
        self.character_id = character_id
        self.x_pos = 0
        self.y_pos = 0
        self.resources = {
            "health": 100.0,
            "energy": 50.0,
            "stamina": 30.0
        }
        self.inventory = {}

    def move_up(self):
        """Move character up by increasing y position by 1."""
        self.y_pos += 1

    def move_down(self):
        """Move character down by decreasing y position by 1."""
        self.y_pos -= 1

    def move_left(self):
        """Move character left by decreasing x position by 1."""
        self.x_pos -= 1

    def move_right(self):
        """Move character right by increasing x position by 1."""
        self.x_pos += 1

    def collect_item(self, item: str, num_items: int):
        """
        Add item(s) to the inventory. Increase count if already exists.
        """
        if item in self.inventory:
            self.inventory[item] += num_items
        else:
            self.inventory[item] = num_items

    def drop_item(self, item: str):
        """
        Remove one of the specified item if it exists in inventory.
        """
        if item in self.inventory:
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def list_inventory(self):
        """
        Print the inventory items and their quantities.
        """
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for item, count in self.inventory.items():
                print(f"{count} {item}")

    def use_resource(self, resource: str, amount: float):
        """
        Reduce the resource level by the specified amount. Not below zero.
        """
        if resource in self.resources:
            self.resources[resource] = max(0, self.resources[resource] - amount)

    def replenish_resource(self, resource: str, amount: float):
        """
        Increase the resource level by the specified amount.
        """
        if resource in self.resources:
            self.resources[resource] += amount

    def get_resource_level(self, resource: str):
        """
        Return the current level of the specified resource.
        """
        return self.resources.get(resource, None)

    def get_position(self):
        """
        Return the current position as an (x, y) tuple.
        """
        return (self.x_pos, self.y_pos)

    def reset_position(self):
        """
        Reset the character's position to (0, 0).
        """
        self.x_pos = 0
        self.y_pos = 0

    def print_summary(self):
        """
        Print a summary of the character's state.
        """
        print(f"\nCharacter ID: {self.character_id}")
        print(f"Position: ({self.x_pos}, {self.y_pos})")
        print("Resources:")
        for r, val in self.resources.items():
            print(f"  {r}: {val}")
        print("Inventory:")
        self.list_inventory()


def main():
    # Create two characters
    hero = GameCharacter("Hero001")
    support = GameCharacter("Support002")

    # Move characters
    hero.move_up()
    hero.move_right()
    support.move_left()
    support.move_down()

    # Collect items
    hero.collect_item("sword", 1)
    hero.collect_item("potion", 2)
    support.collect_item("spellbook", 1)

    # Use resources
    hero.use_resource("energy", 10)
    hero.use_resource("health", 20)
    support.use_resource("stamina", 15)

    # Replenish resources
    hero.replenish_resource("health", 5)
    support.replenish_resource("stamina", 10)

    # Drop an item
    hero.drop_item("potion")

    # Get resource levels
    print(f"Hero's energy: {hero.get_resource_level('energy')}")
    print(f"Support's stamina: {support.get_resource_level('stamina')}")

    # Get and reset position
    print(f"Hero's position: {hero.get_position()}")
    hero.reset_position()
    print(f"Hero's position after reset: {hero.get_position()}")

    # List inventories
    print("\nHero's Inventory:")
    hero.list_inventory()
    print("\nSupport's Inventory:")
    support.list_inventory()

    # Print summaries
    hero.print_summary()
    support.print_summary()


if __name__ == "__main__":
    main()
