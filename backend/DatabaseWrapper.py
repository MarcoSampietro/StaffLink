import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:

    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'cursorclass': pymysql.cursors.DictCursor
        }

    def _get_connection(self):
        """Crea e restituisce una nuova connessione al database."""
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=None):
        """Esegue query di scrittura (INSERT, UPDATE, DELETE) e fa il commit."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            print(f"Errore DB durante execute_query: {e}")
            raise e
        finally:
            connection.close()

    def fetch_all(self, query, params=None):
        """Esegue query di lettura (SELECT) e restituisce tutti i risultati come dizionari."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Errore DB durante fetch_all: {e}")
            raise e
        finally:
            connection.close()

    def fetch_one(self, query, params=None):
        """Esegue query di lettura (SELECT) e restituisce un singolo record come dizionario."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            print(f"Errore DB durante fetch_one: {e}")
            raise e
        finally:
            connection.close()

    # --- Metodi specifici per la logica di business di StaffLink Arena ---

    def get_utenti_ordinati(self):
        """
        Recupera tutti gli utenti.
        """
        query = "SELECT * FROM utente ORDER BY cognome ASC, nome ASC"
        return self.fetch_all(query)

    def get_distinta_presenze_evento(self, id_evento):
        """
        Recupera lo staff confermato per un evento. 
        Ideale per la generazione del CSV.
        """
        query = """
            SELECT u.cognome, u.nome, s.nome_settore, t.timbratura_ingresso
            FROM turno_assegnato t
            JOIN utente u ON t.id_steward = u.id_utente
            JOIN settore s ON t.id_settore = s.id_settore
            WHERE s.id_evento = %s AND t.stato_candidatura = 'confermato'
            ORDER BY u.cognome ASC, u.nome ASC
        """
        return self.fetch_all(query, (id_evento,))

    def check_disponibilita_settore(self, id_settore):
        """
        Verifica i posti disponibili in tempo reale sottraendo i turni confermati
        dalla capacità richiesta del settore.
        """
        query = """
            SELECT 
                s.capacita_richiesta,
                (SELECT COUNT(*) FROM turno_assegnato WHERE id_settore = s.id_settore AND stato_candidatura = 'confermato') as occupati
            FROM settore s
            WHERE s.id_settore = %s
        """
        result = self.fetch_one(query, (id_settore,))
        if result:
            return result['capacita_richiesta'] - result['occupati']
        return 0