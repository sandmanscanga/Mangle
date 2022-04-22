"""Module used to mangle username wordlists"""
import random


def mangle(name1, name2, domainonly, domain=None):
    """Mangle a pair of names"""

    mangled = []

    if domain is not None:
        mangled.append(f"{name1}{name2}@{domain}")
        mangled.append(f"{name1}.{name2}@{domain}")

    onlydomains = domain is not None and domainonly is True

    if not onlydomains:
        mangled.append(f"{name1}{name2}")
        mangled.append(f"{name1}.{name2}")

    return mangled


def mangle_combo(name1, name2, domainonly, domain=None):
    """Mangles a name combination excluding duplicate initials"""

    mangled_combo = []
    both_are_initials = len(name1) == 1 and len(name2) == 1
    if both_are_initials is False:
        mangled = mangle(name1, name2, domainonly, domain=domain)
        mangled_combo.extend(mangled)

    return mangled_combo


def get_name_combos(name, uppercase):
    """Generates name combinations according to rules"""

    combos = []
    combos.append(name.lower())
    combos.append(name.title())
    combos.append(name[0].lower())
    combos.append(name[0].upper())
    if uppercase is True:
        combos.append(name.upper())

    return combos


def mangle_bulk(name1, name2, uppercase, domainonly, domain=None):
    """Mangles all combinations of users"""

    mangled_bulk = []
    for name1_combo in get_name_combos(name1, uppercase):
        for name2_combo in get_name_combos(name2, uppercase):
            mangled = mangle_combo(
                name1_combo,
                name2_combo,
                domainonly,
                domain=domain
            )
            mangled_bulk.extend(mangled)

    return mangled_bulk


def main(args):
    """Run the user mangler main process"""

    # Load raw user names
    with open(args.infile, "r") as file:
        raw_names = file.read().strip().split("\n")

    mangled = []
    for raw_name in raw_names:
        firstname, lastname = raw_name.split()
        first_last_mangled = mangle_bulk(
            firstname,
            lastname,
            args.uppercase,
            args.domainonly,
            domain=args.domain,
        )
        last_first_mangled = mangle_bulk(
            lastname,
            firstname,
            args.uppercase,
            args.domainonly,
            domain=args.domain
        )
        mangled.extend(first_last_mangled)
        mangled.extend(last_first_mangled)

    # Remove case-insensitive duplicates
    if args.unique is True:
        mangled = list({name.lower() for name in mangled})

    # Sort mangled results
    if args.sort is True:
        mangled = sorted(mangled)
    elif args.random is True:
        random.shuffle(mangled)

    # Write mangled results to file
    if args.outfile:
        with open(args.outfile, "w") as file:
            file.write("\n".join(mangled) + "\n")

    # Display mangled results
    if args.quiet is False:
        for user in mangled:
            print(user)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="specify input filename")
    parser.add_argument(
        "-d", "--domain",
        required=False,
        help="specify email domain to add as mangled suffix"
    )
    parser.add_argument(
        "-D", "--domainonly",
        action="store_true",
        help="specify domain only flag to only include domain mangled users"
    )
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument(
        "-s", "--sort",
        action="store_true",
        help="specify sort flag to sort mangled users"
    )
    group1.add_argument(
        "-r", "--random",
        action="store_true",
        help="specify random flag to randomize mangled users"
    )
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument(
        "-U", "--uppercase",
        action="store_true",
        help="specify uppercase flag to include mangled uppercase users"
    )
    group2.add_argument(
        "-u", "--unique",
        action="store_true",
        help="specify unique flag to remove all case-insensitive duplicates"
    )
    parser.add_argument(
        "-o", "--outfile",
        required=False,
        help="specify output file to write mangled results"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="specify quiet flag to suppress output"
    )
    args = parser.parse_args()

    main(args)
