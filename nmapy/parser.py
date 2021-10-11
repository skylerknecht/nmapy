import os
import re

from collections import namedtuple

Service = namedtuple('Service', ['number', 'status', 'transport_protocol', 'application_protocol'])
Host = namedtuple('Host', ['addr', 'hostname', 'status', 'services'])

HOST_WITH_SERVICES = re.compile(r'Host:\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\(.*\)\sPorts\:.*')
HOST_WITHOUT_SERVICES = re.compile(r'Host:\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\(.*\)\sStatus:\s.*')

class Parser:

    hosts = []
    web_protocols = {
        'http':'http',
        'http-proxy':'http',
        'https':'https',
        'ssl/http':'https',
        'ssl/https':'https',
        'ssl/https?':'https',
        'ssl/http-proxy':'https'
        }
    delimiter = '\n'

    def __init__(self, nmap_file):
        self.display_functions = {
            'hosts':self.display_hosts,
            'webhosts':self.display_webhosts,
            'webports':self.display_webports
        }
        self.nmap_file = nmap_file
        self.parse_hosts()

    def parse_hosts(self):
        if not os.path.exists(self.nmap_file):
            print(f'{self.nmap_file} does not exist.')
            return None
        with open(self.nmap_file, 'r') as fd:
            for line in fd:
                _line_values = line.split()
                if HOST_WITH_SERVICES.match(line):
                    addr = _line_values[1]
                    hostname = _line_values[2]
                    status = 'Up'
                    services = ''.join(_line_values[4:]).split(',')
                    services = self.parse_services(services)
                    self.hosts.append(Host(addr, hostname, status, services))
                    continue
                if HOST_WITHOUT_SERVICES.match(line):
                    addr = _line_values[1]
                    hostname = _line_values[2]
                    status = _line_values[4]
                    self.hosts.append(Host(addr, hostname, status, []))
                    continue

    def parse_services(self, services):
        _services = []
        for service in services:
            _service_values = service.split('/')
            number = _service_values[0]
            status = _service_values[1]
            transport_protocol = _service_values[2]
            application_protocol = _service_values[4]
            _services.append(Service(number, status, transport_protocol, application_protocol))
        return _services

    def display_hosts(self):
        for host in self.hosts:
            print(f'{host.addr} {host.hostname} {host.status}', end=' ')
            if not host.services:
                print(end=self.delimiter)
                continue
            for service in host.services:
                print(f'{service.application_protocol} {service.number} {service.transport_protocol} {service.status}', end=', ')
            print(end=self.delimiter)

    def display_webhosts(self):
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol in self.web_protocols:
                    web_protocol = self.web_protocols[service.application_protocol]
                    print(f'{web_protocol}://{host.addr}:{service.number}', end=self.delimiter)

    def display_webports(self):
        for host in self.hosts:
            if not host.services:
                continue
            for service in host.services:
                if service.application_protocol in self.web_protocols:
                    print(f'{service.number}', end=self.delimiter)
