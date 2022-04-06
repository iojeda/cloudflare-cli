import argparse

# Execution for List
def printlist(args):
    print("List selected")
    if args.list_zones is not None:
        print("List zones available")
    if args.zone is not None:
        print("Zone: ", args.zone)
        if args.list_dns is not None:
            print("List all DNS records for", args.zone)


# Execution for Update
def update(args):
    print("Update selected")
    print("Zone: ", args.zone)

# Argument definitions
# Create top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')
# Create parser for "l" (list) command
parser_l = subparsers.add_parser("l", help="l help")
listgroup = parser_l.add_mutually_exclusive_group()
listgroup.add_argument("-z","--zone", help="Specify zone to scope")
listgroup.add_argument("-lz", "--list-zones",action='store_true', help="list all zones")
parser_l.add_argument("-ldns","--list-dns",action='store_true', help="List all DNS records of -z ZONE ")
parser_l.add_argument("-rt","--record-type",choices=['A','AAAA','CNAME','TXT'], help="Specify record type to filter request")
parser_l.add_argument("-sdns","--search-dns", help="Specify full or partial DNS record name to search")
parser_l.set_defaults(func=printlist)

# Create parser for "u" (update) command
parser_u = subparsers.add_parser("u", help="u help")
parser_u.add_argument("zone", help="u help")
parser_u.set_defaults(func=update)
parser.add_argument("-z","--zone", help="Specify zone to use")
# Parse Arguments from commandline

args = parser.parse_args()
args.func(args)
