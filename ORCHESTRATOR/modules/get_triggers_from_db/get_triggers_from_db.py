def get_triggers_from_db(conn):
        """Este metodo é inicializado assim que o processo é executado, ele pega todos os triggers atuais no banco de dados
        preenche a lista list_of_triggers_and_ids"""
        print("get_triggers")
        list_of_triggers_and_ids = []
        # conn = make_database_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID, TRIGGER_EXPRESSION FROM FOLDERS;")
            data = cursor.fetchall()
            if data:
                for i in data:
                    list_of_triggers_and_ids.append(i)  # Adiciona os triggers e IDs encontrados à lista
            return list_of_triggers_and_ids
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()