from bots.bot import Bot
import asyncio


async def run_queue_scripts(list_of_queue_scripts):
    """Função assíncrona para processar os itens da fila."""
    print("run_queue_scripts")
    id = list_of_queue_scripts.pop(0)  # Pega o primeiro ID da fila
    try:
        await Bot(id)  # Chama o método para processar o script com o ID
        print(f"{id} Finalizado")
    except Exception as e:
        print(f"Erro ao rodar o script com ID {id}: {e}")