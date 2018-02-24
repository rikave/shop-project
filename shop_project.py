from collections import OrderedDict
import time

class ItemClass(object):
   """Object of an item with various methods"""

   def __init__(self, name, quantity=0, price=0, reorder_point=0, reorder_quantity=0, delivery_time_left=0,
                delivery_time_full=0):
      # passable variables (on creation)
      self.name = name
      self.quantity = quantity
      self.price = price
      self.reorder_point = reorder_point           #ROP
      self.reorder_quantity = reorder_quantity     #ROQ
      self.delivery_time_left = delivery_time_left
      self.delivery_time_full = delivery_time_full
      # nonpassable variables (on creation)
      self.manual_order_quantity = 0   #should be set to 0 after the delivery is complete
      self.manual_delivery_left = 0

   def __repr__(self):
      print("\nRepresentation of stock item")
      print("=============================")
      print("{:<15}: {}".format("Name", self.name))
      print("{:<15}: {}".format("Quantity", self.quantity))
      print("{:<15}: {} zl".format("Price", self.price))
      print("{:<15}: {}".format("ROP", self.reorder_point))
      print("{:<15}: {}".format("ROQ", self.reorder_quantity))
      print("{:<15}: {} day(s)".format("Delivery time", self.delivery_time_full))
      print()


class StockClass(object):
   """Main stock which contains different methods to manage it"""

   def __init__(self):
      # stock_dict description
      # "name": { quantity, price, reorder_point, reorder_quantity, delivery_time_left(days), delivery_time_full(days) }
      self.stock_dict = { "banana":    ItemClass("banana", 22, 0.81, 15, 110, 1, 2),
                          "apple":     ItemClass("apple", 15, 0.50, 17, 112, 0, 2),
                          "carrot":    ItemClass("carrot", 5, 0.50, 10, 60, 0, 2),
                          "cucumber":  ItemClass("cucumber", 6, 3, 11, 62, 0, 2),
                          "tomato":    ItemClass("tomato", 7, 1, 10, 60, 0, 2),
                          "bread":     ItemClass("bread", 6, 2.50, 12, 15, 0, 1),
                          "milk":      ItemClass("milk", 4, 2.10, 15, 70, 0, 3)
      }
      self.stock_dict = OrderedDict(sorted(self.stock_dict.items()))

   def buy(self):
      print("Here's a list of our items:\n{}\n".format(", ".join(self.stock_dict.keys())))
      name = input("What would you like to buy? (one item at a time please) - ")

      if self.stock_dict.get(name):
         if self.stock_dict[name].quantity == 0:
            print("Sorry, {} is currently unavailable.".format(name))
            return
      else:
         print("'{}' is out of our offer or not inserted yet.".format(name))
         return

      print("We have {} available for {} zl/each. How much do you want? ".format( \
                                                   self.stock_dict[name].quantity, self.stock_dict[name].price))
      buy_quantity = input()
      try:
         buy_quantity = int(buy_quantity)
      except Exception as err:
         print("Next time insert a number")
         return
      available = self.stock_dict[name].quantity
      if available >= buy_quantity:
         self.stock_dict[name].quantity -= buy_quantity
         print("You bought: {} {} for {:.2f} zl.".format(buy_quantity, name, buy_quantity*self.stock_dict[name].price))
      else:
         print("Sorry, we have only {} of {}.".format(available, name))

   def return_item(self):
      name = input("What would you like to return? ")
      if self.stock_dict.get(name):
         return_qty = input("How much do you want to return? ")
         if return_qty.isdigit():
            self.stock_dict[name].quantity += int(return_qty)
            print("Added {} {} to our stock.".format(return_qty, name))
         else:
            print("Sorry, I expect a whole number. Try again.")
      else:
         print("We don't have such item. Make sure you typed the right name or try adding it to our store.")

   def order_manually(self):
      name = input("What do you want to order? ")
      if self.stock_dict.get(name):
         print("\nPlease, consider these values before ordering.")
         print("{:<15}{}".format("Name:", name))
         print("{:<15}{}".format("Quantity:", self.stock_dict[name].quantity))
         print("{:<15}{}".format("ROP:", self.stock_dict[name].reorder_point))
         print("{:<15}{}".format("ROQ:", self.stock_dict[name].reorder_quantity))
         print("{:<15}{} day(s) (AUTO)".format("Next delivery:", self.stock_dict[name].delivery_time_left))
         print("{:<15}{} in {} day(s) (MANUAL)\n".format("", self.stock_dict[name].manual_order_quantity,
                                                     self.stock_dict[name].manual_delivery_left))

         if self.stock_dict[name].manual_delivery_left:
            print("But wait...it's already ordered manually. Contact your boss if you need another delivery.")
            return
         order_qty = input("How much do you want to order? ")
         if order_qty.isdigit():
            self.stock_dict[name].manual_order_quantity = int(order_qty)
            self.stock_dict[name].manual_delivery_left = self.stock_dict[name].delivery_time_full
            print("Your order should arrive in {} day(s).".format(self.stock_dict[name].manual_delivery_left))

         else:
            print("Sorry, I expect a whole number. Try again.")
      else:
         print("We don't have such item. Make sure you typed the right name or try adding it to our store.")

   def delivery_check(self):
      item_name = input("Delivery of which item do you want to check? ")
      if self.stock_dict.get(item_name):
         if self.stock_dict[item_name].delivery_time_left:
            print("{} {} should be delivered in {} day(s). (AUTO)".format(
                  self.stock_dict[item_name].reorder_quantity, item_name,
                  self.stock_dict[item_name].delivery_time_left))
         else:
            print("{} is not automatically ordered.".format(item_name.capitalize()))
         if self.stock_dict[item_name].manual_delivery_left:
            print("{} {} should be delivered in {} day(s). (MANUAL)".format(
                  self.stock_dict[item_name].manual_order_quantity,
                  item_name,
                  self.stock_dict[item_name].manual_delivery_left))
      else:
         print("{} is out of our offer or not inserted yet.".format(item_name.capitalize()))

   def list_items(self):
      print("\n{:<15}|| {:>3}".format("Name", "Quantity"))
      print("============================")
      for name in self.stock_dict:
         print("{:<15}||{:>7}".format(name, self.stock_dict[name].quantity))

   def add_item(self):
      print("add item")

   def edit_item(self):
      name = input("Which item do you want to edit? ")
      params = "quantity, price, reorder_point, reorder_quantity, delivery_time_left, delivery_time_full"
      if name in self.stock_dict.keys():
         self.stock_dict[name].__repr__()
         methods = {"price": self.stock_dict[name].price}
         parameter = input("Which parameter do you want to change?\n"
                           "quantity, price, reorder_point, reorder_quantity, delivery_time_left, delivery_time_full ")
         if parameter in ("quantity", "price", "reorder_point", "reorder_quantity", "delivery_time_left",
                          "delivery_time_full"):
            print(getattr(self.stock_dict[name],parameter))
            print(methods[parameter])
         else:
            print("No such parameter.")
      else:
         print("No such item.")

   def delete_item(self):
      print("Warning! You are about to completely delete an item from our stock.\n"
            "===================================================================")
      time.sleep(1)
      confirmation = input("Are you sure that you want to delete an item? yes/no - ")
      if confirmation == "yes":
         name = input("Which item do you want to delete? ")
         if self.stock_dict.get(name):
            del self.stock_dict[name]
         elif name == "":
            print("You didn't delete anything. We're leaving it as it was.")
         else:
            print("Sorry, '{}' is not in our inventory. Maybe you've already deleted it?".format(name))
      elif confirmation == "no":
         print("Uhh, that's why this assertion is here.")
      else:
         print("Looks like you've changed your mind.")

   def exit(self):
      raise SystemExit("Exiting...")


def menu(user_choice):

   actions = {
            "1": "buy",
            "2": "return_item",
            "3": "order_manually",
            "4": "delivery_check",
            "5": "list_items",
            "6": "add_item",
            "7": "edit_item",
            "8": "delete_item",
            "9": "exit"
   }

   try:
      method = getattr(stock, actions[user_choice], "nothing")
      method()
   except Exception as err:
      print("{}\nInvalid input".format(err))



### MAIN ###
if __name__ == "__main__":
   stock = StockClass()
   first_visit = 1

   while True:
      if first_visit:
         print("\nWelcome to our store manager. What would you like to do?")
         first_visit = 0
      else:
         input("\nPress enter to continue.")
      print("\n" + "\n".join((
            "Pick an action:",
            "\t1 - Buy item",
            "\t2 - Return item",
            "\t3 - Order item manually",
            "\t4 - Check delivery time",
            "\t5 - List items",
            "\t6 - Add item",
            "\t7 - Edit item",
            "\t8 - Delete item",
            "\t9 - Exit",
            "Note: You can send empty text to cancel at any time"))
      )

      user_pick = input("\t")
      print()
      menu(user_pick)
