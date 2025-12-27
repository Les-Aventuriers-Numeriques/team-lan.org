from babel.dates import get_timezone, format_date
from datetime import date, datetime

locale = 'fr_FR'
tzinfo = get_timezone('Europe/Paris')

USE_HTML_EXTENSION = False

WEBASSETS_BUNDLES = [
    ('css_base', ('css/base.css',), {'filters': 'rcssmin', 'output': 'css/base.css'}),
    ('css_lan', ('css/base.css', 'css/lan.css'), {'filters': 'rcssmin', 'output': 'css/lan.css'}),
]

team_name = 'Les Aventuriers Numériques'
motto = 'Une team multigaming francophone et conviviale'

CONTEXTS = [
    (r'index\.html', {
        'games_being_played': [
            ('Broken Arrow', 'https://store.steampowered.com/app/1604270/Broken_Arrow', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaav2.png'),
            ('Call to Arms: Gates of Hell', 'https://store.steampowered.com/app/400750/Call_to_Arms__Gates_of_Hell_Ostfront', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co3c8w.png'),
            ('Door Kickers 2', 'https://store.steampowered.com/app/1239080', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2g0w.png'),
            ('Hearts of Iron IV', 'https://store.steampowered.com/app/394360', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaaql.png'),
            ('Mindustry', 'https://store.steampowered.com/app/1127400', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coabei.png'),
            ('Parkitect', 'https://store.steampowered.com/app/453090', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1li8.png'),
            ('Rust', 'https://store.steampowered.com/app/252490', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coajjj.png'),
            ('Satisfactory', 'https://store.steampowered.com/app/526870', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co8tfy.png'),
            ('Squad', 'https://store.steampowered.com/app/393380', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaasd.png'),
        ],
        'previously_played_games': [
            ('10 Miles to Safety', 'https://store.steampowered.com/app/1015140/', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1sh5.png'),
            ('Age of Empires II: Definitive Edition', 'https://store.steampowered.com/app/813780', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coar0y.png'),
            ('Arma 2', 'https://store.steampowered.com/app/33900', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2ehb.png'),
            ('Arma 3', 'https://store.steampowered.com/app/107410', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaaut.png'),
            ('Call to Arms', 'https://store.steampowered.com/app/302670', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co28w1.png'),
            ('Company of Heroes', 'https://store.steampowered.com/app/228200', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2ht7.png'),
            ('Company of Heroes 2', 'https://store.steampowered.com/app/231430', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaayw.png'),
            ('Company of Heroes: Blitzkrieg Mod', 'https://store.steampowered.com/app/681590/Company_of_Heroes_Blitzkrieg_Mod/', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co8gzk.png'),
            ('Crusader Kings III', 'https://store.steampowered.com/app/1158310', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co90uu.png'),
            ('Delta Force', 'https://store.steampowered.com/app/2507950', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coa98y.png'),
            ('Door Kickers', 'https://store.steampowered.com/app/248610', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1r1y.png'),
            ('Hell Let Loose', 'https://store.steampowered.com/app/686810', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co6sqr.png'),
            ('Killing Floor', 'https://store.steampowered.com/app/1250', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2sn9.png'),
            ('Killing Floor 2', 'https://store.steampowered.com/app/232090', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2coc.png'),
            ('Men of War: Assault Squad 2', 'https://store.steampowered.com/app/244450', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co28sc.png'),
            ('Minecraft: Java Edition', 'https://minecraft.net/', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coa77e.png'),
            ('Prison Architect', 'https://store.steampowered.com/app/233450', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co62ch.png'),
            ('Project Reality: BF2', 'https://www.realitymod.com/', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2r0b.png'),
            ('PUBG: Battlegrounds', 'https://store.steampowered.com/app/578080', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaam4.png'),
            ('Rocket League', 'https://store.steampowered.com/app/252950', 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaiyq.png'),
            ('Running With Rifles', 'https://store.steampowered.com/app/270150', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1u0z.png'),
            ('Thunder Tier One', 'https://store.steampowered.com/app/377300', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2mg6.png'),
            ('War Thunder', 'https://store.steampowered.com/app/236390', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1p78.png'),
            ('World War Z', 'https://store.steampowered.com/app/699130/World_War_Z/', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2i4r.png'),
        ],
    }),
    (r'lan\.html', {
        'current_attendees': None, # 8,
        'max_attendees': None, # 14,
        'start_date': None, # date(2025, 11, 7),
        'end_date': None, # date(2025, 11, 12),
        'location': None, # {'name': 'Courtenay', 'url': 'https://maps.app.goo.gl/1pBpnWsVrg65qyNn9'},
    }),
]

JINJA_GLOBALS = {
    'social_links': [
        ('discord', 'https://discord.gg/vQYv4MfQf8'),
        ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
        ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
    ],
    'team_name': team_name,
    'motto': motto,
    'now': datetime.now(tz=tzinfo),
    'team_founded': date(2024, 3, 8),
}


def dateformat(*args, **kwargs):
    return format_date(*args, **kwargs, locale=locale)


JINJA_FILTERS = {
    'dateformat': dateformat,
}
