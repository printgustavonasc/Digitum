import math
import cv2
from cvzone.HandTrackingModule import HandDetector

# Inicializa o detector de maos
detector = HandDetector(
    staticMode=False,
    maxHands=1,
    detectionCon=0.7,
    minTrackCon=0.5,
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Nao foi possivel abrir a webcam.")

print("HandSync - Teste CVZone")
print("Pressione Q para sair.")

try:
    while True:
        sucesso, frame = camera.read()

        if not sucesso:
            print("Erro ao capturar imagem.")
            break

        # Espelha a imagem
        frame = cv2.flip(frame, 1)

        # Detecta a mao
        maos, frame = detector.findHands(
            frame,
            draw=True,
            flipType=True,
        )

        if maos:
            mao = maos[0]
            

            # Retorna uma lista com 5 valores:
            # 1 = dedo levantado
            # 0 = dedo abaixado
            dedos = detector.fingersUp(mao)
            pontos = mao["lmList"]

            # Articulacoes do polegar:
            # 2 = MCP (base)
            # 3 = IP (articulacao intermediaria)
            # 4 = ponta

            def distancia(a, b):
                return math.hypot(
                    a[0] - b[0],
                    a[1] - b[1],
                )

            a = distancia(pontos[3], pontos[4])
            b = distancia(pontos[2], pontos[3])
            c = distancia(pontos[2], pontos[4])

            # Lei dos cossenos para calcular o angulo na articulacao 3
            cos_angulo = (a*a + b*b - c*c) / (2*a*b)
            cos_angulo = max(-1, min(1, cos_angulo))

            angulo = math.degrees(math.acos(cos_angulo))

            # Polegar considerado estendido quando a articulacao
            # esta relativamente alinhada
            # Distancia da ponta do polegar ate a base do dedo minimo
            dist_polegar = distancia(pontos[4], pontos[17])

            # Largura da palma, usada como referencia
            largura_palma = distancia(pontos[5], pontos[17])

            # Distancia proporcional ao tamanho da mao
            proporcao = dist_polegar / max(largura_palma, 1)

            # Duas condicoes para considerar o polegar aberto
            polegar_reto = angulo > 150
            polegar_afastado = proporcao > 1.15

            dedos[0] = int(polegar_reto and polegar_afastado)

            quantidade = dedos.count(1)

            texto = f"DEDOS: {quantidade}"

            print(
                f"\rAngulo: {angulo:.1f} | "
                f"Proporcao: {proporcao:.2f} | "
                f"Dedos: {dedos} | Total: {quantidade}    ",
               f"\rMao: {mao['type']} | "
                f"Dedos: {dedos} | "
                f"Total: {quantidade}     ",
                end="",
                flush=True,
            )
        else:
            texto = "NENHUMA MAO"

        cv2.putText(
            frame,
            texto,
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3,
        )

        cv2.imshow("HandSync - CVZone", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
    print("\nTeste encerrado.")
