
import cv2
import math
import time
import serial
from collections import deque
from cvzone.HandTrackingModule import HandDetector

# CONFIGURACOES
PORTA = "/dev/ttyUSB0"
BAUDRATE = 9600

detector = HandDetector(
    staticMode=False,
    maxHands=1,
    detectionCon=0.7,
    minTrackCon=0.5,
)

def distancia(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def contar_dedos(mao):
    dedos = detector.fingersUp(mao)
    pontos = mao["lmList"]

    # Angulo do polegar
    a = distancia(pontos[3], pontos[4])
    b = distancia(pontos[2], pontos[3])
    c = distancia(pontos[2], pontos[4])

    if a > 0 and b > 0:
        cos_angulo = (a*a + b*b - c*c) / (2*a*b)
        cos_angulo = max(-1, min(1, cos_angulo))
        angulo = math.degrees(math.acos(cos_angulo))
    else:
        angulo = 0

    # Distancia proporcional do polegar
    largura_palma = distancia(pontos[5], pontos[17])
    dist_polegar = distancia(pontos[4], pontos[17])
    proporcao = dist_polegar / max(largura_palma, 1)

    dedos[0] = int(angulo > 150 and proporcao > 1.15)

    return dedos.count(1)

def main():
    print("HandSync - CVZone + Arduino")

    arduino = serial.Serial(PORTA, BAUDRATE, timeout=1)
    camera = None

    try:
        # Arduino Uno normalmente reinicia ao abrir a porta
        time.sleep(2)

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise RuntimeError("Nao foi possivel abrir a webcam.")

        historico = deque(maxlen=5)
        ultimo_enviado = None

        while True:
            sucesso, frame = camera.read()
            if not sucesso:
                break

            frame = cv2.flip(frame, 1)

            maos, frame = detector.findHands(
                frame,
                draw=True,
                flipType=True,
            )

            if maos:
                quantidade = contar_dedos(maos[0])
            else:
                quantidade = 0

            # Estabilizacao: exige 5 leituras iguais
            historico.append(quantidade)

            if (
                len(historico) == 5
                and len(set(historico)) == 1
                and quantidade != ultimo_enviado
            ):
                arduino.write(str(quantidade).encode("ascii"))
                arduino.flush()
                ultimo_enviado = quantidade
                print(f"Enviado ao Arduino: {quantidade}")

            texto = f"DEDOS: {quantidade}"
            cv2.putText(
                frame,
                texto,
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3,
            )

            cv2.imshow("HandSync - Arduino", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # Desliga os LEDs antes de encerrar
        if arduino.is_open:
            arduino.write(b"0")
            arduino.flush()

        if camera is not None:
            camera.release()

        cv2.destroyAllWindows()
        arduino.close()
        print("HandSync encerrado.")

if __name__ == "__main__":
    main()
