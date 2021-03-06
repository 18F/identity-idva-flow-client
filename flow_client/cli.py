import argparse
import datetime

from flow_client import oidc, settings


def parse_args():

    description = """Generate a url with signed request object for a flow endpoint.

    flow can be selected by name from list in config or specified by url. if not specified, defaults to first flow in config.
    time is specified in days and seconds. defaults to time set in config which is usually 1 day"""

    parser = argparse.ArgumentParser(
        description=description,
        prog="sign_url.sh",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="flow name. used to select flow from list of flows in config",
    )
    parser.add_argument("-u", "--url", help="flow url"),
    parser.add_argument(
        "-l", "--list", action="store_true", help="list stored flow names and exit"
    )
    parser.add_argument(
        "-d", "--days", type=float, help="num days sig is valid. summed with seconds"
    )
    parser.add_argument(
        "-s", "--seconds", type=float, help="num seconds sig is valid. summed with days"
    )

    return parser.parse_args()


def main():

    args = parse_args()

    # list flows and exit
    if args.list:
        print(f"list of flows:")
        for name in settings.FLOWS.keys():
            print(f"\t{name}")
        return

    # select duration
    if args.seconds is None and args.days is None:
        valid_for = settings.VALID_FOR
        print(f"using default duration:  ", end="")
    else:
        valid_for = datetime.timedelta(
            days=0 if args.days is None else args.days,
            seconds=0 if args.seconds is None else args.seconds,
        )
        print(f"using supplied duration:  ", end="")
    print(f"{valid_for.days} days and {valid_for.seconds} seconds")

    # select flow
    if args.name is not None:
        if args.name not in settings.FLOWS:
            print(f"no such flow:  {args.name}")
            return
        url = settings.FLOWS[args.name]
        print(f"using supplied flow:  {args.name}")
    elif args.url is not None:
        url = args.url
        print(f"using supplied flow url")
    else:
        name = next(iter(settings.FLOWS.keys()))
        print(f"using default flow:  {name}")
        url = settings.FLOWS[name]

    request = oidc.gen_sig_url(url, valid_for)
    print(request.url)


if __name__ == "__main__":
    main()
