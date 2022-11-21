from moderngov import api
import argparse
import logging

logger = logging.getLogger()


def run():
    parser = argparse.ArgumentParser(
        prog='moderngov',
        description='Query public data from your council website',
        epilog='Query a local council website to ask for data from the moderngov API')

    parser.add_argument('website')
    parser.add_argument('-w', '--ward-list', dest='ward_list', action='store_true')
    parser.add_argument('-m', '--member-list', dest='member_list', action='store_true')
    parser.add_argument('-M', '--member-detail', dest='member_id', type=int, action='store')
    parser.add_argument('-b', '--committee_list', dest='committee_list', action='store_true')
    parser.add_argument('-B', '--committee-detail', dest='committee_id', type=int, action='store')
    args = parser.parse_args()
    instance = api.ModerngovApi(args.website)

    if args.ward_list:
        print(*instance.wards.list(), sep="\n")

    elif args.member_list:
        lst = map(lambda x: x['memberid'] + " " + x['fullusername'], instance.members.list())
        print(*lst, sep="\n")

    elif args.committee_list:
        lst = map(lambda x: x['committeeid'] + " " + x['committeetitle'], instance.committees.list())
        print(*lst, sep="\n")

    elif args.committee_id:
        data = instance.committees.by_id(args.committee_id)
        print_dict(data)

    elif args.member_id:
        data = instance.members.by_id(args.member_id)
        print_dict(data)

    else:
        logger.error("You didn't request any data, try -h!")


def print_dict(record: dict, key_name: str = "", indent: int = 0):
    indent_string = " " * indent

    if not record:
        print("No result found")

    if key_name:
        print(key_name)

    for key, value in record.items():
        if type(value) is dict:
            print_dict(value, key_name=key, indent=indent + 2)
            continue
        elif type(value) is list:
            for item in value:
                print_dict(item, indent=indent + 2)
        elif type(value) is str:
            print(indent_string + "{:20} {:6}".format(key, value or "none"))


if __name__ == '__main__':
    run()
