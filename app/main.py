import os
import json
from app.customer import Customer
from app.shop import Shop
from app.utils import distance, travel_cost


def shop_trip() -> None:
    # Загружаем конфиг
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")
    with open(config_path) as f:
        config = json.load(f)

    config_fuel_cost = config["FUEL_PRICE"]

    # Создаем объекты клиентов и магазинов
    customers = [Customer(**c) for c in config["customers"]]
    shops = [Shop(**s) for s in config["shops"]]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        shop_costs = []

        # Рассчитываем стоимость поездки для каждого магазина
        for shop in shops:
            # Проверяем, есть ли все нужные товары в магазине
            if all(item in shop.products for item in customer.product_cart):
                dist_to_shop = distance(customer.location, shop.location)
                dist_home = distance(shop.location, customer.location)
                fuel_cost = travel_cost(
                    dist_to_shop, customer.car, config_fuel_cost
                )
                return_cost = travel_cost(
                    dist_home, customer.car, config_fuel_cost
                )
                products_cost = sum(
                    shop.products[item] * qty
                    for item, qty in customer.product_cart.items()
                )
                total_cost = round(fuel_cost + return_cost + products_cost, 2)
                shop_costs.append(
                    (
                        total_cost,
                        shop,
                        fuel_cost,
                        return_cost,
                        products_cost
                    )
                )
                print(
                    f"{customer.name}'s "
                    f"trip to the {shop.name} costs {total_cost}")
            else:
                print(
                    f"{customer.name} "
                    f"cannot buy all products in {shop.name}"
                )
        # Выбираем магазин с минимальной стоимостью
        if not shop_costs:
            print(
                f"{customer.name} "
                f"doesn't have enough money to make a purchase in any shop"
            )
            continue

        shop_costs.sort(key=lambda x: x[0])
        (
            cheapest_total,
            chosen_shop,
            fuel_cost,
            return_cost,
            products_cost
        ) = shop_costs[0]

        if customer.money >= cheapest_total:
            print(f"{customer.name} rides to {chosen_shop.name}\n")
            # customer.update_location(chosen_shop.location)
            chosen_shop.print_receipt(customer.name, customer.product_cart)

            customer.money = customer.money - cheapest_total

            print(f"{customer.name} rides home")
            # customer.update_location(
            # [customer.location[0], customer.location[1]]
            # )  # возвращение домой
            print(f"{customer.name} now has {customer.money} dollars\n")
        else:
            print(
                f"{customer.name} "
                "doesn't have enough money to make a purchase in any shop"
            )


shop_trip()
