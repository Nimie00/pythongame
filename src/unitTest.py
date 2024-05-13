import unittest
from CharacterHandler import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.char = Character("Test Character", player=True, image_path="test.jpg")
        self.char.money = 100

    def test_decrease_health(self):
        self.char.health = 50
        self.char.decrease_health(20)
        self.assertEqual(self.char.health, 30)

    def test_decrease_hunger(self):
        self.char.hunger = 50
        self.char.decrease_hunger(20)
        self.assertEqual(self.char.hunger, 30)

    def test_increase_health(self):
        self.char.health = 50
        self.char.increase_health(30)
        self.assertEqual(self.char.health, 80)

    def test_increase_hunger(self):
        self.char.hunger = 50
        self.char.increase_hunger(30)
        self.assertEqual(self.char.hunger, 80)

    def test_add_item_to_inventory(self):
        self.char.add_item_to_inventory_in_order("Sword")
        self.assertIn("Sword", [item for row in self.char.get_inventory() for item in row])

    def test_remove_item_from_inventory(self):
        self.char.add_item_to_inventory_in_order("Sword")
        self.char.remove_item_from_inventory(0, 0)
        self.assertIsNone(self.char.get_inventory()[0][0])

    def test_buy_item(self):
        self.char.buy_item("Food", 50)
        self.assertEqual(self.char.get_money(), 50)

    def test_search_for_item(self):
        # Implementációs teszt, amely csak a függvény meghívásának helyességét ellenőrzi
        self.char.search_for_item()
        # Tesztelhető, hogy a karakter inventory-ja megváltozott-e a keresés során

    def test_eat_food(self):
        self.char.eat_food("alma")
        self.assertEqual(self.char.get_health(), 100)  # Az alap érték 100 + az almához tartozó 20 életerő

    # Új tesztek hozzáadása az előzőek mellé
    def test_get_health(self):
        self.assertEqual(self.char.get_health(), 100)

    def test_get_hunger(self):
        self.assertEqual(self.char.get_hunger(), 100)

    def test_get_health(self):
        self.assertEqual(self.char.get_health(), 100)

    def test_get_hunger(self):
        self.assertEqual(self.char.get_hunger(), 100)

    def test_get_activity(self):
        self.assertIsNone(self.char.get_activity())

    def test_get_stand_at_city(self):
        self.assertFalse(self.char.get_stand_at_city())

    def test_get_wandering_at_market(self):
        self.assertFalse(self.char.get_wandering_at_market())

    def test_get_collecting_mode(self):
        self.assertFalse(self.char.get_collecting_mode())

    def test_get_sleeping(self):
        self.assertFalse(self.char.get_sleeping())

    def test_get_inventory(self):
        expected_inventory = [[None] * 5 for _ in range(5)]
        self.assertEqual(self.char.get_inventory(), expected_inventory)

    def test_get_money(self):
        self.assertEqual(self.char.get_money(), 100)

    def test_get_food_items(self):
        expected_food_items = {"alma": 40, "hal": 70, "sajt": 60, "eletero_itala": 200, "gyogynoveny": 50}
        self.assertEqual(self.char.get_food_items(), expected_food_items)
    def test_set_health(self):
        self.char.increase_health(80)
        self.assertEqual(self.char.get_health(), 100)

    def test_set_hunger(self):
        self.char.increase_hunger(90)
        self.assertEqual(self.char.get_hunger(), 100)

    def test_set_activity(self):
        self.char.set_activity("Barangolás")
        self.assertEqual(self.char.get_activity(), "Barangolás")

    def test_set_stand_at_city(self):
        self.char.set_stand_at_city(True)
        self.assertTrue(self.char.get_stand_at_city())

    def test_set_wandering_at_market(self):
        self.char.set_wandering_at_market(True)
        self.assertTrue(self.char.get_wandering_at_market())

    def test_set_collecting_mode(self):
        self.char.set_collecting_mode(True)
        self.assertTrue(self.char.get_collecting_mode())

    def test_set_sleeping(self):
        self.char.set_sleeping(True)
        self.assertTrue(self.char.get_sleeping())

    def test_set_money(self):
        self.char.set_money(50)
        self.assertEqual(self.char.get_money(), 50)

    def test_get_name(self):
        self.assertEqual(self.char.get_name(), "Test Character")

    def test_get_image_path(self):
        self.assertEqual(self.char.get_image_path(), "test.jpg")

    def test_get_player(self):
        self.assertTrue(self.char.get_player())

    def test_get_has_food(self):
        self.assertEqual(self.char.get_has_food(), 0)

    def test_get_activity_probabilities(self):
        expected_activity_probabilities = {
            "Barangolás": 0.25,
            "Állás a standnál": 0.25,
            "Járkálás a falu vásárjában": 0.25,
            "Gyűjtögető üzemmód": 0.25,
        }
        self.assertEqual(self.char.get_activity_probabilities(), expected_activity_probabilities)

    def test_set_name(self):
        self.char.set_name("New Character Name")
        self.assertEqual(self.char.get_name(), "New Character Name")

    def test_set_image_path(self):
        self.char.set_image_path("new_image.png")
        self.assertEqual(self.char.get_image_path(), "new_image.png")

    def test_set_player(self):
        self.char.set_player(False)
        self.assertFalse(self.char.get_player())

    def test_set_has_food(self):
        self.char.set_has_food(1)
        self.assertEqual(self.char.get_has_food(), 1)

if __name__ == '__main__':
    unittest.main()