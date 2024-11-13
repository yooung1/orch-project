import asyncio

async def Bot(id):
    print("Bot")
    """Simula o processamento de um bot, rodando em segundo plano"""
    try:
        print(f"BOT {id} EXECUTADO")
        
        # Inicia o subprocess de forma assíncrona
        process = await asyncio.create_subprocess_exec(
            "python",
            r"C:\Users\Young1\Desktop\Python\bots\meu_script.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Aguarda o processo terminar sem bloquear a execução
        stdout, stderr = await process.communicate()

        # Exibe a saída do subprocess
        print(f"[STDOUT]\n{stdout.decode()}")
        if stderr:
            print(f"[STDERR]\n{stderr.decode()}")

        print(f"BOT {id} FINALIZADO")
    except Exception as e:
        print(f"Erro: {e}")