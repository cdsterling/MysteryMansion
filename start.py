import random
  # we will use random to generate our items in random rooms maybe to generate secret locations


mansion_rooms = [
  {
    "name":"Study",
    "x" : 0,
    "y" : 0,
  },
  {
    "name": "Loungue",
    "x": 4,
    "y": 0,
  },
  {
    "name": "Library",
    "x": 0,
    "y": 2,
  },
  {
    "name": "Stairs",
    "x": 2,
    "y": 2,
  },
  {
    "name": "Dining Room",
    "x": 4,
    "y": 2,
  },
  {
    "name": "Conservatory" ,
    "x": 0,
    "y": 4,
  },
  {
    "name": "Ball Room",
    "x": 2,
    "y": 4,
  },
  {
    "name": "Kitchen",
    "x": 4,
    "y": 4,
  }

]

def next_room_generator():
  for nextRoom in mansion_rooms:
    yield nextRoom

class coordinate:
  def __init__(self, x_coord, y_coord):
    self.x = x_coord
    self.y = y_coord

  def is_matching_position(self, other_coord):
    if self.x == other_coord.x and self.y == other_coord.y:
      return True
    else:
      return False

  def print_coordinates(self):
    print("X:", self.x, "Y:", self.y, end=" ")
  



#think of a room as a generic box of indermanite size located at a cooriinate on a grid
class room: 
  def __init__(self, roomDetails, xval, yval, doors_locked=False):
    self.name = roomDetails["name"]
    self.coordinate = coordinate(xval, yval)
    self.item = None
    self.has_secret_path = None
    self.secret_path_destination = None
    self.doorslocked= doors_locked

  def print_room(self):
    print("----", self.name, "----")

  def get_room_initial(self):
    return self.name[0]


  def inspect_room(self):
    print("looking around the", self.name)
    if self.item:
      print("---->oh snap, you found a", self.item)
    else:
      print("---->nothing much to see here, just a regular ol", self.name)
      
  def search_for_secrets_room(self):
    returnItem = None
    if self.has_secret_path:
      print("you found a secret path")
      print("looks like this secret path leads to ", self.secret_path_destination)
    else:
      print("couldn't find any secret paths here")

    if self.item:
      print("oh snap! you found an item")
      print("whoa, it looks like you found the", self.item)
      returnItem = self.item
      self.item = None
      print("taking the", returnItem, "and puting it in your inventory")

class hallway(room):
  def __init__(self, xval, yval):
    self.name = "Hallway"
    self.coord = coordinate(xval, yval)

# think of a mansion as a 2d matrix of rooms and Hallways between rooms
class mansion:
  
  def __init__(self, ListOfRooms):
    #we add 1 room to be the entryway, this is where the 
    # player spawns and is always at coordinate (0,0)
    number_of_rooms = len(ListOfRooms) +1 

    if number_of_rooms % 5 == 0:
      print("5 width matrix")
      self.x_width = 10
      self.y_width = (number_of_rooms // 5) *2
    elif number_of_rooms %4 == 0:
      print("4 width matrix")
      self.x_width = 8
      self.y_width = (number_of_rooms // 4) *2
    elif number_of_rooms % 3 == 0:
      print("3 width matrix")
      self.x_width = 6
      self.y_width = (number_of_rooms // 3) *2
    else:
      room_overage = number_of_rooms % 3
      for num in range(room_overage):
        del ListOfRooms[len(ListOfRooms) -1] 
      
      number_of_rooms = len(ListOfRooms) +1 
      self.x_width = 6
      self.y_width = (number_of_rooms // 4) *2
    
    print("number of rooms", number_of_rooms)
    print("---xwidth:",self.x_width, "  ywidth", self.y_width)
  
    roomGen = next_room_generator()
    self.layout = []
    for i in range(self.y_width):
      self.layout.append([])

    print("printing layout")
    print(self.layout)
    for yval in range(self.y_width):
      for xval in range(self.x_width):
        if yval %2 == 0: #rooms are on even y values 
          
          if xval == 0 and yval == 0: #special case for initial entryway room
            print("---Adding Entryway at [", xval,"][",yval,"]")
            self.layout[xval].append(
              room(
                {
                  "name":"Entryway"
                },
                xval,
                yval
              )
            )
          elif xval %2 == 0: #rooms are on even x values
            print("---Adding newRoom at[", xval,"][",yval,"]")
            self.layout[xval].append(
              room(
                next(roomGen), xval, yval
              )
            )
          else: #hallways are on odd x values
            print("---Adding hallway at[", xval,"][",yval,"]")
            self.layout[xval].append(
              hallway(xval, yval)
            )
        
        else: #odd yvals are always hallways
          print("---Adding hallway at[", xval,"][",yval,"]")
          self.layout[xval].append(
            hallway(xval, yval)
          )
           

  def print_mansion(self):
    for yval in range(self.y_width):
      for xval in range(self.x_width):
        if xval == 0:
          print("|", end="")
        print(self.layout[xval][yval].get_room_initial()+"|", end="" )
        if xval == self.x_width -1:
          print("")

  def which_room(self, mansion_guest):
    guest_x = mansion_guest.coord.x
    guest_y = mansion_guest.coord.y
    return self[guest_x][guest_y].name

  def look_at_location(self, xval,yval):
    return self[xval][yval].name

  def print_suroundings(self, mansion_guest):
    guest_x = mansion_guest.coord.x
    guest_y = mansion_guest.coord.y
    guest_location = self.which_room(mansion_guest)

    if guest_location =="Hallway":
      print("you are in the Hallway")
      #first look North
      if guest_y == 0:
        print("North of you there is an impenetrable wall")
      else:
        print("North of you there is", self.look_at_location(guest_x, guest_y-1))

      #then look East
      if guest_x == 0:
        print("East of you there is an impenetrable wall")
      else:
        print("East of you there is", self.look_at_location(guest_x-1, guest_y))
      # then look south
      if guest_y == self.y_width-1:
        print("South of you there is an impenetrable wall")
      else:
        print("South of you there is", self.look_at_location(guest_x, guest_y+1))
      # then look west      
      if guest_x == self.x_width-1:
        print("West of you there is an impenetrable wall")
      else:
        print("West of you there is", self.look_at_location(guest_x+1, guest_y))
    else:
      print("You are inside of the" ,guest_location)
    


    






class player:
  def __init__(self):
    self.inventory = []
    # Player always starts in the entryway at (0,0)
    self.coord = coordinate(0, 0)

  def print_player_details(self, house):
    self.print_location(house)
    if len(self.inventory) > 0:
      print("items in inventory:")
      for item in inventory:
        print("--", item)
    else:
      print("no items in your inventory")

  def print_location(self, house):
    for location in house:
      if self.coord.is_matching_position(location.coord):
        print("you are in the:", location.name)
        return
    print("you are in the: Hallway")
    self.coord.print_coordinates()
  
    


  

def main():
  print("starting up main")
  #set up my mansion
  MysteryMansion = mansion(mansion_rooms)

  MysteryMansion.print_mansion()
  chad = player()

  #chad.print_player_details(mansion)


if __name__ == "__main__":
  main()

  