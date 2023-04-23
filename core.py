import netifaces
import pprint

pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(netifaces.interfaces())
interface = netifaces.interfaces()

eth = "{5B2076CD-93DD-4CCE-A823-4F80EAEC1524}"  # 以太网


# for i in interface:
#    print('\n**************Details of Interface - ' + i + ' *********************')
#    pp.pprint(netifaces.ifaddresses(i))

# 获取IP地址
def get_ip_address():
    ip_info = {
        "ipv4": netifaces.ifaddresses(eth)[netifaces.AF_INET][0]['addr'],
        "ipv6": netifaces.ifaddresses(eth)[netifaces.AF_INET6][0]['addr'],
    }
    # print(ip_info)
    return ip_info
