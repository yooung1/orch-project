from datetime import datetime
from croniter import croniter

def check_trigger_time(list_of_triggers_and_ids, list_of_queue_scripts, list_of_sended_items):
    """Verifica se a próxima execução do cron é hoje e a que horas será."""
    print("check_trigger_time")
    base = datetime.now()  
    current_time = datetime.now().strftime("%H:%M")
    try:
        for i in list_of_triggers_and_ids:  # Itera pelos triggers e IDs
            cron = croniter(i[1], base)  # Calcula o próximo horário baseado na expressão cron
            current_run = cron.get_next(datetime).strftime("%H:%M")  # Obtém o próximo horário de execução
            current_item = i[0]  # Obtém o ID do item
            # Se o horário atual bater e o item não foi enviado ainda, adiciona à fila
            if current_run == current_time and current_item not in list_of_sended_items:
                list_of_queue_scripts.append(str(current_item))
                list_of_sended_items.append(str(current_item))  # Marca o item como enviado
        return list_of_queue_scripts, list_of_sended_items
    except Exception as e:
        print(e)