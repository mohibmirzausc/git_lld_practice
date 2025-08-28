import unittest
from restaurant import Restaurant, RestaurantBuilder
from order import Order, OrderBuilder
from user import User, Customer, Driver

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("Setting up tests")

    def test_restaurant(self):
        restaurant_builder: RestaurantBuilder = RestaurantBuilder()

        restaurant_builder.set_name("Stirred Roasters")
        restaurant = restaurant_builder.add_menu_item("Matcha", 5.573).add_menu_item("Espresso Latte", 6.702).add_menu_item("Muffin", 7.12).build()

        self.assertEqual(restaurant.get_name().lower(), "stirred roasters")
        self.assertEqual(len(restaurant.get_items()), 3)
        self.assertEqual(restaurant.get_item_price("MAtcha"), 5.57)

        print(restaurant)

    def test_order(self):
        sarah = Customer("Motu")
        order_builder = OrderBuilder()
        order_builder.set_customer(sarah)


        restaurant_builder = RestaurantBuilder()
        restaurant_builder.set_name("Stirred Roasters")
        restaurant = restaurant_builder.add_menu_item("Matcha", 5.573).add_menu_item("Espresso Latte", 6.702).add_menu_item("Muffin", 7.12).build()

        order_builder.set_restaurant(restaurant)

        order_builder.order_item("matcha", 1)

        order = order_builder.build()

        self.assertTrue(order.customer, sarah)



unittest.main(verbosity=2)