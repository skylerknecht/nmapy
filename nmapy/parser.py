import os
import re

from collections import namedtuple

Service = namedtuple('Service', ['number', 'status', 'transport_protocol', 'application_protocol'])
Host = namedtuple('Host', ['addr', 'hostname', 'status', 'services'])

HOST_WITH_SERVICES = re.compile(r'Host:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\(([^)]+)\)\sPorts:\s(.*)')
HOST_WITHOUT_SERVICES = re.compile(r'Host:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\(([^)]+)\)\sStatus:\s(\w+)')

class Parser:

    def __init__(self, nmap_file, delimiter='\n'):
        self.hosts = []
        self.delimiter = delimiter
        self.web_protocols = {
            'http': 'http',
            'http-proxy': 'http',
            'https': 'https',
            'ssl/http': 'https',
            'ssl/https': 'https',
            'ssl/https?': 'https',
            'ssl/http-proxy': 'https'
        }
        self.network_protocols = {
            'smb': 'smb',
            'ms-sql-s': 'mssql',
            'postgresql': 'postgresql'
        }
        self.display_functions = {
            'hosts': self.display_hosts,
            'webhosts': self.display_webhosts,
            'webports': self.display_webports,
            'smbhosts': self.display_smbhosts,
            'sqlhosts': self.display_sqlhosts,
            'sqlports': self.display_sqlports,
            'livehosts': self.display_livehosts,
            'liveports': self.display_liveports
        }
        self.nmap_file = nmap_file
        self.parse_hosts()

    def parse_hosts(self):
        if not os.path.exists(self.nmap_file):
            print(f'{self.nmap_file} does not exist.')
            return None
        with open(self.nmap_file, 'r') as fd:
            for line in fd:
                line = line.strip()
                match_services = HOST_WITH_SERVICES.match(line)
                match_status = HOST_WITHOUT_SERVICES.match(line)
                if match_services:
                    addr, hostname, services_str = match_services.groups()
                    services = self.parse_services(services_str.split(', '))
                    self.hosts.append(Host(addr, hostname, 'Up', services))
                elif match_status:
                    addr, hostname, status = match_status.groups()
                    self.hosts.append(Host(addr, hostname, status, []))

    def parse_services(self, services):
        _services = []
        for service in services:
            _service_values = service.split('/')
            if len(_service_values) >= 5:
                number = _service_values[0]
                status = _service_values[1]
                transport_protocol = _service_values[2]
                application_protocol = _service_values[4]
                _services.append(Service(number, status, transport_protocol, application_protocol))
        return _services

    def output(self, items):
        stripped_items = [item.strip() for item in items]
        print(self.delimiter.join(stripped_items))

    def display_hosts(self):
        output_lines = []
        for host in self.hosts:
            output_line = f'{host.addr} ({host.hostname}) {host.status}'
            if host.services:
                services = [f'{service.application_protocol} {service.number} {service.transport_protocol} {service.status}' for service in host.services]
                output_line += ' ' + ', '.join(services)
            output_lines.append(output_line)
        self.output(output_lines)

    def display_webhosts(self):
        output_lines = []
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol in self.web_protocols:
                    web_protocol = self.web_protocols[service.application_protocol]
                    output_lines.append(f'{web_protocol}://{host.addr}:{service.number}')
        self.output(output_lines)

    def display_webports(self):
        output_lines = []
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol in self.web_protocols:
                    output_lines.append(f'{service.number}')
        self.output(output_lines)

    def display_smbhosts(self):
        output_lines = []
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol == 'smb':
                    output_lines.append(f'smb://{host.addr}:{service.number}')
        self.output(output_lines)

    def display_sqlhosts(self):
        output_lines = []
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol == 'ms-sql-s':
                    output_lines.append(f'mssql://{host.addr}:{service.number}')
                elif service.application_protocol == 'postgresql':
                    output_lines.append(f'postgresql://{host.addr}:{service.number}')
        self.output(output_lines)

    def display_sqlports(self):
        output_lines = []
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol in ['ms-sql-s', 'postgresql']:
                    output_lines.append(f'{service.number}')
        self.output(output_lines)

    def display_livehosts(self):
        unique_hosts = set()
        for host in self.hosts:
            if host.status == 'Up':
                unique_hosts.add(host.addr)
        self.output(sorted(unique_hosts))

    def display_liveports(self):
        unique_ports = set()
        for host in self.hosts:
            if host.status == 'Up' and host.services:
                for service in host.services:
                    unique_ports.add(service.number)
        self.output(sorted(unique_ports, reverse=True))