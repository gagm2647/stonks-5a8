from square_sdk import SquareAPI

if __name__ == "__main__":

  api = SquareAPI()
  cost = api.getPriceOf("Test_object1")
  print(cost)
  newcost = int(cost) + 50
  api.setPriceOf("Test_object1", newcost)
  cost = api.getPriceOf("Test_object1")
  print(cost)