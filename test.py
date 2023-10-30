import unittest

from app import Kitchen, KitchenCabinet, Appliance


class TestKitchenPlanner(unittest.TestCase):
    def test_cabinet_intersection(self):
        cabinet1 = KitchenCabinet("Дерево", (2, 1, 2), (0, 0, 0))
        cabinet2 = KitchenCabinet("Металл", (2, 1, 2), (1.5, 0, 0))
        self.assertTrue(cabinet1.intersects(cabinet2))

    def test_cabinet_too_close(self):
        cabinet1 = KitchenCabinet("Дерево", (2, 1, 2), (0, 0, 0))
        cabinet2 = KitchenCabinet("Металл", (2, 1, 2), (1.5, 0, 0))
        self.assertTrue(cabinet1.is_too_close(cabinet2))

    def test_appliance_intersection(self):
        cabinet = KitchenCabinet("Дерево", (2, 1, 2), (0, 0, 0))
        appliance = Appliance("Микроволновка", (0.5, 0.5, 0.3), (0.5, 0.5, 1))
        self.assertTrue(appliance.intersects(cabinet))

    def test_appliance_floating(self):
        kitchen = Kitchen((10, 10, 3))
        cabinet = KitchenCabinet("Дерево", (2, 1, 2), (0, 0, 0))
        appliance = Appliance("Микроволновка", (0.5, 0.5, 0.3), (0.5, 0.5, 2.1))
        kitchen.add_cabinet(cabinet)
        kitchen.add_appliance(appliance)
        self.assertEqual(kitchen.check_conditions(), "Appliance Микроволновка is floating.")

    def test_all_conditions_met(self):
        kitchen = Kitchen((10, 10, 3))
        cabinet = KitchenCabinet("Дерево", (2, 1, 2), (0, 0, 0))
        appliance = Appliance("Микроволновка", (0.5, 0.5, 0.3), (1, 0.5, 2))
        kitchen.add_cabinet(cabinet)
        kitchen.add_appliance(appliance)
        self.assertEqual(kitchen.check_conditions(), "All conditions met.")


if __name__ == '__main__':
    unittest.main()
