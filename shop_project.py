from collections import OrderedDict
import time


class ItemClass(object):
    """Object of an item with various methods"""

    def __init__(self, name, quantity=0, price=0, reorder_point=0,
                 reorder_quantity=0, delivery_time_left=0,
                 delivery_time_full=0):
        # passable variables (on creation)
        self.name = name
        self.quantity = quantity
        self.price = price
        self.reorder_point = reorder_point  # ROP
        self.reorder_quantity = reorder_quantity  # ROQ
        self.delivery_time_left = delivery_time_left
        self.delivery_time_full = delivery_time_full

        # nonpassable variables (on creation)
        self.manual_order_quantity = 0  # should be set to 0 after the delivery
        self.manual_delivery_left = 0

    def __str__(self):
        _indent = 15
        print("\nRepresentation of stock item")
        print("=============================")
        print("{0:<{1}}: {2}".format("Name", _indent, self.name))
        print("{0:<{1}}: {2}".format("Quantity", _indent, self.quantity))
        print("{0:<{1}}: {2} zl".format("Price", _indent, self.price))
        print("{0:<{1}}: {2}".format("ROP", _indent, self.reorder_point))
        print("{0:<{1}}: {2}".format("ROQ", _indent, self.reorder_quantity))
        print("{0:<{1}}: {2} day(s)".format("Delivery time", _indent,
                                            self.delivery_time_full))
        print()


class StockClass(object):
    """Main stock which contains different methods to manage it"""

    def __init__(self):
        """stock_dict description
            "name": { quantity, price, reorder_point, reorder_quantity,
                      delivery_time_left(days), delivery_time_full(days) }
        """
        self.stock_dict = {
            "banana": ItemClass("banana", 22, 0.81, 15, 110, 1, 2),
            "apple": ItemClass("apple", 15, 0.50, 17, 112, 0, 2),
            "carrot": ItemClass("carrot", 5, 0.50, 10, 60, 0, 2),
            "cucumber": ItemClass("cucumber", 6, 3, 11, 62, 0, 2),
            "tomato": ItemClass("tomato", 7, 1, 10, 60, 0, 2),
            "bread": ItemClass("bread", 6, 2.50, 12, 15, 0, 1),
            "milk": ItemClass("milk", 4, 2.10, 15, 70, 0, 3),
            }
        self.stock_dict = OrderedDict(sorted(self.stock_dict.items()))

    def buy(self):
        print("Here's a list of our items:\n{}\n".format(
            ", ".join(self.stock_dict.keys())))
        name = input(
            "What would you like to buy? (one item at a time please) - ")

        if not self.stock_dict.get(name):
            print("'{}' is out of our offer or not inserted yet.".format(name))
            return
        if self.stock_dict[name].quantity == 0:
            print("Sorry, {} is currently unavailable.".format(name))
            return

        print(
            "We have {} available for {} zl/each. How much do you want? " \
            .format(self.stock_dict[name].quantity, self.stock_dict[name].price)
        )
        try:
            buy_quantity = int(input())
        except ValueError:
            print("Next time insert a whole number")
            return

        available = self.stock_dict[name].quantity
        if available >= buy_quantity:
            self.stock_dict[name].quantity -= buy_quantity
            print("You bought: {} {} for {:.2f} zl.".format(
                buy_quantity, name, buy_quantity * self.stock_dict[name].price))
        else:
            print("Sorry, we have only {} of {}.".format(available, name))

    def return_item(self):
        name = input("What would you like to return? ")
        if not self.stock_dict.get(name):
            print("We don't have such item. Make sure you typed ",
                  "the right name or try adding it to our store.")
            return
        return_qty = input("How much do you want to return? ")
        if not return_qty.isdigit():
            print("Sorry, I expect a whole number. Try again.")
            return
        self.stock_dict[name].quantity += int(return_qty)
        print("Added {} {} to our stock.".format(return_qty, name))

    def order_manually(self):
        name = input("What do you want to order? ")
        if not self.stock_dict.get(name):
            print("We don't have such item. Make sure you typed the right ",
                  "name or try adding it to our store.")
            return

        _indent = 15
        print("\nPlease, consider these values before ordering.")
        print("{0:<{1}}{2}".format("Name:", _indent, name))
        print("{0:<{1}}{2}".format("Quantity:", _indent,
                                   self.stock_dict[name].quantity))
        print("{0:<{1}}{2}".format("ROP:", _indent,
                                   self.stock_dict[name].reorder_point))
        print("{0:<{1}}{2}".format("ROQ:", _indent,
                                   self.stock_dict[name].reorder_quantity))
        print("{0:<{1}}{2} day(s) (AUTO)".format(
            "Next delivery:", _indent,
            self.stock_dict[name].delivery_time_left)
        )
        print("{0:<{1}}{2} in {3} day(s) (MANUAL)\n".format(
            "",
            _indent,
            self.stock_dict[name].manual_order_quantity,
            self.stock_dict[name].manual_delivery_left),
        )

        if self.stock_dict[name].manual_delivery_left:
            print("But wait...it's already ordered manually. ",
                  "Contact your boss if you need another delivery.")
            return
        order_qty = input("How much do you want to order? ")
        if not order_qty.isdigit():
            print("Sorry, I expect a whole number. Try again.")
            return
        self.stock_dict[name].manual_order_quantity = int(order_qty)
        self.stock_dict[name].manual_delivery_left = \
            self.stock_dict[name].delivery_time_full
        print("Your order should arrive in {} day(s).".format(
            self.stock_dict[name].manual_delivery_left))


    def delivery_check(self):
        item_name = input("Delivery of which item do you want to check? ")
        if not self.stock_dict.get(item_name):
            print("{} is out of our offer or not inserted yet.".format(
                item_name.capitalize()))
            return
        if self.stock_dict[item_name].delivery_time_left:
            print("{} {} should be delivered in {} day(s). (AUTO)".format(
                self.stock_dict[item_name].reorder_quantity, item_name,
                self.stock_dict[item_name].delivery_time_left))
        else:
            print("{} is not automatically ordered.".format(
                item_name.capitalize()))
        if self.stock_dict[item_name].manual_delivery_left:
            print("{} {} should be delivered in {} day(s). (MANUAL)".format(
                self.stock_dict[item_name].manual_order_quantity,
                item_name, self.stock_dict[item_name].manual_delivery_left))


    def list_items(self):
        print("\n{:<15}|| {:>3}".format("Name", "Quantity"))
        print("============================")
        for name in self.stock_dict:
            print("{:<15}||{:>7}".format(name, self.stock_dict[name].quantity))

    def add_item(self):
        print("add item")

    def edit_item(self):
        name = input("Which item do you want to edit? ")
        if name not in self.stock_dict.keys():
            print("No such item.")
            return
        params = ["quantity", "price", "reorder_point", "reorder_quantity",
                  "delivery_time_left", "delivery_time_full",]
        self.stock_dict[name].__str__()
        parameter = input(
            "Available parameters: {}\n".format(", ".join(params)) +
            "Which parameter do you want to change? ")
        check_parameter = getattr(self.stock_dict[name], parameter, None)
        if check_parameter is None:
            print("No such parameter - '{}'".format(parameter))
            return
        print(
            "\nNote: You're about to edit {} of {}\n".format(parameter, name) +
            "Currently: {}\n".format(check_parameter)+
            "New value: ",
            end = ""
        )

        new_value = input()
        conversion_formats = [int, float]
        if parameter != "price":
            conversion_formats.pop()
        for method in conversion_formats:
            try:
                setattr(self.stock_dict[name], parameter, method(new_value))
                print("You've set {} of {} to {}.".format(parameter, name,
                                                         new_value))
                return
            except ValueError:
                pass
        print("Sorry, integer number is expected*.\n"
              "*for 'price' it could also be float.")

    def delete_item(self):
        print(
          "Warning! You are about to completely delete an item from our stock."
          "\n"
          "===================================================================")
        time.sleep(1)
        name = input("Which item do you want to delete? ")
        if self.stock_dict.get(name):
            confirmation = input(
                "Are you sure that you want to delete this item? yes/no - ")
            if confirmation == "yes":
                del self.stock_dict[name]
                print("You've deleted '{}'.".format(name))
            elif confirmation == "no":
                print("Uhh, that's why this assertion is here.")
            else:
                print("Looks like you've changed your mind.")
        elif name == "":
            print("You didn't delete anything. We're leaving it as it was.")
        else:
            print("Sorry, '{}' is not in our inventory. ".format(name) +
                  "Maybe you've already deleted it?")

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
