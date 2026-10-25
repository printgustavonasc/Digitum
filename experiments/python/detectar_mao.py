import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODELO = "hand_landmarker.task"

opcoes = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODELO),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Não foi possível abrir a webcam.")

print("Detecção iniciada. Pressione Q para sair.")

try:
    with vision.HandLandmarker.create_from_options(opcoes) as detector:
        timestamp_ms = 0

        while True:
            sucesso, frame = camera.read()

            if not sucesso:
                print("Falha ao capturar imagem.")
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

            if resultado.hand_landmarks:
                altura, largura = frame.shape[:2]

                for mao in resultado.hand_landmarks:
                    for ponto in mao:
                        x = int(ponto.x * largura)
                        y = int(ponto.y * altura)

                        cv2.circle(
                            frame,
                            (x, y),
                            4,
                            (0, 255, 0),
                            -1,
                        )

                cv2.putText(
                    frame,
                    "MAO DETECTADA",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )

            else:
                cv2.putText(
                    frame,
                    "NENHUMA MAO",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("HandSync - Deteccao", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()
