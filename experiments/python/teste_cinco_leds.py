
import time
import serial

with serial.Serial("/dev/ttyUSB1", 9600, timeout=1) as arduino:
    time.sleep(2)

    print("=== HandSync: teste dos 5 LEDs ===")

    while True:
        comando = input("Quantidade de LEDs (0-5) ou q: ").strip()

        if comando.lower() == "q":
            arduino.write(b"0")
            break

        if comando not in ("0", "1", "2", "3", "4", "5"):
            print("Comando inválido.")
            continue

        arduino.write(comando.encode("ascii"))
        print(f"Comando enviado: {comando}")
