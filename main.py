import socket

def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(1)
            result = connection.connect_ex((host, port))
            return result == 0
    except OSError: # OSError is raised for system-related errors
        return False

def main():
    while True:
        try:
            print("\nEnter the host (or 'exit' to quit):")
            host = input("Host [localhost]: ").strip()

            if host.lower() == "exit":
                print("Exiting the program.")
                break

            if not host:
                host = "127.0.0.1"

            port_range = input(
                "Enter the port range (e.g., 20-100): "
            ).strip()

            if port_range.lower() == "exit":
                print("Exiting the program.")
                break

            start_port, end_port = map(
                int, port_range.split("-")
            )

            if not 1 <= start_port <= end_port <= 65535:
                raise ValueError

            print(f"\nScanning {host}, ports {start_port}-{end_port}...")
            open_ports = []

            for port in range(start_port, end_port + 1):
                if check_port(host, port):
                    open_ports.append(port)
                    print(f"Port {port} is open on {host}.")

            if not open_ports:
                print("No open ports found in the specified range.")
            else:
                print(
                    f"Open ports on {host}: "
                    f"{', '.join(map(str, open_ports))}"
                )

        except KeyboardInterrupt:
            print("\nExiting the program.")
            break

        except (ValueError, OverflowError):
            print(
                "Invalid port range. "
                "Enter two integers, e.g., 20-100, "
                "with ports between 1 and 65535."
            )

        except OSError as e:
            print(f"Network error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
