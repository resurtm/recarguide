from os import path as p

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates countries list Python file'

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        self.stdout.write('Generating countries list file...')

        file_path = p.dirname(p.realpath(__file__))
        file_path = p.join(file_path, 'data', 'countries.txt')

        countries = []

        with open(file_path) as fp:
            for line in fp:
                name, code, isd, cur_code, cur_sign = line.rstrip().split('\t')
                countries.append((name, code, isd, cur_code, cur_sign))

        out_path = p.dirname(p.dirname(p.dirname(p.realpath(__file__))))
        out_path = p.join(out_path, 'countries.py')

        pat1 = "    ({idx}, '{name}'),\n"
        pat2 = "    ({idx}, '{name}', '{code}', '{isd}', '{c1}', '{c2}'),\n"

        countries_fn = ('def get_countries(include_empty=True):\n'
                        '    result = [(c, n) for __, n, c, __, __, __ in full_countries]\n'
                        '    if include_empty:\n'
                        '        result.insert(0, (None, ""))\n'
                        '    return result\n')

        with open(out_path, 'w') as fp:
            fp.write('# id, name\n')
            fp.write('countries = [\n')
            for idx, country in enumerate(countries):
                name = country[0].replace("'", r"\'")
                fp.write(pat1.format(idx=idx + 1, name=name))
            fp.write(']\n\n')

            fp.write('# id, name, code, isd, currency code, currency symbol\n')
            fp.write('full_countries = [\n')
            for idx, country in enumerate(countries):
                name = country[0].replace("'", r"\'")
                code = country[1].replace("'", r"\'")
                isd = country[2].replace("'", r"\'")
                c1 = country[3].replace("'", r"\'")
                c2 = country[4].replace("'", r"\'")
                fp.write(pat2.format(idx=idx + 1, name=name, code=code, isd=isd,
                                     c1=c1, c2=c2))
            fp.write(']\n\n\n')
            fp.write(countries_fn)

        self.stdout.write(self.style.SUCCESS('Done!'))
