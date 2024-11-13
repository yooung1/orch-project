from ORCHESTRATOR.database_connection.database_connection import DatabaseConnection
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from croniter import croniter
from datetime import datetime
from rich.panel import Panel
import snowflake.connector
import time


class UserInterface:
    def __init__(self):
        # Instanciando Console()
        self.console = Console()

    def process_name_UI(self):
        """User interface for the process name"""
        # Mostra o painel com uma instrução
        self.console.print(Panel("[bold blue]INSIRA O NOME DO PROCESSO - EXEMPLOS: RPAXXXX - RPA5001 - RPA1001 - RPA2002[/bold blue]", border_style="blue"))
        
        while True:
            process_name = Prompt.ask("[bold green]PROCESS NAME[/bold green]")
            # Verifica se o nome do processo é válido
            if len(process_name) < 7:
                self.console.print(Panel("[bold red]INSIRA UM NOME VALIDO SEGUINDO OS EXEMPLOS ACIMA![/bold red]", border_style="red"))
            else:
                return process_name.upper()  # Retorna o nome do processo em letras maiúsculas

    def process_trigger_UI(self):
        """User interface for the process trigger GENERATE YOUR EXPRESSION IN https://crontab.cronhub.io/"""
        self.console.print(Panel("[bold blue]INSIRA A EXPRESSÃO CRON - EXEMPLOS: 0 11 * * * - 30 23 * * 1,3,5[/bold blue]", border_style="blue"))
        
        while True:
            cron_expression = Prompt.ask("[bold green]CRON EXPRESSION[/bold green]")  # Pergunta ao usuário a expressão cron
            try:
                base = datetime.now()  # Obtém a data e hora atual
                cron = croniter(cron_expression, base)  # Cria um objeto croniter com a expressão fornecida
                next_run = cron.get_next(datetime)  # Obtém a próxima execução com base na expressão
                self.console.print(Panel(f"[bold green]Próxima execução: {next_run}[/bold green]", border_style="green"))
                time.sleep(2)  # Pequeno intervalo para o usuário visualizar
                return cron_expression  # Retorna a expressão cron válida
            except Exception as e:
                # Se houver um erro, exibe uma mensagem de erro no painel
                self.console.print(Panel("[bold red]Expressão cron inválida! Tente novamente.[/bold red]", border_style="red"))


class BotFolder(UserInterface, DatabaseConnection):
    """When you call the class it will initialize the database and the Console"""
    def __init__(self):
        super().__init__()
        self.conn = self.make_database_connection()  # Chamando o método da instância
        # Criar o cursor
        self.cursor = self.conn.cursor()
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        self.console.print("[bold red] ENCERRANDO CONEXÃO COM BANCO DE DADOS.... [/bold red]")
    
    def create_new_bot_folder(self):
        try:
            while True:
                self.process_name = self.process_name_UI()
                self.cursor.execute("""
                    SELECT * FROM Folders
                    WHERE Process_Name = %s;
                """, (self.process_name,))
                data = self.cursor.fetchall()
                if len(data) == 0:
                    break
                self.console.print(Panel(f"[bold red]\nNOME DE PASTA JA EXISTENTE '{self.process_name}', TENTE OUTRO NOME POR GENTILEZA\n", border_style="red"))

            cron_expression = self.process_trigger_UI()
            self.cursor.execute("""
                INSERT INTO FOLDERS (Process_Name, Trigger_expression)
                VALUES (%s, %s);
            """, (self.process_name, cron_expression))
            self.console.print(Panel(f"\n[bold green] NOVO FOLDER {self.process_name} CRIADO COM SUCESSO\n[/bold green]"))
        except snowflake.connector.errors.BadGatewayError as e:
            print("Erro 502: Bad Gateway - O servidor intermediário recebeu uma resposta inválida do servidor final.")
        except snowflake.connector.errors.BadRequest as e:
            print("Erro 400: Bad Request - A requisição foi inválida ou malformada.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            self.close_connection()





# Executando
BotFolder().create_new_bot_folder()
