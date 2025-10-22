import grpc
import inventory_pb2
import inventory_pb2_grpc

# Функция, которая создаёт товары для отправки
def generate_stock_updates():
    stock_updates = [
        {"item_id": "SKU001", "name": "Ноутбук", "new_quantity": 15},
        {"item_id": "SKU002", "name": "Монитор", "new_quantity": 8},
    ]

    # По одному создаём и отправляем каждый товар
    for item in stock_updates:
        yield inventory_pb2.StockItem(
            item_id=item["item_id"],
            name=item["name"],
            new_quantity=item["new_quantity"]
        )

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        # Создаём объект для вызова методов сервера
        stub = inventory_pb2_grpc.InventoryControlStub(channel)
        print("Отправка данных серверу...")

        # Вызываем метод сервера и передаём ему наши товары
        response = stub.BulkUpdateStock(generate_stock_updates())
        print(f"Результат: {response.message}")

if __name__ == '__main__':

    run()
