import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Não foi possível abrir a webcam.")

print("Webcam iniciada. Pressione Q para encerrar.")

try:
    while True:
        sucesso, frame = camera.read()

        if not sucesso:
            print("Erro ao capturar imagem da webcam.")
            break

        cv2.imshow("HandSync - Teste de Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
