import asyncio
import schedule
from datetime import datetime
from ORCHESTRATOR.modules.database_connection.database_connection import DatabaseConnection
from ORCHESTRATOR.modules.get_triggers_from_db.get_triggers_from_db import get_triggers_from_db
from ORCHESTRATOR.modules.check_day_of_execution.check_day_of_execution import check_day_of_execution
from ORCHESTRATOR.modules.check_trigger_time.check_trigger_time import check_trigger_time
from ORCHESTRATOR.modules.run_queue_scripts.run_queue_scripts import run_queue_scripts
from ORCHESTRATOR.modules.clean_list_of_sended_items.clean_list_of_sended_items import clean_list_of_sended_items


class Monitoring(DatabaseConnection):
    def __init__(self):
        print("INICIALIZANDO ATRIBUTOS")
        # Inicializa variáveis para armazenar os triggers, itens enviados, e fila de scripts
        self.list_of_triggers_and_ids = []  # Lista que vai armazenar triggers e IDs dos scripts
        self.list_of_sended_items = []  # Lista para armazenar os itens já enviados
        self.list_of_queue_scripts = []  # Fila de scripts que precisam ser rodados
        self.process_is_running = False  # Flag para verificar se algum processo já está rodando
        self.get_triggers_from_db() # Settar os triggers na execução do processo


    def get_triggers_from_db(self):
        self.list_of_triggers_and_ids = get_triggers_from_db(self.make_database_connection())
        self.check_day_of_execution()
        

    def check_day_of_execution(self):
        self.list_of_triggers_and_ids = check_day_of_execution(self.list_of_triggers_and_ids)
        

    def check_trigger_time(self):
        data = check_trigger_time(self.list_of_triggers_and_ids, self.list_of_queue_scripts, self.list_of_sended_items)
        self.list_of_queue_scripts = data[0]
        self.list_of_sended_items = data[1]

    # Função assíncrona para processar os itens da fila.
    async def run_queue_scripts(self):
        try:
            if not self.process_is_running and len(self.list_of_queue_scripts):
                self.process_is_running = True
                await run_queue_scripts(self.list_of_queue_scripts)
        finally:
            self.process_is_running = False
        # """Função assíncrona para processar os itens da fila."""
        # print("run_queue_scripts")
        # if not self.process_is_running and len(self.list_of_queue_scripts) > 0:  # Verifica se não há outro processo rodando e se há itens na fila
        #     self.process_is_running = True
        #     id = self.list_of_queue_scripts.pop(0)  # Pega o primeiro ID da fila
        #     try:
        #         await self.Bot(id)  # Chama o método para processar o script com o ID
        #         print(f"{id} Finalizado")
        #     except Exception as e:
        #         print(f"Erro ao rodar o script com ID {id}: {e}")
        #     finally:
        #         self.process_is_running = False

    # AQUI VAI ESTAR A LOGICA PARA RODAR O SCRIPT
    # PRECISO ADICIONAR ALGUNS METODOS A MAIS 
    # ONDE ELE VAI ACHAR O SCRIPT Q PRECISAR RODAR?
    # async def Bot(self, id):
    #     print("Bot")
    #     """Simula o processamento de um bot, rodando em segundo plano"""
    #     try:
    #         print(f"BOT {id} EXECUTADO")
            
    #         # Inicia o subprocess de forma assíncrona
    #         process = await asyncio.create_subprocess_exec(
    #             "python",
    #             r"C:\Users\Young1\Desktop\Python\BOTS\meu_script.py",
    #             stdout=asyncio.subprocess.PIPE,
    #             stderr=asyncio.subprocess.PIPE
    #         )

    #         # Aguarda o processo terminar sem bloquear a execução
    #         stdout, stderr = await process.communicate()

    #         # Exibe a saída do subprocess
    #         print(f"[STDOUT]\n{stdout.decode()}")
    #         if stderr:
    #             print(f"[STDERR]\n{stderr.decode()}")

    #         print(f"BOT {id} FINALIZADO")
    #     except Exception as e:
    #         print(f"Erro: {e}")
    
    
    # Função principal para rodar a tarefa assíncrona periodicamente.
    async def start(self):
        """Função principal para rodar a tarefa assíncrona periodicamente.""" 
        try:
            # Configura o schedule para rodar run_queue_scripts a cada segundo
            schedule.every(1).seconds.do(self.check_trigger_time)
            schedule.every(1).seconds.do(lambda: asyncio.create_task(self.run_queue_scripts()))  # Agenda a execução da função
            schedule.every(2).seconds.do(lambda: asyncio.create_task(clean_list_of_sended_items(self.list_of_sended_items))) # chama clean_list_of_sended_items de forma assíncrona
            while True:
                schedule.run_pending()  # Executa tarefas pendentes do schedule
                await asyncio.sleep(1)  # Espera 1 segundo antes de checar novamente
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # Função para rodar o monitoramento
    def run_monitoring():
        monitor = Monitoring()  # Cria uma instância de Monitoring
        asyncio.run(monitor.start())  # Inicia o monitoramento usando asyncio.run()

    # Executa o monitoramento
    run_monitoring()  # Chama a função que irá rodar o monitoramento