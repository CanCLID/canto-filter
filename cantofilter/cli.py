import argparse
import sys
from .judge import judge

sys.stdout.reconfigure(encoding='utf-8')


def main():
    """
    When used as a command line tool, specify input text file with `--input <INPUT.txt>`, and output mode with `--mode <MODE>`.
    """
    argparser = argparse.ArgumentParser(
        description='Specify input text file with `--input <INPUT.txt>`, where each line is a sentence. ')

    argparser.add_argument('--input', type=str, default='input.txt',
                           help='Specify input text file, where each line is a sentence. Default is `input.txt`.')
    argparser.add_argument('--mode', type=str, default='all',
                           help='Specify the mode of output. `all` for all sentences with a class label prepended, `cantonese`, `mandarin`, `mixed`, `neutral` for outputing certain types of sentences only. Default is `all`.')

    args = argparser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        for line in f:
            l = line.strip()
            judgement: str = judge(l)
            if args.mode == 'all':
                sys.stdout.write(f'{judgement}\t{l}\n')
            elif args.mode == 'label':
                sys.stdout.write(f'{judgement}\n')
            elif args.mode == judgement:
                sys.stdout.write(f'{l}\n')


if __name__ == '__main__':
    main()
