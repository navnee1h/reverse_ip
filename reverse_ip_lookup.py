# Author: Navaneeth MS
#IF ERROR! READ THE TEXT FILE

import requests
import socket
from bs4 import BeautifulSoup
from tabulate import tabulate

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Unable to resolve domain"

def fetch_reverse_ip_info(ip_address):
    url = 'https://viewdns.info/reverseip/'
    params = {
        'host': ip_address,
        't': '1'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Will raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract domain names and resolved dates
        table = soup.find('table', border='1')
        if table:
            rows = table.find_all('tr')[1:]  # Skip the first row as it contains headers
            data = []
            for row in rows:
                columns = row.find_all('td')
                domain = columns[0].text.strip()
                resolved_date = columns[1].text.strip()
                website_link = f"http://www.{domain}" if not domain.startswith('http') else domain
                data.append([website_link, resolved_date])
            return data
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    host = input("Enter the host name: ")

    # Get IP address of the host
    ip_address = get_ip_address(host)
    if ip_address == "Unable to resolve domain":
        print(ip_address)
    else:
        print(f"\nIP Address: {ip_address}\n")

        # Fetch reverse IP details
        reverse_ip_info = fetch_reverse_ip_info(ip_address)
        if reverse_ip_info:
            print("Related sites:\n")
            print(tabulate(reverse_ip_info, headers=['Related sites', 'Resolved Date'], tablefmt='grid'))
        else:
            print("No related sites found")

