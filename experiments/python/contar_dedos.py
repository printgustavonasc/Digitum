import math

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODELO = "hand_landmarker.task"

# (base, articulacao, ponta) para cada dedo
DEDOS = [
    (2, 3, 4),      # Polegar
    (5, 6, 8),      # Indicador
    (9, 10, 12),    # Medio
    (13, 14, 16),   # Anelar
    (17, 18, 20),   # Mindinho
]

CONEXOES = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17),
]


def angulo(a, b, c):
    """Calcula o angulo ABC em graus."""
    ab = (a.x - b.x, a.y - b.y)
    cb = (c.x - b.x, c.y - b.y)

    produto = ab[0] * cb[0] + ab[1] * cb[1]
    norma_ab = math.hypot(*ab)
    norma_cb = math.hypot(*cb)

    if norma_ab == 0 or norma_cb == 0:
        return 0

    cosseno = produto / (norma_ab * norma_cb)
    cosseno = max(-1, min(1, cosseno))

    return math.degrees(math.acos(cosseno))


def distancia(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def contar_dedos(pontos):
    quantidade = 0

    # Indicador, médio, anelar e mindinho
    dedos = [
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 16),
        (17, 18, 19, 20),
    ]

    for base, articulacao1, articulacao2, ponta in dedos:
        angulo1 = angulo(
            pontos[base],
            pontos[articulacao1],
            pontos[articulacao2],
        )

        angulo2 = angulo(
            pontos[articulacao1],
            pontos[articulacao2],
            pontos[ponta],
        )

        estendido = angulo1 > 155 and angulo2 > 155

        afastado = (
            distancia(pontos[ponta], pontos[base])
            > distancia(pontos[articulacao2], pontos[base]) * 1.3
        )

        if estendido and afastado:
            quantidade += 1

    # Polegar: avaliar extensão e afastamento da própria base
    angulo_polegar = angulo(
        pontos[2],
        pontos[3],
        pontos[4],
    )

    distancia_ponta = distancia(
        pontos[4],
        pontos[2],
    )

    distancia_articulacao = distancia(
        pontos[3],
        pontos[2],
    )

    polegar_estendido = (
        angulo_polegar > 150
        and distancia_ponta > distancia_articulacao * 1.5
    )

    if polegar_estendido:
        quantidade += 1

    return quantidade


opcoes = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(
        model_asset_path=MODELO
    ),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Nao foi possivel abrir a webcam.")

print("HandSync - Contagem de dedos")
print("Pressione Q para encerrar.")

try:
    with vision.HandLandmarker.create_from_options(opcoes) as detector:
        timestamp_ms = 0

        while True:
            sucesso, frame = camera.read()

            if not sucesso:
                print("Falha na captura.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            imagem = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb,
            )

            timestamp_ms += 33
            resultado = detector.detect_for_video(
                imagem,
                timestamp_ms,
            )

            quantidade = None

            if resultado.hand_landmarks:
                pontos = resultado.hand_landmarks[0]
                quantidade = contar_dedos(pontos)

                altura, largura = frame.shape[:2]

                for inicio, fim in CONEXOES:
                    a = pontos[inicio]
                    b = pontos[fim]

                    cv2.line(
                        frame,
                        (int(a.x * largura), int(a.y * altura)),
                        (int(b.x * largura), int(b.y * altura)),
                        (0, 200, 0),
                        2,
                    )

                for ponto in pontos:
                    cv2.circle(
                        frame,
                        (int(ponto.x * largura),
                         int(ponto.y * altura)),
                        4,
                        (0, 255, 0),
                        -1,
                    )

            texto = (
                f"DEDOS: {quantidade}"
                if quantidade is not None
                else "NENHUMA MAO"
            )

            cv2.putText(
                frame,
                texto,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.imshow("HandSync - Contagem", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()
