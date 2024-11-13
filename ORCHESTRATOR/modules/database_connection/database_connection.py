from rich.console import Console
from rich.panel import Panel
import snowflake.connector


class DatabaseConnection:
    def __init__(self, console=None):
        # Se o console for fornecido, usa-o; caso contrário, cria um novo
        self.console = Console()

    def make_database_connection(self):
        try:
            # Conexão com o banco de dados
            conn = snowflake.connector.connect(
                user=
                password=
                account=
                database='ORCHESTRATOR',
                schema='STRUCTURE',
                quote_identifiers=True
            )
            return conn
        except snowflake.connector.errors.Error as e:
            self.console.print(f"[bold red]Erro ao conectar ao banco de dados: {e}[/bold red]")
            raise
        except snowflake.connector.errors.DatabaseError as e:
            self.console.print(Panel(f"[bold red]Erro ao conectar ao banco de dados: {e}[/bold red]", border_style="red"))
        except Exception as e:
            self.console.print(Panel(f"[bold red]Erro inesperado: {e}[/bold red]", border_style="red"))
