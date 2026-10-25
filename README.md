[DIGITUM]
Sistema de reconhecimento de gestos com visão computacional e Arduino.

O Digitum é meu primeiro projeto e protótipo experimental que utiliza a webcam para identificar a quantidade de dedos levantados e controlar cinco LEDs conectados a um Arduino em tempo real. Desenvolvi como uma experiência prática de integração entre software, hardware e visão computacional, com o objetivo de explorar e entender como as máquinas entendem gestos humanos e convertem isso em comandos eletrônicos.

[Tecnologias usadas]
Python 3.12: Para processamento e integração do sistema.
OpenCV: Para captura e processamento dos frames da webcam.
MediaPipe e CVZone: Para detecção de mãos e identificação dos dedos.
PySerial: Para comunicação serial entre Python e Arduino.
Arduino Uno: Para controle dos LEDs a partir dos comandos recebidos.

[Como funciona]
1. A webcam captura a imagem da mão.
2. O algoritmo identifica os pontos de referência da mão.
3. O Python calcula a quantidade de dedos levantados.
4. O resultado é transmitido ao Arduino pela comunicação serial.
5. O Arduino acende a quantidade correspondente de LEDs.

[Instruções para testar]
Conexões (Protoboard x Arduino): 
LED 1 > D2
LED 2 > D3
LED 3 > D4
LED 4 > D5
LED 5 > D6
Terra comum > GND
(Cada LED usa um resistor de 220 Ω em série.)

Instalação (Requisitos: Python 3.12, Arduino compatível e webcam):

1. Clone o repositório e acesse a pasta:
git clone URL_DO_REPOSITORIO
cd handsync

2. Crie e ative um ambiente virtual:
python3 -m venv .venv
source .venv/bin/activate

3. Instale as dependências:
python -m pip install -r requirements.txt

4. Carregue no Arduino o sketch localizado em:
arduino/controle_cinco_leds/controle_cinco_leds.ino

5. Configure no programa Python a porta serial correspondente ao Arduino e execute:
python handsync_cvzone.py

Pressione Q para encerrar.
(obs para Linux, dependendo das permissões do dispositivo, pode ser necessário adicionar o usuário ao grupo dialout e iniciar uma nova sessão.)

[Testes]
Testes manuais do reconhecimento dos dedos de 0 a 5, comunicação serial, resposta dos LEDs, estabilidade e funcionamento com ambas as mãos (documentado em docs/).

[Limitações conhecidas]
O reconhecimento pode apresentar imprecisões dependendo da orientação da mão, da posição do polegar e das condições de captura da webcam. O algoritmo utiliza regras geométricas para melhorar a classificação do polegar, mas não garante reconhecimento perfeito em todas as situações.

[Estrutura do projeto]
handsync_cvzone.py: aplicação principal.
arduino/: sketch utilizado no protótipo.
experiments/: experimentos e versões anteriores.
docs/: documentação técnica, testes e resultados.
requirements.txt: dependências Python.

[Estado do projeto]
Versão 1.0 — Protótipo funcional.
