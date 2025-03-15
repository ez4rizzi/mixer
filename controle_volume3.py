import serial
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import numpy as np

# Configurar comunicação com o Arduino
porta_serial = serial.Serial("COM4", 9600, timeout=1)
time.sleep(2)  # Aguarda a inicialização da comunicação serial

# Configurar controle de volume mestre
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_master = interface.QueryInterface(IAudioEndpointVolume)

# Função para mapear valores do potenciômetro (0-1023) para volume (0.0 - 1.0)
def mapear_volume(valor):
    return np.interp(valor, [0, 1023], [0.0, 1.0])

# Função para buscar sessões de áudio de aplicativos específicos
def get_app_session(app_name):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and app_name.lower() in session.Process.name().lower():
            return session.SimpleAudioVolume
    return None  # Retorna None se o aplicativo não estiver em execução

try:
    while True:
        try:
            # Lê uma linha da porta serial
            dado_bruto = porta_serial.readline().decode('utf-8', errors='ignore').strip()

            # Verifica se os dados começam com < e terminam com >
            if dado_bruto.startswith("<") and dado_bruto.endswith(">"):
                # Remove os delimitadores < e >
                dado_bruto = dado_bruto[1:-1]

                # Divide os valores separados por vírgula
                valores = dado_bruto.split(",")

                # Converte os valores para inteiros
                try:
                    valores_int = [int(v) for v in valores if v.isdigit()]
                    
                    if len(valores_int) == 4:
                        # Controle do volume mestre
                        volume_mestre = mapear_volume(valores_int[0])
                        volume_master.SetMasterVolumeLevelScalar(volume_mestre, None)
                        print(f"🔊 Volume Mestre: {int(volume_mestre * 100)}%")

                        # Controle do Spotify
                        spotify = get_app_session("Spotify.exe")
                        if spotify:
                            volume_spotify = mapear_volume(valores_int[1])
                            spotify.SetMasterVolume(volume_spotify, None)
                            print(f"🎵 Spotify: {int(volume_spotify * 100)}%")

                        # Controle do Google Chrome
                        chrome = get_app_session("chrome.exe")
                        if chrome:
                            volume_chrome = mapear_volume(valores_int[2])
                            chrome.SetMasterVolume(volume_chrome, None)
                            print(f"🌍 Chrome: {int(volume_chrome * 100)}%")

                        # Controle do Discord
                        discord = get_app_session("Discord.exe")
                        if discord:
                            volume_discord = mapear_volume(valores_int[3])
                            discord.SetMasterVolume(volume_discord, None)
                            print(f"🎙️ Discord: {int(volume_discord * 100)}%")

                    else:
                        print(f"Dado incompleto recebido: {valores}")

                except ValueError:
                    print(f"Erro ao converter para inteiro: {valores}")

            else:
                print(f"Dado inválido recebido: {dado_bruto}")

        except serial.SerialException as e:
            print(f"Erro na comunicação serial: {e}")
            break

except KeyboardInterrupt:
    print("\nEncerrando a leitura serial...")

finally:
    porta_serial.close()
    print("Porta serial fechada.")
