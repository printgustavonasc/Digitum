import time
import serial

PORTA = "/dev/ttyUSB0"
VELOCIDADE = 9600

arduino = serial.Serial(PORTA, VELOCIDADE, timeout=1)

# Aguarda o Arduino reiniciar após abrir a conexão serial
time.sleep(2)

print("HandSync - Teste de comunicação serial")
print("1 = Acender LED")
print("0 = Apagar LED")
print("q = Sair")

try:
    while True:
        comando = input("Digite um comando: ").strip()

        if comando.lower() == "q":
            break

        if comando not in ("0", "1"):
            print("Comando inválido. Digite 0 ou 1.")
            continue

        arduino.write(comando.encode("utf-8"))
        print(f"Comando {comando} enviado.")

finally:
    arduino.close()
    print("Conexão serial encerrada.")
