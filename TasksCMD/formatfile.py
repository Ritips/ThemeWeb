import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--frame-height", type=int)
parser.add_argument("--frame-width", type=int)
parser.add_argument("file", type=str)


def format_text_block(frame_height, frame_width, file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f_read:
            data = list(f_read.readlines())
            symbol_count = 0
            text_return = []
            tmp_list_symbols = []
            for string in data:
                if len(text_return) == frame_height:
                    break
                if len(string) <= 1:
                    symbol_count = 0
                    text_return.append('\n')
                else:
                    for symbol in string:
                        if len(text_return) == frame_height:
                            break
                        if symbol == '\n':
                            symbol_count = 0
                            if tmp_list_symbols:
                                text_return.append(''.join(tmp_list_symbols) + '\n')
                                tmp_list_symbols.clear()
                        else:
                            tmp_list_symbols.append(symbol)
                            symbol_count += 1
                            if symbol_count == frame_width:
                                if len(text_return) != frame_height - 1:
                                    tmp_list_symbols.append('\n')
                                text_return.append(''.join(tmp_list_symbols))
                                tmp_list_symbols.clear()
                                symbol_count = 0
                        if len(text_return) == frame_height:
                            break
        #  print(text_return)
        return ''.join(text_return)
    except Exception as er:
        return er


if __name__ == '__main__':
    args = parser.parse_args()
    print(format_text_block(args.frame_height, args.frame_width, args.file))
