import threading
import time

def invia_email_convocazione_async(email_steward, titolo_evento, nome_settore):
    """
    Simula l'invio asincrono di un'email di conferma convocazione.
    """
    def send_email():
        # Simuliamo un ritardo di rete di 3 secondi
        time.sleep(3)
        print(f"\n[ASYNC TASK] 📧 Email inviata a {email_steward}: Sei stato confermato per '{titolo_evento}' nel settore {nome_settore}!\n")

    # Avvia il processo in un thread separato
    thread = threading.Thread(target=send_email)
    thread.start()