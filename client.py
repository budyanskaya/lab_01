import grpc
import inventory_pb2
import inventory_pb2_grpc

def generate_stock_updates():
    stock_updates = [
        {"item_id": "SKU001", "name": "Ноутбук", "new_quantity": 15},
        {"item_id": "SKU002", "name": "Монитор", "new_quantity": 8},
    ]
    
    for item in stock_updates:
        yield inventory_pb2.StockItem(
            item_id=item["item_id"],
            name=item["name"],
            new_quantity=item["new_quantity"]
        )

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryControlStub(channel)
        print("Отправка данных серверу...")
        
        response = stub.BulkUpdateStock(generate_stock_updates())
        print(f"Результат: {response.message}")

if __name__ == '__main__':
    run()