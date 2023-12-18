import re
import time
import num2words
import pymorphy3

from .sets import MEASURES, MONTHS
from polyglot.transliteration import Transliterator


__MORPH = pymorphy3.MorphAnalyzer()
__TRANSLITERATOR = Transliterator(source_lang="en", target_lang="ru")

# Patterns
__DATE_SEP = re.compile(r'[/.]')
__DOT = re.compile(r'\.')
__AT = re.compile(r'@')
__ENG = re.compile(r'[A-Za-z]+')
__SPACE = re.compile(r'\s+')
__PROTOCOL = re.compile(r'http[s]?://')


def __morph_number(number, *case):
    case = {element for element in case if element}
    word = num2words.num2words(number, lang='ru')
    if case:
        word = " ".join([__MORPH.parse(word)[0].inflect(case).word for word in word.split()])
    return word


def __morph_ordinal_number(number, *case):
    case = {element for element in case if element}
    word = num2words.num2words(number, to='ordinal', lang='ru')
    if case:
        *head, tail = word.split()
        # 'Второй', 'восьмой', и т. д. интерпретируются как слова ж. р. Р. п.
        if int(number[-1]) in [2, 6, 8]:
            if not ('femn' in case or 'neut' in case):
                case.add('masc')
        word = (" ".join(head) + ' ' if head else '') + __MORPH.parse(tail)[0].inflect(case).word
    return word


def __morph_word(word, *case):
    case = {element for element in case if element}
    if case:
        word = " ".join([__MORPH.parse(w)[0].inflect(case).word for w in word.split()])
    return __MORPH.parse(word)[0]


def __parse_cardinal(word, *tags):
    _, case, _ = tags
    return __morph_number(word, case)


def __parse_address(word, *tags):
    tag_dict, case, lemma = tags
    if abbr := tag_dict.get('abbr'):
        new_lemma = __morph_word(lemma, case).word
        word = word.replace(abbr, new_lemma + ' ') if tag_dict.get('space') == '' else word.replace(abbr, new_lemma)
    if fraction := tag_dict.get('fraction'):
        word = word.replace(fraction, ' дробь ')
    if letter := tag_dict.get('letter'):
        word = word.replace(letter, ' ' + letter)
    return word


def __parse_phone(lang_match, *_):
    re_phone = [lang_match[:1],
                lang_match[1:4],
                lang_match[4:7],
                lang_match[7:9],
                lang_match[9:11]]
    return " ".join([__morph_number(num) for num in re_phone])


def __parse_decimal(lang_match, *tags):
    _, case, _ = tags
    whole_part, fractional_part = lang_match.split(',')

    whole = __morph_number(whole_part, case)
    fractional = __morph_number(fractional_part, case)

    match len(fractional_part):
        case 1 if fractional_part == '5' and whole_part != '0':
            return f"{whole} с половиной"
        case 1:
            return f"{whole} целых {fractional} десятых"
        case 2:
            return f"{whole} целых {fractional} сотых"
        case 3:
            return f"{whole} целых {fractional} тысячных"


def __parse_ordinal(lang_match, *tags):
    _, case, _ = tags
    num = lang_match.split('-')[0]

    match lang_match:
        case _ if lang_match.endswith('-й'):
            return __morph_ordinal_number(num, case)
        case _ if lang_match.endswith('-го'):
            return __morph_ordinal_number(num, 'gent')
        case _ if lang_match.endswith('-му'):
            return __morph_ordinal_number(num, 'datv')
        case _ if lang_match.endswith('-м'):
            return __morph_ordinal_number(num, 'ablt')
        case _ if lang_match.endswith('-ом'):
            return __morph_ordinal_number(num, 'loct')
        case _ if lang_match.endswith('я'):
            return __morph_ordinal_number(num, 'femn', 'nomn')
        case _ if lang_match.endswith('ю'):
            return __morph_ordinal_number(num, 'femn', 'accs')
        case _ if lang_match.endswith('-ой'):
            return __morph_ordinal_number(num, 'femn', 'gent')
        case _ if lang_match.endswith('-е'):
            return __morph_ordinal_number(num if int(num) < 10 else str(num), 'neut' if int(num) < 10 else 'plur')
        case _ if lang_match.endswith('-ей'):
            return __morph_ordinal_number(num, 'femn', 'datv')
        case _ if lang_match.endswith('-х'):
            try:
                return __morph_ordinal_number(num, 'ADJF', 'plur', 'gent')
            except AttributeError:
                return __morph_ordinal_number(num, 'plur', 'gent')


def __morph_time(time, case, minutes=False):
    match time:
        case '00':
            return 'ровно'
        case _ if time.startswith('0'):
            return (
                f"{__morph_number(time[0], case)} "
                f"{__morph_number(time[-1], case, 'femn' if time[-1] in ('1', '2') else None)} "
                f"{__morph_word('минута' if minutes else 'секунда', case).make_agree_with_number(int(time[-1])).word}"
            )
        case '10' | '11' | '12':
            return (
                f"{__morph_number(time, case)} "
                f"{__morph_word('минута' if minutes else 'секунда', case).make_agree_with_number(int(time)).word}"
            )
        case _ if time[-1] == '1':
            arr = __morph_number(time).split()
            return (
                f"{' '.join(arr[:-1])} {__morph_word(arr[-1], case, 'femn').word} "
                f"{__morph_word('минута' if minutes else 'секунда', case).make_agree_with_number(int(time)).word}"
            )
        case _:
            return (
                f"{__morph_number(time, case)} "
                f"{__morph_word('минута' if minutes else 'секунда', case).make_agree_with_number(int(time)).word}"
            )


def __parse_time(lang_match, *tags):
    _, case, _ = tags
    hours, minutes, *seconds = lang_match.split(':')
    return __morph_number(hours, case) + ' ' \
           + __morph_word('час', case).make_agree_with_number(int(hours)).word + ' ' \
           + __morph_time(minutes, case, minutes=True) \
           + (' ' + __morph_time(" ".join(seconds), case) if seconds else '')


def __parse_date(lang_match, *tags):
    _, case, _ = tags
    d, m, *y = re.split(__DATE_SEP, lang_match)
    if y:
        y = " ".join(y)
        if len(y) == 2:
            y = __morph_ordinal_number('20' + y, case) if int(y) < int(time.strftime('%Y')[-2:]) \
                else __morph_ordinal_number('19' + y, case)
        else:
            y = __morph_ordinal_number(y, case)
        *head, tail = y.split()
        y = f"{' '.join(head)} {__morph_word(tail, 'gent').word} года"
        return (
            f"{__morph_ordinal_number(d, 'neut', 'gent')} "
            f"{__morph_word(MONTHS[int(m)], 'gent').word} {y}"
        )
    return (
        f"{__morph_ordinal_number(d, 'masc', 'gent')} "
        f"{__morph_word(MONTHS[int(m)], 'gent').word}"
    )


def __parse_mail(lang_match, *tags):
    return re.sub(__DOT, ' точка ', re.sub(__AT, ' собака ', lang_match))


def __parse_url(lang_match, *tags):
    clean = re.sub(__DOT, ' точка ', re.sub(__PROTOCOL, '', lang_match))
    return " ".join([__TRANSLITERATOR.transliterate(w) if re.findall(__ENG, w) else w for w in clean.split()])


def __parse_measure(lang_match, *tags):
    _, case, _ = tags
    n, m = re.split(__SPACE, lang_match)
    return __morph_number(n, case) + ' ' + __MORPH.parse(MEASURES.get(m))[0].make_agree_with_number(int(n)).word


def __parse_latin(lang_match, *_):
    if lang_match == 'w':
        return 'дабл ю'
    return __TRANSLITERATOR.transliterate(lang_match)


def __final_parse(token, *_):
    token.text = token.text.lower()
    if token.text.isnumeric():
        token.text = token.text.replace(token.text, num2words.num2words(token.text, lang='ru'))
    elif re.findall(__ENG, token.text):
        token.text = re.sub(__ENG, __TRANSLITERATOR.transliterate(token.text), token.text)
    return token.text


interfaces = {
    'address': __parse_address,
    'decimal': __parse_decimal,
    'ordinal': __parse_ordinal,
    'cardinal': __parse_cardinal,
    'measure': __parse_measure,
    'phone': __parse_phone,
    'mail': __parse_mail,
    'url': __parse_url,
    'time': __parse_time,
    'date': __parse_date,
    'latin': __parse_latin
}
