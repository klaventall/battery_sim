import sys
import argparse

from app import create_app
from death import DeathStats

def run_server():
    app = create_app()
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)

def compute_death_stats():
    data_dir = "../DeathRecords/"
    death_stats = DeathStats(data_dir)
    
    return death_stats.run()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count',
                        help="Increase verbosity of output")
    subparsers = parser.add_subparsers(help='test subcommands')
    
    parser_web_app = subparsers.add_parser('web-app', help="displays results in local browser")
    parser_web_app.set_defaults(cmd='web-app')
 

    parser_death_stats = subparsers.add_parser('death-stats', help="computes stats in death data")
    parser_death_stats.set_defaults(cmd='death-stats')


    args = parser.parse_args(argv[1:])

    if args.cmd == "web-app":
        return run_server()
    elif args.cmd =="death-stats":
        return compute_death_stats()
    else:
        raise NotImplementedError("Unknown command: {!r}".format(args.cmd))

       

if __name__ == "__main__":
    sys.exit(main())