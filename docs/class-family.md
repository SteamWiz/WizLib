# ClassFamily

The `ClassFamily` is a powerful utility in WizLib that enables automatic discovery and registration of related classes. It creates a queryable "family" of classes that can be looked up by their attributes.

## Overview

A class family is a hierarchy of classes with a single super-parent (termed the "atriarch") at the top. Subclasses inherit from this parent or from other subclasses, forming a tree-like structure.

The key features of ClassFamily are:

1. **Automatic Discovery**: Classes are automatically discovered and registered simply by being defined in the right package location
2. **Attribute-Based Lookup**: Classes can be looked up by their attributes (like name, key, etc.)
3. **Dynamic Instantiation**: Classes can be instantiated dynamically without direct references

## How It Works

When a class inherits from ClassFamily, it becomes the "atriarch" of a family. All subclasses of this class are automatically added to the family. The atriarch maintains a list of all family members in its `family` property.

The ClassFamily system carefully avoids attribute inheritance when querying. It uses `__dict__` to ensure it only sees attributes defined directly on each specific class, not those inherited from parent classes.

## Key Methods

| Method | Description |
|--------|-------------|
| `family_members(attr)` | Get all family members that have the specified attribute |
| `family_member(attr, value)` | Find a family member with a specific attribute value |
| `get_member_attr(attr)` | Get the value of an attribute for a specific family member |

## Example: Vehicle Catalog System

Imagine you're building a vehicle catalog system for a dealership. You have different types of vehicles, each with specific attributes and behaviors. Using ClassFamily, you can organize these vehicles and look them up dynamically.

```python
from wizlib.class_family import ClassFamily

# Base Vehicle class (the "atriarch")
class Vehicle(ClassFamily):
    fuel_type = "unknown"
    wheels = 0
    
    def __init__(self, color, year):
        self.color = color
        self.year = year
    
    def get_description(self):
        return f"{self.year} {self.color} {self.get_vehicle_type()}"
    
    def get_vehicle_type(self):
        return "Vehicle"

# Intermediate class for wheeled vehicles
class WheeledVehicle(Vehicle):
    # Abstract intermediate class, doesn't define a vehicle_type
    pass

# Concrete vehicle classes
class Car(WheeledVehicle):
    vehicle_type = "car"
    wheels = 4
    fuel_type = "gasoline"
    
    def get_vehicle_type(self):
        return self.vehicle_type

class ElectricCar(Car):
    vehicle_type = "electric car"
    fuel_type = "electricity"

class Motorcycle(WheeledVehicle):
    vehicle_type = "motorcycle"
    wheels = 2
    fuel_type = "gasoline"
    
    def get_vehicle_type(self):
        return self.vehicle_type

class Truck(WheeledVehicle):
    vehicle_type = "truck"
    wheels = 6
    fuel_type = "diesel"
    
    def get_vehicle_type(self):
        return self.vehicle_type

class Boat(Vehicle):
    vehicle_type = "boat"
    propulsion = "motor"
    fuel_type = "gasoline"
    
    def get_vehicle_type(self):
        return self.vehicle_type
```

With this structure, you can now use the ClassFamily methods to query and instantiate vehicles:

```python
# Find all vehicle types
vehicle_types = [cls.vehicle_type for cls in Vehicle.family_members('vehicle_type')]
print(f"Available vehicle types: {', '.join(vehicle_types)}")
# Output: Available vehicle types: car, electric car, motorcycle, truck, boat

# Find a specific vehicle by type
car_class = Vehicle.family_member('vehicle_type', 'car')
my_car = car_class(color="red", year=2023)
print(my_car.get_description())  # Output: 2023 red car

# Find all vehicles with a specific fuel type
electric_vehicles = Vehicle.family_members('fuel_type', 'electricity')
for cls in electric_vehicles:
    vehicle = cls(color="blue", year=2023)
    print(f"{vehicle.get_description()} runs on {cls.fuel_type}")
# Output: 2023 blue electric car runs on electricity

# Find all vehicles with a specific number of wheels
two_wheelers = Vehicle.family_members('wheels', 2)
for cls in two_wheelers:
    print(f"A {cls.vehicle_type} has {cls.wheels} wheels")
# Output: A motorcycle has 2 wheels
```

This example demonstrates how ClassFamily allows you to:

1. Organize related classes in a hierarchy
2. Query classes based on their attributes
3. Instantiate classes dynamically without direct references
4. Handle intermediate abstract classes (like WheeledVehicle) that don't define all attributes

## Implementation Details

The ClassFamily system works by:

1. Tracking all subclasses of the atriarch class
2. Storing them in a list property called `family`
3. Providing methods to query this list based on class attributes

When querying attributes, ClassFamily is careful to only look at attributes defined directly on each class (not inherited attributes). This allows intermediate abstract classes to exist in the hierarchy without affecting the lookup system.

## Creating Your Own Class Family

To create your own class family:

1. Create a base class that inherits from ClassFamily
2. Define subclasses that inherit from this base class
3. Use the family_member() and family_members() methods to query the family

This pattern is particularly useful when you have a collection of related types that you want to be able to look up dynamically, without having to maintain explicit registries or mappings.
