import subprocess

def get_available_networks():
    """Отримує список доступних Wi-Fi мереж."""
    result = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True)
    networks = []
    for line in result.stdout.split("\n"):
        line = line.strip()
        if line.lower().startswith("ssid "):
            networks.append(line.split(": ")[-1])
    return networks