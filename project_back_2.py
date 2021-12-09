from scapy.all import *
import json


# class for packets storing
class Packet:

    def __init__(self, ether_dst, ether_src, ip_version, ip_proto, ip_src, ip_dst, tcp_sport, tcp_dport, udp_sport,
                 udp_dport):
        self.ether_dst = ether_dst
        self.ether_src = ether_src
        self.ip_version = ip_version
        self.ip_proto = ip_proto
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport
        self.udp_sport = udp_sport
        self.udp_dport = udp_dport

    # creating a dictionary with object attributes
    def __str__(self):
        obj_dict = {}
        obj_dict['Ethernet'] = {'dst': self.ether_dst, 'src': self.ether_src}
        if self.ip_proto == "-":
            obj_dict['IP'] = {'version': self.ip_version, 'src': self.ip_src, 'dst': self.ip_dst}
        else:
            obj_dict['IP'] = {'version': self.ip_version, 'proto': self.ip_proto, 'src': self.ip_src,
                              'dst': self.ip_dst}
        if self.tcp_sport == "-":
            obj_dict['UDP'] = {'sport': self.udp_sport, 'dport': self.udp_sport}
        else:
            obj_dict['TCP'] = {'sport': self.tcp_sport, 'dport': self.tcp_dport}
        return json.dumps(obj_dict)


# Singleton class for capture
class Capture:
    # class attribute which stores the object
    _instance = None

    # method for packets capture. calls the method that make objects of Packet class
    def get_capture(self, c_filter, counter, timeout):
        packets = sniff(filter=c_filter, count=counter, timeout=timeout)
        self.object_creator(packets)
        # for i in packets:
        #     print(repr(i))
        # print(packets)
        return packets

    # initialize an single object and call get_capture method
    def __init__(self):
        if Capture._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Capture._instance = self

    # method for calling __init__
    @staticmethod
    def get_instance():
        if Capture._instance is None:
            Capture()
        else:
            return Capture._instance

# method for creating Packet class objects. stores them in a list.
    def object_creator(self, packets):
        global list_of_objects
        list_of_objects = []
        for i in packets:
            if i.haslayer(TCP) or i.haslayer(UDP):
                ether_dst = i.getlayer(0).dst
                ether_src = i.getlayer(0).src
                ip_version = i.getlayer(1).version
                try:
                    ip_proto = i.getlayer(1).proto
                except AttributeError:
                    ip_proto = "-"
                try:
                    ip_src = i.getlayer(1).src
                except AttributeError:
                    ip_src = "-"
                try:
                    ip_dst = i.getlayer(1).dst
                except AttributeError:
                    ip_dst = "-"
                if i.getlayer(TCP):
                    tcp_sport = i.getlayer(2).sport
                    tcp_dport = i.getlayer(2).dport
                    udp_sport = "-"
                    udp_dport = "-"
                else:
                    tcp_sport = "-"
                    tcp_dport = "-"
                    udp_sport = i.getlayer(2).sport
                    udp_dport = i.getlayer(2).dport

                obj = Packet(ether_dst, ether_src, ip_version, ip_proto, ip_src, ip_dst, tcp_sport, tcp_dport,
                             udp_sport, udp_dport)
                list_of_objects.append(obj)

    # method that stores Packet objects attributes in a string and prints them to a json file
    @staticmethod
    def json_file(arg):
        final_json = ""
        for obj in list_of_objects:
            final_json += obj.__str__()
        path = arg+'.json'
        try:
            with open(path, 'w') as f:
                json.dump(final_json, f)
                return True
        except FileNotFoundError:
            return False

    # method for creating pie chart
    @staticmethod
    def plot():
        tcp_no = 0
        udp_no = 0
        for obj in list_of_objects:
            if obj.tcp_sport == "-":
                udp_no += 1
            else:
                tcp_no += 1

        # print([tcp_no,udp_no])
        plt.pie([tcp_no, udp_no], labels=["TCP", "UDP"], colors=['r', 'c'], autopct="%.1f%%")
        plt.show()
