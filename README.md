# OmniBrow v1.0.2

**OmniBrow** is a powerful, multifaceted browser application tailored for cybersecurity specialists and enthusiasts. Created by Alik Paranyan, a cybersecurity specialist and cybercriminal enthusiast, OmniBrow combines advanced web browsing with robust tools for URL parsing, Google Dorking, domain information lookup, and port scanning. This unique blend of features makes OmniBrow an indispensable tool for comprehensive web analysis and security research.

## Features

### Advanced Web Browser
- **Seamless Navigation**: Navigate the web effortlessly with a built-in browser that supports all modern web standards.
- **Integrated Toolbars**: Quickly access essential functions like back, forward, reload, and home.

### URL Parsing
- **Detailed URL Analysis**: Parse and analyze URLs to extract components such as scheme, host, and path.
- **Google Search Extraction**: Automatically extract URLs from Google search results for deeper analysis.

### Google Dorking
- **Powerful Search Queries**: Utilize advanced Google search techniques (dorks) to uncover hidden information and potential vulnerabilities.
- **Custom Dork Queries**: Select from a variety of dork types and input custom parameters for tailored search results.

### Domain Information Lookup
- **DNS Lookup**: Retrieve DNS information for any domain.
- **IP Information**: Fetch detailed IP information, including geographical data.
- **WHOIS Lookup**: Access WHOIS records to gather ownership and registration details.
- **SSL Certificate Information**: Inspect SSL certificates to verify domain security.

### Port Scanning
- **Fast Port Scanning**: Scan a range of ports on a target domain or IP address using multithreading for faster results.
- **Customizable Settings**: Specify the range of ports, number of threads, and timeout for each scan.
- **Detailed Results**: View open ports and additional information for thorough security analysis.

## Installation

To install and run OmniBrow, follow these steps:

### Prerequisites

- Python 3.x

### Steps

1. **Clone the Repository**

    ```sh
    git clone https://github.com/alyaparan/omnibrow.git
    cd omnibrow
    ```

2. **Create and Activate a Virtual Environment**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Application**

    ```sh
    python main.py --no-sandbox
    ```

## Usage

1. **Launch OmniBrow**: Start the application using the installation steps provided.
2. **Navigate the Web**: Use the browser's navigation toolbar for standard browsing.
3. **Parse URLs**: Click on "Parse URL" to extract and view the components of the current URL.
4. **Perform Google Dorking**: Select a dork query type, input your parameter, and perform the search.
5. **Lookup Domain Information**: Enter a domain and use the available buttons to fetch DNS, IP, WHOIS, and SSL certificate information.
6. **Scan Ports**: Enter the target domain/IP, specify the range of ports, number of threads, and timeout, then click "Scan Ports" to view open ports.

## Contribution

Contributions to OmniBrow are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request. Together, we can enhance the capabilities of this powerful tool.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Developed by Alik Paranyan also as @alyaparan, Cyber Security Specialist and Cyber Criminal Enthusiast.
