import grpc
from concurrent import futures
import inventory_pb2
import inventory_pb2_grpc

# Создаем класс, который обрабатывает запросы от клиентов
class InventoryControlServicer(inventory_pb2_grpc.InventoryControlServicer):
    # Вызываем этот метод, когда клиент отправляет нам товары
    def BulkUpdateStock(self, request_iterator, context):
        print("Начало обработки потока обновлений от клиента...")
        items_processed = 0
        # По одному принимаем товары, которые присылает клиент
        for stock_item in request_iterator:
            items_processed += 1
            print(f"Обработан товар: ID={stock_item.item_id}, Название='{stock_item.name}', Новое количество={stock_item.new_quantity}")
        # Когда все товары получены, отправляем клиенту итоговый ответ
        summary = inventory_pb2.BulkUpdateSummary(
            items_processed=items_processed,
            message=f"Успешно обновлено {items_processed} позиций.",
            success=True
        )
        print(f"Обработка потока завершена. Итого: {items_processed} позиций.")
        return summary

def serve():
    # Создаём сервер, который может работать с 10 клиентами одновременно
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Определяем какой класс серверу надо использовать для обработки запросов
    inventory_pb2_grpc.add_InventoryControlServicer_to_server(
        InventoryControlServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Сервер InventoryControl запущен на порту 50051...")
    server.wait_for_termination()

if __name__ == '__main__':

    serve()
