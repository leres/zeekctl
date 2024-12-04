import sys

from ZeekControl import doc, node, options, plugin


# Prints the command docstrings in a form suitable for direct inclusion
# into the documentation.
def print_commands(cls):
    cmds = []

    for i in cls.__dict__:
        docstr = cls.__dict__[i].__doc__
        if i.startswith("do_") and docstr:
            cmds += [(i[3:], docstr)]

    cmds.sort()

    for cmd, docstr in cmds:
        if docstr.startswith("- "):
            # First line are arguments.
            docstr = docstr.splitlines()
            args = docstr[0][2:]
            docstr = "\n".join(docstr[1:])
        else:
            args = ""

        if args:
            args = f" *{args}*"

        output = ""
        for line in docstr.splitlines():
            output += f"    {line.strip()}\n"

        output = output.strip()

        print()
        print(f".. _{cmd}:\n\n*{cmd}*{args}\n    {output}")
        print()


# Print options documentation.
def print_options():
    print("User Options")
    print("~~~~~~~~~~~~")

    out, err = options.print_options(options.Option.USER)
    print(out, end="")
    if err:
        print(err, file=sys.stderr)

    print()
    print("Internal Options")
    print("~~~~~~~~~~~~~~~~")
    print()

    out, err = options.print_options(options.Option.AUTOMATIC)
    print(out, end="")
    if err:
        print(err, file=sys.stderr)


# Print plugin and node documentation.
def print_plugin():
    print(doc.print_class(plugin.Plugin, tag="no-methods"), end="")
    print(doc.print_class(plugin.Plugin, header=False), end="")
    print(doc.print_class(plugin.Plugin, "override", header=False), end="")

    print(doc.print_class(node.Node), end="")


def print_zeekctl_docs(mainpath, zeekctlclass):
    print(".. Autogenerated. Do not edit.\n")
    with open(mainpath) as f:
        for line in f:
            fields = line.strip().split(None, 2)
            if len(fields) == 3 and fields[0] == ".." and fields[1] == "include::":
                if fields[2] == "commands.rst":
                    print_commands(zeekctlclass)
                elif fields[2] == "options.rst":
                    print_options()
                elif fields[2] == "plugins.rst":
                    print_plugin()
            else:
                print(line, end="")
