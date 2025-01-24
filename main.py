import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

CONST_SENHA_WIFI_CARACTERES = 8
CONST_SENHAS_TENTADAS = set()  # Usando um conjunto para evitar duplicatas e melhorar a busca
LOCK = threading.Lock()  # Lock para evitar condições de corrida
senha_encontrada = threading.Event()  # Evento para sinalizar quando a senha for encontrada

def gerar_senha_wifi():
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVXWZY1234567890abcdefghijklmnopqrstuvxwzy!@#$%¨&*()_+") 
                   for _ in range(CONST_SENHA_WIFI_CARACTERES))

def password_cracker(senha, thread_id, tentativas_por_thread):
    global CONST_SENHAS_TENTADAS

    while not senha_encontrada.is_set():
        tentativa = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVXWZY1234567890abcdefghijklmnopqrstuvxwzy!@#$%¨&*()_+") 
                            for _ in range(CONST_SENHA_WIFI_CARACTERES))
        
        # Lock para acesso seguro ao conjunto de senhas tentadas
        with LOCK:
            if tentativa in CONST_SENHAS_TENTADAS:
                continue  # Já tentada, ignorar
            CONST_SENHAS_TENTADAS.add(tentativa)

        # Incrementar contador de tentativas
        tentativas_por_thread[thread_id] += 1

        # Checar se a tentativa é a senha correta
        if tentativa == senha:
            senha_encontrada.set()  # Sinaliza que a senha foi encontrada
            print(f"[Thread-{thread_id}] Senha encontrada: {tentativa}")
            break

def main():
    senha = gerar_senha_wifi()  # Gera a senha alvo
    print(f"Senha original: {senha}")

    num_threads = 4  # Número de threads que queremos usar
    tentativas_por_thread = [0] * num_threads  # Contador de tentativas por thread

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(password_cracker, senha, i, tentativas_por_thread) for i in range(num_threads)]

        # Exibir progresso
        while not senha_encontrada.is_set():
            with LOCK:
                print("\nProgresso das threads:")
                for thread_id, tentativas in enumerate(tentativas_por_thread):
                    print(f"[Thread-{thread_id}] Tentativas: {tentativas}")
            time.sleep(1)  # Espera 1 segundo antes de verificar novamente

    print("\nFinalizado! Estatísticas de tentativas:")
    for thread_id, tentativas in enumerate(tentativas_por_thread):
        print(f"[Thread-{thread_id}] Tentativas: {tentativas}")

if __name__ == "__main__":
    main()
