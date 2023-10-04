# product_name = "rower"
# price = 300
# amount = 2
#
# warehouses = {}
#
# warehouses[product_name] = {
#     "price": price,
#     "amount": amount
# }
#
# warehouses["boat"] = {
#     "price": price,
#     "amount": amount
# }
#
# print(warehouses)
#
# print(warehouses["boat"])
# print(warehouses["boat"]["price"])

# my_dict = {
#     "kwota": 300,
#     "ilość": 4
# }
#
# my_list = []
#
# print(type(my_dict.keys()), my_dict.items())
#
# for key in my_dict.keys():
#     print(key)
#
# for value in my_dict.values():
#     print(value)
#
# for key, value in my_dict.items():
#     print(key, value)

# print(type(my_dict), my_dict)
# print(type(enumerate(my_list)), enumerate(my_list))
#
# for index, elements in enumerate(my_dict):
#     print(index, elements)


# operation_history = []
#
# operation_history.append({"Saldo":
#     (
#         f"Kwota operacji: 300",
#         f"Stan konta po operacji: 500"
#     )})
#
# from datetime import date, datetime
#
# present_date = datetime.now()
# formatted_date = present_date.strftime("%d-%m-%Y %H:%M:%S")
#
# print(formatted_date)

# # Wyświetla historię operacji
# print("Historia operacji:")
# for index, operation in enumerate(operation_history):
#     for key, value in operation.items():
#         print(f"{index + 1}. {key}:")
#         print(value)

# print(f"{index + 1}. {operation}")

# for key, value in operation.items():
#     print(f"{index + 1}. {key}:"
#           f"{value}")