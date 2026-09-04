from locust import HttpUser, task, between


class RevoShopUser(HttpUser):
    wait_time = between(1, 3)

    product_id = 1
    user_id = 4
    order_id = None

    @task
    def user_journey(self):
        # 1. GET all products
        with self.client.get(
            "/products",
            name="GET /products"
        ) as response:

            if response.status_code != 200:
                return

            products = response.json()

            if not products:
                return

            # Ambil product pertama
            self.product_id = products[0]["id"]

        # 2. GET single product
        with self.client.get(
            f"/products/{self.product_id}",
            name="GET /products/<id>"
        ) as response:

            if response.status_code != 200:
                return

        # 3. POST new order
        order_data = {
            "user_id": self.user_id,
            "items": [
                {
                    "product_id": self.product_id,
                    "quantity": 1
                }
            ]
        }

        with self.client.post(
            "/orders",
            json=order_data,
            name="POST /orders"
        ) as response:

            if response.status_code not in [200, 201]:
                return

            order = response.json()

            self.order_id = order.get("id")

            if not self.order_id:
                return

        # 4. GET created order
        with self.client.get(
            f"/orders/{self.order_id}",
            name="GET /orders/<id>"
        ) as response:

            if response.status_code != 200:
                return