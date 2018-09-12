import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying, car_type):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
        self.car_type = car_type

    def get_photo_file_ext(self):
        _, root = os.path.splitext(self.photo_file_name)
        return root


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, car_type, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, car_type, body_width=None, body_height=None, body_length=None):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.body_width = body_width
        self.body_height = body_height
        self.body_length = body_length

    def get_body_volume(self):
        return self.body_width*self.body_height*self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, car_type, extra):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                if row[0] == 'car':
                    vehicle = Car(row[1], row[3], float(row[5]), row[0], int(row[2]))
                    car_list.append(vehicle)
                if row[0] == 'truck':
                    try:
                        body_whl = [float(x) for x in row[4].split('x')]
                    except:
                        body_whl = [None, None, None]
                    vehicle = Truck(row[1], row[3], float(row[5]), row[0], body_whl[0], body_whl[1], body_whl[2])
                    car_list.append(vehicle)
                if row[0] == 'spec_machine':
                    vehicle = SpecMachine(row[1], row[3], float(row[5]), row[0], row[6])
                    car_list.append(vehicle)
            except Exception as e:
                pass

    return car_list


#car1 = CarBase('Toyota', '123.jpeg', 10, 'Car')
#print(car1.get_photo_file_ext())
#print (get_car_list('coursera_week3_cars.csv'))

