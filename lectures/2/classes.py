class Point():
    def __init__(self,input1,input2 ): # method which starts when class is created, (self - references the object we are dealing (like this->x in Java), x - )
        self.x = input1
        self.y = input2


#p = Point(2,8)
#print(p.x)
#print(p.y)


class Flight():
    def __init__(self,capacity):
        self.capacity = capacity 
        self.passengeres =[]
    

    def add_passenger(self, name):
        if not self.open_seats():
            return False
        
        self.passengeres.append(name)
        return True

    def open_seats(self):
        return self.capacity-len(self.passengeres)
        

flight = Flight(3)

people = ["Harry", "ron", "Hermiona", "Severus"]


for person in people: 
    success = flight.add_passenger(person)

    if success:
        print(f"Added{person} to the flight")
    else:
        print(f"Flight overbooked. Passegner {person} can't be added")



