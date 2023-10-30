import tkinter as tk
from tkinter import messagebox, simpledialog


class KitchenCabinet:
    def __init__(self, material, dimensions, coordinates):
        self.material = material
        self.dimensions = dimensions
        self.coordinates = coordinates

    def intersects(self, other):
        # Проверка пересечения двух шкафов в 3D пространстве
        for i in range(3):
            if (self.coordinates[i] > other.coordinates[i] + other.dimensions[i] or
                    self.coordinates[i] + self.dimensions[i] < other.coordinates[i]):
                return False
        return True

    def is_too_close(self, other):
        # Проверка, что два шкафа из разных материалов находятся слишком близко (меньше 2 метров)
        if self.material != other.material:
            for i in range(3):
                if abs(self.coordinates[i] - other.coordinates[i]) < 2:
                    return True
        return False


class Appliance:
    def __init__(self, name, dimensions, coordinates):
        self.name = name
        self.dimensions = dimensions
        self.coordinates = coordinates
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on

    def intersects(self, cabinet):
        # Техника не находится внутри объема шкафа по координатам x и y
        for i in range(2):
            if (self.coordinates[i] >= cabinet.coordinates[i] + cabinet.dimensions[i] or
                    self.coordinates[i] + self.dimensions[i] <= cabinet.coordinates[i]):
                return False

        # Проверяем z координату
        if (self.coordinates[2] <= cabinet.coordinates[2] or
                self.coordinates[2] >= cabinet.coordinates[2] + cabinet.dimensions[2]):
            return False

        # Если техника находится ровно на верхней границе шкафа или выше, они не пересекаются
        if self.coordinates[2] >= cabinet.coordinates[2] + cabinet.dimensions[2]:
            return False

        # Если нижняя часть техники находится выше нижней части шкафа, но ниже его верхней части, они пересекаются
        if self.coordinates[2] - self.dimensions[2] < cabinet.coordinates[2] + cabinet.dimensions[2]:
            return True

        return False


class Kitchen:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.cabinets = []
        self.appliances = []

    def add_cabinet(self, cabinet):
        self.cabinets.append(cabinet)

    def add_appliance(self, appliance):
        self.appliances.append(appliance)

    def check_conditions(self):
        for i in range(len(self.cabinets)):
            for j in range(i+1, len(self.cabinets)):
                if self.cabinets[i].intersects(self.cabinets[j]):
                    return f"Cabinets {i+1} and {j+1} intersect."
                if self.cabinets[i].is_too_close(self.cabinets[j]):
                    return f"Cabinets {i+1} and {j+1} of different materials are too close."

        for i in range(len(self.appliances)):
            for j in range(len(self.cabinets)):
                if self.appliances[i].intersects(self.cabinets[j]):
                    return f"Appliance {i+1} and Cabinet {j+1} intersect."

        for appliance in self.appliances:
            is_floating = True
            for cabinet in self.cabinets:
                if (appliance.coordinates[2] == cabinet.coordinates[2] + cabinet.dimensions[2] and
                        appliance.coordinates[0] + appliance.dimensions[0] <= cabinet.coordinates[0] +
                        cabinet.dimensions[0] and
                        appliance.coordinates[0] >= cabinet.coordinates[0] and
                        appliance.coordinates[1] + appliance.dimensions[1] <= cabinet.coordinates[1] +
                        cabinet.dimensions[1] and
                        appliance.coordinates[1] >= cabinet.coordinates[1]):
                    is_floating = False
                    break
            if is_floating:
                return f"Appliance {appliance.name} is floating."

        return "All conditions met."


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitchen Planner")

        self.kitchen = Kitchen((10, 10, 3))

        # GUI
        self.label = tk.Label(root, text="Kitchen Planner")
        self.label.pack(pady=10)

        self.add_cabinet_button = tk.Button(root, text="Add Cabinet", command=self.add_cabinet)
        self.add_cabinet_button.pack(pady=5)

        self.add_appliance_button = tk.Button(root, text="Add Appliance", command=self.add_appliance)
        self.add_appliance_button.pack(pady=5)

        self.check_button = tk.Button(root, text="Check Conditions", command=self.check_conditions)
        self.check_button.pack(pady=20)

    def add_cabinet(self):
        material = simpledialog.askstring("Input", "Enter cabinet material:")
        dimensions = simpledialog.askstring("Input", "Enter cabinet dimensions (x,y,z):").split(',')
        coordinates = simpledialog.askstring("Input", "Enter cabinet coordinates (x,y,z):").split(',')
        cabinet = KitchenCabinet(material, list(map(float, dimensions)), list(map(float, coordinates)))
        self.kitchen.add_cabinet(cabinet)

    def add_appliance(self):
        name = simpledialog.askstring("Input", "Enter appliance name:")
        dimensions = simpledialog.askstring("Input", "Enter appliance dimensions (x,y,z):").split(',')
        coordinates = simpledialog.askstring("Input", "Enter appliance coordinates (x,y,z):").split(',')
        appliance = Appliance(name, list(map(float, dimensions)), list(map(float, coordinates)))
        self.kitchen.add_appliance(appliance)

    def check_conditions(self):
        result = self.kitchen.check_conditions()
        messagebox.showinfo("Result", result)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
