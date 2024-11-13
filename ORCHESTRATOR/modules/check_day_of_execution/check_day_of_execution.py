from datetime import datetime
from croniter import croniter

def check_day_of_execution(list_of_triggers_and_ids):
    """Verifica todos os itens na lista e remove os que não têm execução hoje."""
    print("check_day_of_execution")
    base = datetime.now()  # Obtém a data e hora atual
    try:
        for i in list_of_triggers_and_ids[:]:  # Itera pelos triggers e IDs (fazendo cópia da lista)
            cron = croniter(i[1], base)  # Calcula o próximo horário baseado na expressão cron
            next_run = cron.get_next(datetime)  # Obtém o próximo horário de execução
            # Verifica se o próximo horário de execução é hoje
            if next_run.date() != base.date():  # Se não for para hoje, remove da lista
                list_of_triggers_and_ids.remove(i)
        return list_of_triggers_and_ids
    except Exception as e:
        print(f"Erro: {e}")