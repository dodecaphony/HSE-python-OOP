from re import compile


class Pattern:
    def __init__(self, name, pattern, lemma=None) -> None:
        self.name = name if not lemma else 'address'
        self.pattern = pattern
        self.lemma = lemma


address_patterns = [
    Pattern(
        'city',
        compile(r'((?P<abbr>\bг\b\.?|гор\.)|'
                r'(?P<id>\bгород.?\b))'
                r'(?P<space>\s*)'
                r'(?P<name>[А-ЯЁа-яё]{3,})'),
        'город'),
    Pattern(
        'street_before',
        compile(r'((?P<id>\bулиц.{1,3}\b)|'
                r'(?P<abbr>\bул\b\.?))'
                r'(?P<space>\s*)'
                r'(?P<name>[А-ЯЁа-яё]+)'),
        'улица'),
    Pattern(
        'street_after',
        compile(r'(?P<name>[-А-ЯЁ]+[-а-яё]+)'
                r'(?P<space>\s+)'
                r'((?P<id>\bулиц.{1,3}\b)|'
                r'(?P<abbr>\bул\b\.?))'),
        'улица'),
    Pattern(
        'district_before',
        compile(r'((?P<abbr>г\.о\.)'
                r'(?P<space>\s+)'
                r'(?P<name>[А-ЯЁа-яё]{2,}))'),
        'городской округ'),
    Pattern(
        'district_after',
        compile(r'(?P<name>[-А-ЯЁа-яё]{2,})'
                r'(?P<space>\s+)'
                r'(?P<abbr>г\.о\.)'),
        'городской округ'),
    Pattern(
        'area',
        compile(r'(?P<name>[А-ЯЁа-яё]+)(?P<space>\s+)'
                r'((?P<id>область)|'
                r'(?P<abbr>\bобл\b\.?))'),
        'область'),
    Pattern(
        'settlement',
        compile(r'((?P<id>посёлок)|'
                r'(?P<abbr>\bп\b\.))(?P<space>\s*)'
                r'(?P<name>[А-ЯЁа-яё]{2,})'),
        'посёлок'),
    Pattern(
        'city_settlement',
        compile(r'((?P<id>посёлок городского типа)|'
                r'(?P<abbr>\bпгт\b\.?))(?P<space>\s+)'
                r'(?P<name>[А-ЯЁа-яё]{2,})'),
        'посёлок городского типа'),
    Pattern(
        'village',
        compile(r'((?P<id>село)|'
                r'(?P<abbr>\bс\b\.))(?P<space>\s*)'
                r'(?P<name>[А-ЯЁа-яё]{2,})'),
        'село'),
    Pattern(
        'countryside',
        compile(r'((?P<id>\bдеревн.\b)|'
                r'(?P<abbr>\bд\b\.))(?P<space>\s*)'
                r'(?P<name>[А-ЯЁа-яё]{2,})'),
        'деревня'),
    Pattern(
        'rural_district',
        compile(r'((?P<id>сельский округ)|'
                r'(?P<abbr>\bс\/о\b\.?))(?P<space>\s+)'
                r'(?P<name>[-А-ЯЁа-яё]{2,})'),
        'сельский округ'),
    Pattern(
        'rural_settlement',
        compile(r'((?P<id>сельское поселение)|'
                r'(?P<abbr>\bс\/пос\b\.?))(?P<space>\s+)'
                r'(?P<name>[-А-ЯЁа-яё]{2,})'),
        'сельское поселение'),
    Pattern(
        'micro_district',
        compile(r'((?P<id>микрорайон)|'
                r'(?P<abbr>\bмкр\b\.?))(?P<space>\s+)'
                r'(?P<name>([А-ЯЁа-яё]{2,}))'),
        'микрорайон'),
    Pattern(
        'boulevard_before',
        compile(r'((?P<id>бульвар)|'
                r'(?P<abbr>\bб-р\b\.?))(?P<space>\s+)'
                r'(?P<name>[-А-ЯЁа-яё]{2,})'),
        'бульвар'),
    Pattern(
        'boulevard_after',
        compile(r'(?P<name>[А-ЯЁа-яё]{2,})(?P<space>\s+)'
                r'((?P<id>бульвар)|'
                r'(?P<abbr>\bб-р\b\.?))'),
        'бульвар'),
    Pattern(
        'house',
        compile(r'((?P<id>\bдом\b\.?)|'
                r'(?P<abbr>\bд\b\.?))(?P<space>\s*)'
                r'(?P<name>[0-9]+(?P<fraction>\/)?[0-9]*(?P<letter>[а-я])?)'),
        'дом'),
    Pattern(
        'block',
        compile(r'((?P<id>квартал)|'
                r'(?P<abbr>\bкв-л\b\.?))(?P<space>\s*)'
                r'(?P<name>[0-9]+)'),
        'квартал'),
    Pattern(
        'building',
        compile(r'((?P<id>строени..?)|'
                r'(?P<abbr>\bстр\b\.?))(?P<space>\s*)'
                r'(?P<name>[0-9]+([а-я])?)'),
        'строение'),
    Pattern(
        'housing',
        compile(r'((?P<id>корпус.?)|'
                r'(?P<abbr>\bк\b\.?|корп\.))(?P<space>\s*)'
                r'(?P<name>\d+([а-я])?)'),
        'корпус'),
    Pattern(
        'sector',
        compile(r'((?P<id>участок)|'
                r'(?P<abbr>\bуч\b\.?))(?P<space>\s*)'
                r'(?P<name>\d+[а-я]?)'),
        'участок'),
    Pattern(
        'alley',
        compile(r'(?P<name>[А-ЯЁа-яё]+)(?P<space>\s+)'
                r'((?P<id>алле.?.?)|'
                r'(?P<abbr>\bалл\b\.?))'),
        'аллея'),
    Pattern(
        'prospect_before',
        compile(r'((?P<id>проспект)|'
                r'(?P<abbr>\bпр-кт\b))(?P<space>\s+)'
                r'(?P<name>[-А-ЯЁа-яё]{2,})'),
        'проспект'),
    Pattern(
        'prospect_after',
        compile(r'(?P<name>[-А-ЯЁа-яё]{2,})(?P<space>\s+)'
                r'((?P<id>проспект)|'
                r'(?P<abbr>\bпр-кт\b))'),
        'проспект'),
    Pattern(
        'no_go',
        compile(r'(?P<name>[-А-ЯЁа-яё]{2,})(?P<space>\s+)'
                r'((?P<id>тупик)|'
                r'(?P<abbr>\bтуп\b\.?))'),
        'тупик'),
    Pattern(
        'highway',
        compile(r'(?P<name>[-А-ЯЁа-яё]{2,})(?P<space>\s+)'
                r'((?P<id>шоссе)|'
                r'(?P<abbr>\bш\b\.?))'),
        'шоссе'),
    Pattern(
        'lane',
        compile(r'(?P<name>[А-ЯЁа-яё]+)(?P<space>\s*)'
                r'((?P<id>переулок)|'
                r'(?P<abbr>\bпер\b\.?))'),
        'переулок'),
    Pattern(
        'flat',
        compile(r'((?P<id>квартир.?.?)|'
                r'(?P<abbr>\bкв\b\.?|кварт\.+?))(?P<space>\s*)'
                r'(?P<name>\d+([а-я])?)'),
        'квартира')
]

user_data_patterns = [
    Pattern(
        'mail',
        compile(r'[\w_.+-]+@[\w-]+\.[\w.]+')),
    Pattern(
        'phone',
        compile(r'(\+)?([-\s_()]?\d[-\s_()]?){10,14}')),
    Pattern(
        'url',
        compile(r'\w[\w-]+\w\.[^\s]{2,}|'
                r'www\.\w[\w-]+\w\.[^\s]{2,}|'
                r'https?:\/\/(?:www\.|(?!www))[\w]+\.[^\s]{2,}|'
                r'www\.\w+\.[^\s]{2,}|https?:\/\/(?:www\.|'
                r'(?!www))|[a-zA-Z][a-zA-Z]+\.[^\s]{2,}'))
]

date_time_patterns = [
    Pattern(
        'time',
        compile(r'(?P<hours>[01]?\d|2[0-4]):'
                r'(?P<minutes>[0-5]\d)'
                r'(:(?P<seconds>([0-5]\d)))?')),
    Pattern(
        'date',
        compile(r'(\d+\.\d+(\.\d+)?)|(0?[1-9]|[12]\d|3[01])'
                r'[\/.\-](0[1-9]|1[012])([\/.\-]\d{2,4})?|'
                r'(0?[1-9]|[12]\d|3[01])[\.](0[1-9]|1[012])'
                r'([\/.\-]\d{2,4})?|(0?[1-9]|[12]\d|3[01])'
                r'[\/](0[1-9]|1[012])([\-]\d{2,4})?')),
    Pattern(
        'date_slashed',
        compile(r'^(0?[1-9]|[12]\d|3[01])\/(0[1-9]|1[012])([\/.\-]\d{2,4})?$')),
    Pattern(
        'date_dotted',
        compile(r'^(0?[1-9]|[12]\d|3[01])\.(0[1-9]|1[012])([\/.\-]\d{2,4})?$')),
    Pattern(
        'date_hyphened',
        compile(r'^(0?[1-9]|[12]\d|3[01])\/(0[1-9]|1[012])([\-]\d{2,4})?$'))
]

number_patterns = [
    Pattern(
        'decimal',
        compile(r'\d+,\d+')),
    Pattern(
        'ordinal',
        compile(r'\d+\-(.?му?|.?го|.?я|.?ю|.?й|.?е|х)')),
    Pattern(
        'measure',
        compile(r'(\d+,\d+|\d+)\s*([дкмс]?[м][гл]?|л)'))
]

other_patterns = [
    Pattern(
        'cardinal',
        compile(r'\d+')),
    Pattern(
        'latin',
        compile(r'[A-Za-z]+'))
]
