from datetime import datetime
from json import dumps, loads

print("\n*** Prosty system księgowy/magazyn ***\n")

print("Witaj w programie księgowo-magazynowym.")


def give_operation_date():
    present_date = datetime.now()
    return present_date.strftime("%d-%m-%Y %H:%M:%S")


amount_in_account = 0  # Stan konta
warehouse = {}  # Słownik - magazyn
operation_history = []

# Odczytanie danych z plików
try:
    with open("data_amount_in_account.txt") as file_stream:
        amount_in_account = file_stream.readline()
except FileNotFoundError:
    print("Nie pobrano danych z pliku.")

try:
    amount_in_account = float(amount_in_account)
except ValueError:
    print("Niepoprawne dane wejściowe.")

try:
    with open("warehouse.json") as file_stream:
        warehouse = loads(file_stream.read())
except FileNotFoundError:
    print("Nie pobrano danych z pliku.")

try:
    with open("operation_history.json") as file_stream:
        operation_history = loads(file_stream.read())
except FileNotFoundError:
    print("Nie pobrano danych z pliku.")

while True:
    menu_command = input("""
Wybierz jedno z poniższych poleceń (możesz wpisać także numer):
1 - saldo
2 - sprzedaż
3 - zakup
4 - konto
5 - lista
6 - magazyn
7 - przegląd
8 - koniec
""")

    if menu_command == "1" or menu_command == "saldo":
        # Dodanie lub odjęcie wartości od kwoty na koncie
        difference_in_account = input("Podaj kwotę do dodania lub odjęcia z konta: ")
        try:
            difference_in_account = float(difference_in_account)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue

        amount_in_account = amount_in_account + difference_in_account

        # Aktualizacja historii operacji
        operation_history.append({"Nazwa operacji": "Saldo",
                                  "Opis operacji":
                                      (
                                          f"Kwota operacji: {difference_in_account}\n"
                                          f"Stan konta po operacji: {amount_in_account}"
                                      ),
                                  "Data operacji": give_operation_date()})

    elif menu_command == "2" or menu_command == "sprzedaż":
        # Wprowadzenie danych
        product_to_sell_name = input("Podaj nazwę produktu, który chcesz sprzedać: ")
        if product_to_sell_name not in warehouse:
            print("Produkt, który chcesz sprzedać nie występuje w magazynie.")
            continue
        product_to_sell_price = input("Podaj cenę sprzedaży danego produktu: ")
        try:
            product_to_sell_price = float(product_to_sell_price)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue
        product_to_sell_amount = input("Podaj ilość produktów do sprzedania: ")
        try:
            product_to_sell_amount = int(product_to_sell_amount)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue

        # Odjęcie z magazynu sprzedawanej ilości towaru
        warehouse[product_to_sell_name]["amount"] = \
            warehouse[product_to_sell_name]["amount"] - product_to_sell_amount

        # Sprawdzenie czy jest wystarczająca ilość towaru w magazynie
        if warehouse[product_to_sell_name]["amount"] < 0:
            product_to_sell_amount = product_to_sell_amount + \
                                     warehouse[product_to_sell_name]["amount"]
            print(f"Brak wystarczającej ilości danego towaru w magazynie. "
                  f"Sprzedano {product_to_sell_amount} sztuk.")
            warehouse[product_to_sell_name]["amount"] = 0

        # Dodanie do konta kwoty sprzedaży
        amount_in_account = amount_in_account + (product_to_sell_price * product_to_sell_amount)

        # Jeśli ilość danego towaru = 0 usunięcie towaru z kartoteki magazynu
        if warehouse[product_to_sell_name]["amount"] == 0:
            del warehouse[product_to_sell_name]

        # Aktualizacja historii operacji
        operation_history.append({"Nazwa operacji": "Sprzedaż",
                                  "Opis operacji":
                                      (
                                          f"Nazwa sprzedanego produktu: {product_to_sell_name}\n"
                                          f"Kwota sprzedaży za jeden produkt: {product_to_sell_price}\n"
                                          f"Ilość sprzedanych produktów: {product_to_sell_amount}\n"
                                          f"Stan konta po operacji: {amount_in_account}"
                                      ),
                                  "Data operacji": give_operation_date()})

    elif menu_command == "3" or menu_command == "zakup":
        # Wprowadzenie danych
        product_to_buy_name = input("Podaj nazwę zakupionego produktu: ")
        if product_to_buy_name in warehouse:
            # noinspection PyTypeChecker
            product_to_buy_price = warehouse[product_to_buy_name]["price"]
            print("Cena produktu wynosi: ", warehouse[product_to_buy_name]["price"])
            user_answer = input("Chcesz ją nadpisać? y/n: ")
            if user_answer == "y":
                product_to_buy_price = input("Podaj cenę zakupionego "
                                             "produktu (pojedynczego): ")
            elif user_answer == "n":
                pass
            else:
                print("Niewłaściwa komenda.")
        else:
            product_to_buy_price = input("Podaj cenę zakupionego "
                                         "produktu (pojedynczego): ")
        try:
            product_to_buy_price = float(product_to_buy_price)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue
        product_to_buy_amount = input("Podaj ilość zakupionych produktów: ")
        try:
            product_to_buy_amount = int(product_to_buy_amount)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue

        # Sprawdzenie wystarczających środków na końcie i aktualizacja stanu konta
        if (product_to_buy_price * product_to_buy_amount) > amount_in_account:
            print("Koszt zakupu większy od stanu konta. Operacja niemożliwa.")
            continue
        else:
            amount_in_account = amount_in_account - \
                                (product_to_buy_price * product_to_buy_amount)

        #  Sprawdzenie czy dany produkt jest już w magazynie.
        #  Jeśli tak, zwiększenie jego ilości.
        if product_to_buy_name in warehouse:
            warehouse[product_to_buy_name]["amount"] = warehouse[product_to_buy_name]["amount"] \
                                                       + product_to_buy_amount
        else:
            # Dodanie produktu do słownika magazynu
            warehouse[product_to_buy_name] = {
                "price": product_to_buy_price,
                "amount": product_to_buy_amount
            }

        # Aktualizacja historii operacji
        operation_history.append({"Nazwa operacji": "Zakup",
                                  "Opis operacji":
                                      (
                                          f"Nazwa zakupionego produktu: {product_to_buy_name}\n"
                                          f"Kwota zakupu za jeden produkt: {product_to_buy_price}\n"
                                          f"Ilość zakupionych produktów: {product_to_buy_amount}\n"
                                          f"Stan konta po operacji: {amount_in_account}"
                                      ),
                                  "Data operacji": give_operation_date()})

    elif menu_command == "4" or menu_command == "konto":
        # Wyświetla aktualny stan konta
        print("Kwota na koncie wynosi: ", amount_in_account)

    elif menu_command == "5" or menu_command == "lista":
        # Wyświetla całkowity stan magazynu
        print("Stan magazynu: ")
        for index, name in enumerate(warehouse):
            print(f"{index + 1}. {name.capitalize()}:\n"
                  f"  cena: {warehouse[name]['price']}\n"
                  f"  ilość: {warehouse[name]['amount']}")

    elif menu_command == "6" or menu_command == "magazyn":
        # Wyświetla ilość wskazanego produktu
        product_to_display = input("Podaj nazwę produktu do wyświetlenia: ")
        if product_to_display not in warehouse:
            print("Nie ma w magazynie produktu o podanej nazwie.")
            continue
        print(f"Ilość powyższego produktu w magazynie to "
              f"{warehouse[product_to_display]['amount']} szt.")

    elif menu_command == "7" or menu_command == "przegląd":
        # # Przykładowy wpis
        # operation_history = [{"Nazwa operacji": "Saldo",
        #                       "Opis operacji":
        #                           (
        #                               f"Kwota operacji: 3000\n"
        #                               f"Stan konta po operacji: 3000"
        #                           ),
        #                       "Data operacji": "26.09.2023 21:56:23"},
        #
        #                      {"Nazwa operacji": "Sprzedaż",
        #                       "Opis operacji":
        #                           (
        #                               f"Nazwa sprzedanego produktu: rower\n"
        #                               f"Kwota sprzedaży za jeden produkt: 400\n"
        #                               f"Ilość sprzedanych produktów: 4\n"
        #                               f"Stan konta po operacji: 1400"
        #                           ),
        #                       "Data operacji": "26.09.2023 21:57:35"}
        #                      ]

        # Pobiera zakres wyświetlenia od użytkownika
        print(f"Odnotowano {len(operation_history)} operacji w historii.")

        if len(operation_history) == 0:
            break

        display_history_start_number = input("Podaj początkowy indeks historii operacji: ")
        if display_history_start_number == "":
            display_history_start_number = 1
        try:
            display_history_start_number = int(display_history_start_number)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue
        if display_history_start_number < 1 or display_history_start_number > len(operation_history):
            print(f"Wybrano wartość spoza zakresu. Należy wpisać wartość z przedziału od 1 do {len(operation_history)}")
            continue

        display_history_end_number = input("Podaj końcowy indeks historii operacji: ")
        if display_history_end_number == "":
            display_history_end_number = len(operation_history)
        try:
            display_history_end_number = int(display_history_end_number)
        except ValueError:
            print("Błąd - Należy podać liczbę.")
            continue
        if display_history_end_number < 1 or display_history_end_number > len(operation_history):
            print(f"Wybrano wartość spoza zakresu. Należy wpisać wartość z przedziału od 1 do {len(operation_history)}")
            continue

        # Wyświetla historię operacji
        print("Historia operacji:")
        for index, operation in enumerate(operation_history):
            if index in range(display_history_start_number - 1, display_history_end_number):
                indent_date_width = 60 - len(operation["Nazwa operacji"])
                justify_operation_date = str(operation["Data operacji"].rjust(indent_date_width))
                print(f'{index + 1}. {operation["Nazwa operacji"]} {justify_operation_date}\n'
                      f'{operation["Opis operacji"]}')

    elif menu_command == "8" or menu_command == "koniec":
        with open("data_amount_in_account.txt", "w") as file_stream:
            file_stream.write(str(amount_in_account))

        with open("warehouse.json", "w") as file_stream:
            file_stream.write(dumps(warehouse))

        with open("operation_history.json", "w") as file_stream:
            file_stream.write(dumps(operation_history))

        print("Poporawnie zapisano dane.")
        break

    else:
        pass
