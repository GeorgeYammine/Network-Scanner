# Network-Scanner

A simple Python-based network scanner tool with two main functions:

Discover all live IP addresses on your local network (auto-detects your subnet and scans it with multi-threaded ping requests).

Scan ports and identify common services on a specified target IP (multi-threaded TCP port scan for ports 1–1024).

Features
Automatic detection of your local subnet (assumes a /24 network).

Fast discovery of live hosts using ICMP ping.

Multi-threaded port scanner with basic service detection via standard port numbers.

Cross-platform compatible (Windows/Linux/macOS).

Simple command-line menu interface.

Requirements
Python 3.x

No external dependencies required (uses built-in modules like socket, threading, platform, and os).

Usage
Clone this repository or download the script:

bash
Copy
Edit
git clone https://github.com/yourusername/network-scanner.git
cd network-scanner
Run the scanner:

bash
Copy
Edit
python scanner.py
Follow the on-screen menu:

Press 1 to discover all live IPs on your local network.

Press 2 to scan ports and services on a specific target IP.

Press 0 to exit.

Notes
The subnet is automatically detected based on your current IP address and assumes a /24 network mask.

The ping scan uses OS-native ping commands, so results may vary based on your platform and firewall settings.

The port scanner attempts to identify common services using standard port-to-service mappings, but some services may appear as "Unknown".

Running on networks larger than /24 may require modifying the script.
