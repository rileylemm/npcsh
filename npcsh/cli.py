import argparse
from .serve import start_flask_server
from .helpers import initialize_npc_project


def main():
    parser = argparse.ArgumentParser(description="NPC utilities")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the Flask server")
    serve_parser.add_argument("--port", "-p", help="Optional port")
    serve_parser.add_argument(
        "--cors", "-c", help="CORS origins (comma-separated list)", type=str
    )
    serve_parser.add_argument(
        "--templates", "-t", help="agent templates(comma-separated list)", type=str
    )
    serve_parser.add_argument(
        "--context",
        "-ctx",
        help="important information when merging templates",
        type=str,
    )

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new NPC project")
    init_parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to initialize project in"
    )
    init_parser.add_argument(
        "--templates", "-t", help="agent templates(comma-separated list)", type=str
    )
    init_parser.add_argument(
        "--context",
        "-ctx",
        help="important information when merging templates",
        type=str,
    )

    build_parser = subparsers.add_parser(
        "build", help="Build a NPC team into a standalone executable server"
    )
    build_parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to build project in"
    )

    select_parser = subparsers.add_parser("select", help="Select a SQL model to run")
    select_parser.add_argument("model", help="Model to run")

    assembly_parser = subparsers.add_parser("assemble", help="Run an NPC assembly line")
    assembly_parser.add_argument("line", help="Assembly line to run")

    args = parser.parse_args()

    new_parser = subparsers.add_parser(
        "new", help="Create a new [NPC, tool, assembly_line, ]"
    )
    new_parser.add_argument(
        "type",
        help="Type of object to create",
        choices=["npc", "tool", "assembly_line"],
    )
    # depending on what it is we will have different possible arguments and a different flow
    # the args will be optional for the cli call bbut they will trigger an input sequence where
    # the user specifies the relevant args

    ### ALLOW ALL MACRO COMMANDS TO BE RUN AS CLI COMMANDS
    # E.G. npc vixynt 'prompt' -m 'dall-e-3' -p 'openai'
    # npc ots
    # npc spool

    if args.command == "serve":
        if args.cors:
            # Parse the CORS origins from the comma-separated string
            cors_origins = [origin.strip() for origin in args.cors.split(",")]
        else:
            cors_origins = None
        if args.templates:
            templates = [template.strip() for origin in args.templates.split(",")]
        else:
            templates = None
        if args.context:
            context = args.context.strip()
        else:
            context = None
        start_flask_server(
            port=args.port if args.port else 5337,
            cors_origins=cors_origins,
            templates=templates,
            context=context,
        )
    elif args.command == "init":
        if args.templates:
            templates = [template.strip() for origin in args.templates.split(",")]
        else:
            templates = None
        if args.context:
            context = args.context.strip()
        else:
            context = None

        initialize_npc_project(args.directory, templates=templates, context=context)
    elif args.command == "new":
        # create a new npc, tool, or assembly line
        pass
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
