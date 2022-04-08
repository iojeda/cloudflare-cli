import CloudFlare
import argparse

# Inint Cloudflare API wrapper object for API connection
cf = CloudFlare.CloudFlare(raw=True)

def getZone():
    for zone in getZones():
        if zone['name'] == args.zone:
            return zone
    return None    

def getZones(): 
    page_number = 0
    zones = []
    while True:
        page_number += 1
        raw_results = cf.zones.get(params={'per_page':50,'page':page_number})
        zones += raw_results['result']
        total_pages = raw_results['result_info']['total_pages']
        if page_number == total_pages:
            return zones

def getDNS(zoneid,type="",name="",per_page=100):
    page_number = 0
    dns_records = []
    while True:
        page_number += 1
        raw_results = cf.zones.dns_records.get(zoneid,params={'per_page':per_page,'type':type,'name':name,'page':page_number})
        dns_records += raw_results['result']
        total_pages = raw_results['result_info']['total_pages']
        if page_number == total_pages:
            return dns_records

def putDNS(zoneid,dnsid,type,name,content,ttl):
    raw_results = cf.zones.dns_records.put(zoneid,dnsid,data={'type':type,'name':name,'content':content,'ttl':ttl})
    print("Successfully changed DNS Record to: ",dnsid,type,name,content)
    pass

def printzones():
    for zone in getZones():
        zone_id = zone['id']
        zone_name = zone['name']
        print("zone_id=%s zone_name=%s" % (zone_id, zone_name))    

# Execution for List
def printlist(args):
    print("List selected")
    if args.list_zones is True:
        printzones()            
        exit(0)
    if args.zone is not None:
        zone = getZone() 
        if zone is not None:
            print(zone['name'])
        else:
            print("Invalid Zone name or does not exist")
            exit(1)
        if args.list_dns is True:
            print("List all DNS records for", args.zone)
            dns_records = getDNS(zoneid=zone['id'],type=args.record_type ,name=args.record_name)
            for dns_record in dns_records:
                r_name = dns_record['name']
                r_type = dns_record['type']
                r_value = dns_record['content']
                r_id = dns_record['id']
                print('\t', r_id, r_name, r_type, r_value)
    else:
        if args.list_dns is True:
            print("Zone not specified, requiered parameter -z ZONE")
            exit(1)
        else:
            printzones()
            exit(0)
# Execution for Update
def update(args):
    print("Update selected")
    print("Zone: ", args.zone)

# Execution for Update dns
def updatedns(args):
    print("Update DNS selected")
    print("Zone: ", args.zone)
    zone = getZone()
    dns_records = getDNS(zoneid=zone['id'],type=args.record_type ,name=args.record_name,per_page=1)
    if len(dns_records) != 0:
        dns_record = dns_records[0]
        print("Attempting record dns change for: ",dns_record['id'],dns_record['type'],dns_record['name'],dns_record['content'])
    else:
        print("No matching DNS record found")
        exit(1)
    putDNS(zoneid=zone['id'],dnsid=dns_record['id'],type=args.new_record_type,name=args.new_record_name,content=args.new_content,ttl=dns_record['ttl'])
    #putDNS(zone['id'])
    

# Argument definitions
# Create top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')
# Create parser for "l" (list) command
parser_l = subparsers.add_parser("l", help="l List mode")
listgroup1 = parser_l.add_mutually_exclusive_group()
listgroup1.add_argument("-z","--zone", help="Specify zone to scope")
listgroup1.add_argument("-lz", "--list-zones",action='store_true', help="list all zones")
#listgroup2 = parser_l.add_mutually_exclusive_group()
parser_l.add_argument("-ldns","--list-dns",action='store_true', help="List all DNS records of -z ZONE ")
parser_l.add_argument("-rt","--record-type",choices=['A','AAAA','CNAME','TXT'], help="Specify record type to filter request")
parser_l.add_argument("-rn","--record-name", help="Specify full DNS record name to filter request")
parser_l.set_defaults(func=printlist)

# Create parser for "u" (update) command
parser_u = subparsers.add_parser("u", help="u Update mode")
# Create subparser for "u" (update) command
subparser_u = parser_u.add_subparsers(help='sub-command help')
subparser_u_dns = subparser_u.add_parser("dns", help="Update dns record mode")
subparser_u_dns.add_argument("zone", help="Specify zone name to update")
subparser_u_dns.add_argument("record_type",choices=['A','AAAA','CNAME','TXT'], help="Specify record type to be updated")
subparser_u_dns.add_argument("record_name", help="Specify dns name to be updated")
subparser_u_dns.add_argument("content", help="Specify dns content to be updated")
subparser_u_dns.add_argument("new_record_type",choices=['A','AAAA','CNAME','TXT'], help="Specify the new record type or use same to keep unchanged")
subparser_u_dns.add_argument("new_record_name", help="Specify the new dns name or use same to keep unchanged")
subparser_u_dns.add_argument("new_content", help="Specify the new dns content or use same to keep unchanged")

subparser_u_dns.set_defaults(func=updatedns)
#parser.add_argument("-z","--zone", help="Specify zone to use")
# Parse Arguments from commandline

args = parser.parse_args()
args.func(args)
