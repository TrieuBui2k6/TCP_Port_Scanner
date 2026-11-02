# TCP Port Scanner

A simple command-line TCP port scanner written in Python using the built-in `socket` module. It checks a user-specified host and port range, then reports ports where a TCP connection succeeds.

**Use responsibly:** Run this tool only against `localhost`, your own devices, or systems for which you have explicit authorization.

## Features

- Accepts an IPv4 address or hostname.
- Defaults to `127.0.0.1` when the host field is left empty.
- Scans a user-specified port range, such as `20-100`, including both endpoints.
- Uses TCP sockets to test connectivity.
- Applies a 1-second socket timeout per connection attempt.
- Displays open ports and lists all open ports found in the specified range.
- Validates port ranges from `1` to `65535`.
- Allows the user to exit by entering `exit` at either input prompt.
- Handles keyboard interruption with `Ctrl+C`.
- Handles input and network errors using Python exception handling.

## Requirements

- Python 3.8 or later is recommended.
- No third-party packages are required.
- The scanner uses Python's built-in `socket` module.

## Run

### 1. Navigate to the project directory

Make sure `main.py` is available on your computer.

If you have cloned the repository, navigate to the project directory. For example:

```bash
cd TCP_PORT_SCANNER
```

Replace `TCP_PORT_SCANNER` with your actual project directory name if it is different.

### 2. Run on Kali Linux or other Linux distributions

Open a terminal in the directory containing `main.py`, then execute:

```bash
python3 main.py
```

### 3. Run on Windows

Open PowerShell in the directory containing `main.py`, then execute:

```powershell
py main.py
```

You can also use:

```powershell
python main.py
```

### 4. Enter the target and port range

The program prompts you to enter a hostname or IP address:

```text
Enter the host (or 'exit' to quit):
Host [localhost]:
```

- Enter an IPv4 address, such as `127.0.0.1`.
- Enter a hostname, such as `localhost`.
- Press `Enter` without typing anything to use the default address `127.0.0.1`.

Next, enter the port range:

```text
Enter the port range (e.g., 20-100):
```

Use the format `START-END`, where both endpoints are included.

Examples:

- `20-100`: scans ports 20 through 100.
- `80-80`: scans only port 80.
- `443-443`: scans only port 443.

Enter `exit` at either input prompt to quit the program.

Press `Ctrl+C` to interrupt the scan.

## Example

The following is an illustrative example of a scan against the local machine. The open port shown is only an example; actual results depend on which services are listening and whether connections are permitted.

```text
Enter the host (or 'exit' to quit):
Host [localhost]: 127.0.0.1
Enter the port range (e.g., 20-100): 8000-8010

Scanning 127.0.0.1, ports 8000-8010...
Port 8000 is open on 127.0.0.1.
Open ports on 127.0.0.1: 8000
```

To reproduce this result in a local test environment, open another terminal and start a simple HTTP server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Keep the server running, then execute the scanner in a separate terminal and scan ports `8000-8010`.

If no port in the specified range accepts a TCP connection, the program displays:

```text
No open ports found in the specified range.
```

## How It Works

1. **Create a TCP socket:** `socket.AF_INET` selects IPv4, while `socket.SOCK_STREAM` creates a stream socket commonly used for TCP.
2. **Set a timeout:** `settimeout(1)` limits the waiting time for each connection attempt to approximately one second.
3. **Try to connect:** `connect_ex((host, port))` attempts to establish a TCP connection. A return value of `0` indicates that the connection succeeded.
4. **Check each port:** A `for` loop iterates through the specified range, including the starting and ending ports.
5. **Collect results:** Successful connection attempts are added to the `open_ports` list.
6. **Display results:** The program prints each open port and displays the complete list of open ports after the scan.
7. **Handle errors:** The program handles invalid input, network-related `OSError` exceptions, keyboard interruptions, and other unexpected exceptions.

## Input Format

Enter the port range in `START-END` format.

| Input      | Meaning                                                     |
| ---------- | ----------------------------------------------------------- |
| `20-100`   | Checks ports 20 through 100.                                |
| `80-80`    | Checks only port 80.                                        |
| `443-443`  | Checks only port 443.                                       |
| `100-20`   | Invalid: the starting port is greater than the ending port. |
| `0-100`    | Invalid: ports must be between 1 and 65535.                 |
| `80-70000` | Invalid: the ending port exceeds 65535.                     |
| `abc-100`  | Invalid: port values must be integers.                      |

## Important Limitations

- A successful TCP connection indicates that the connection was accepted at the time of the scan. It does not identify the service or prove that the application is secure.
- A failed connection does not necessarily mean that a port is closed. A firewall, timeout, routing problem, or other network condition may prevent the connection.
- The socket timeout is fixed at one second and cannot currently be configured by the user.
- The scanner uses IPv4 sockets.
- The scan is sequential, so scanning a large port range may take considerable time.
- The program does not identify service names or versions.
- Results are displayed in the terminal and are not automatically saved to a report file.
- Hostname resolution and connection failures may produce different errors depending on the operating system and network configuration.

## Possible Improvements

- Add configurable connection timeouts.
- Improve hostname and IP address validation.
- Support single-port input, such as `80`, without requiring `80-80`.
- Add concurrent scanning with a configurable worker limit.
- Record elapsed scan time and display a progress indicator.
- Export results to JSON or TXT files.
- Add service detection and basic banner inspection.
- Expand unit tests for port-range validation and connection-result handling.
- Improve error classification and logging.
- Consider IPv6 support.

## Learning Objectives

This project provides practice with:

- Python functions, loops, conditionals, lists, and exception handling.
- TCP/IP fundamentals and port numbers.
- The Python `socket` API.
- TCP connection establishment and connection timeouts.
- Input validation and command-line interaction.
- Basic network reconnaissance in an authorized lab environment.
- Writing documentation and testing a small Python security tool.
