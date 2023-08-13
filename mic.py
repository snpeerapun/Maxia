import pyaudio

def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    print("Available microphones:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info['name']
        print(f"Microphone {i}: {device_name}")

    p.terminate()

if __name__ == "__main__":
    list_microphones()