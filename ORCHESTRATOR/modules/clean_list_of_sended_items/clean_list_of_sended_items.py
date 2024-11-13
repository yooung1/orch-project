from datetime import datetime

async def clean_list_of_sended_items(list_of_sended_items):
    print("CLEANING LIST OF SENDED ITENS")
    date = datetime.now().strftime("%H:%M")  # Obtém a hora atual
    if date == "00:01":  # Condição para limpar a lista após 00:00
        print("clean_list_of_sended_items")
        return list_of_sended_items.clear()  # Limpa a lista de itens enviados
        