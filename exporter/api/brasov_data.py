DEFAULT_COLORS = {"route_color": "000000", "route_text_color": "FFFFFF"}
COLOR_MAP = {
    # TODO: Grab colors from official website (check out style.css)
    # https://ratbv.ro/trasee-si-orare/
    "Linia 1": {"route_color": "fcf81d", "route_text_color": "000000"},
    "Linia 2": {"route_color": "00bd47", "route_text_color": "000000"},
    "Linia 3": {"route_color": "a9aea8", "route_text_color": "000000"},
    "Linia 4": {"route_color": "6b99ba", "route_text_color": "000000"},
    "Linia 5": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 5M": {"route_color": "fd7306", "route_text_color": "000000"},
    "Linia 6": {"route_color": "01a98f", "route_text_color": "000000"},
    "Linia 7": {"route_color": "fd7306", "route_text_color": "000000"},
    "Linia 9": {"route_color": "efe44e", "route_text_color": "000000"},
    "Linia 8": {"route_color": "ecc1df", "route_text_color": "000000"},
    "Linia 10": {"route_color": "b31f37", "route_text_color": "000000"},
    "Linia 14": {"route_color": "4bba3a", "route_text_color": "000000"},
    "Linia 15": {"route_color": "030d91", "route_text_color": "000000"},
    "Linia 16": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 17": {"route_color": "65eded", "route_text_color": "000000"},
    "Linia 17B": {"route_color": "fdf681", "route_text_color": "000000"},
    "Linia 18": {"route_color": "ed839a", "route_text_color": "000000"},
    "Linia 20 Expres": {"route_color": "b1f000", "route_text_color": "000000"},
    "Linia 21": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 22": {"route_color": "006bc5", "route_text_color": "000000"},
    "Linia 23": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 23B": {"route_color": "db33a4", "route_text_color": "000000"},
    "Linia 24": {"route_color": "db33a4", "route_text_color": "000000"},
    "Linia 25": {"route_color": "a2e9bd", "route_text_color": "000000"},
    "Linia 28": {"route_color": "efe44e", "route_text_color": "000000"},
    "Linia 29": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 31": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 32": {"route_color": "113bab", "route_text_color": "000000"},
    "Linia 33": {"route_color": "c4c4c4", "route_text_color": "000000"},
    "Linia 34": {"route_color": "9c9c9c", "route_text_color": "000000"},
    "Linia 34B": {"route_color": "ecc1df", "route_text_color": "000000"},
    "Linia 35": {"route_color": "af90a0", "route_text_color": "000000"},
    "Linia 36": {"route_color": "338185", "route_text_color": "000000"},
    "Linia 37": {"route_color": "6e3710", "route_text_color": "000000"},
    "Linia 40": {"route_color": "ff9d1c", "route_text_color": "000000"},
    "Linia 41": {"route_color": "56abc0", "route_text_color": "000000"},
    "Linia 50": {"route_color": "e30e78", "route_text_color": "000000"},
    "Linia 51": {"route_color": "beb53e", "route_text_color": "000000"},
    "Linia 52": {"route_color": "a1d7d7", "route_text_color": "000000"},
    "Linia 53": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 120": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 210": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 220": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 310": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 420": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 520": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 540": {"route_color": "2391d0", "route_text_color": "000000"},
}

STOP_LIST = [
    {"label": "Valea Cetatii", "latitude": 45.630_613_8, "longitude": 25.601_677},
    {"label": "Toamnei", "latitude": 45.652_549_6, "longitude": 25.615_627_1},
    {"label": "Avantgarden", "latitude": 45.665_319_8, "longitude": 25.556_325},
    {"label": "Livada Postei", "latitude": 45.645_514_5, "longitude": 25.588_325},
    {"label": "Sanitas", "latitude": 45.649_333_6, "longitude": 25.600_423_2},
    {"label": "Onix", "latitude": 45.653_442, "longitude": 25.603_991_7},
    {"label": "Biserica Bartolomeu", "latitude": 45.662_822, "longitude": 25.578_067},
    {"label": "Ignis", "latitude": 45.649_883, "longitude": 25.559_381},
    {"label": "Ec. Teodoroiu", "latitude": 45.665_365, "longitude": 25.584_127},
    {"label": "Molnar Janos", "latitude": 45.665_488, "longitude": 25.568_329},
    {"label": "N. Labis", "latitude": 45.678_882_3, "longitude": 25.614_212_7},
    {
        "label": "Academia Henri Coanda",
        "latitude": 45.662_281_2,
        "longitude": 25.593_182_3,
    },
    {"label": "Triaj", "latitude": 45.675_677_100_000_01, "longitude": 25.647_312_1},
    {"label": "Rasaritul", "latitude": 45.653_393, "longitude": 25.56628},
    {"label": "Tudor Vladimirescu", "latitude": 45.664_863_2, "longitude": 25.594_011},
    {"label": "Plevnei", "latitude": 45.660_356, "longitude": 25.59631},
    {"label": "Coresi", "latitude": 45.668_853, "longitude": 25.629_482},
    {"label": "Vectra", "latitude": 45.663_996, "longitude": 25.570_035},
    {"label": "Carierei", "latitude": 45.657_975, "longitude": 25.578_446},
    {"label": "Rulmentul", "latitude": 45.682_184, "longitude": 25.614_951},
    {"label": "Dramatic", "latitude": 45.645_274_5, "longitude": 25.598_257_2},
    {"label": "Agricultorilor", "latitude": 45.666_568, "longitude": 25.572_631},
    {"label": "Piata Tractorul", "latitude": 45.665_968, "longitude": 25.604_892},
    {"label": "Bisericii Romane", "latitude": 45.651_695, "longitude": 25.586_021},
    {"label": "Huniade", "latitude": 45.666_560_999_999_99, "longitude": 25.588_858_9},
    {"label": "Vlahuta", "latitude": 45.657_715_2, "longitude": 25.622_170_5},
    {
        "label": "Carierei*",
        "latitude": 45.658_088_199_999_99,
        "longitude": 25.580_633_1,
    },
    {"label": "Liceul Mesota", "latitude": 45.653_912, "longitude": 25.609_261_6},
    {"label": "Fragilor", "latitude": 45.633_067_999_999_99, "longitude": 25.605_555_5},
    {"label": "Tractorul", "latitude": 45.664_776, "longitude": 25.608_927},
    {
        "label": "Camera de Comert",
        "latitude": 45.651_061_899_999_99,
        "longitude": 25.608_276_1,
    },
    {
        "label": "Stadionul Tineretului",
        "latitude": 45.665_037_5,
        "longitude": 25.583_356_1,
    },
    {"label": "Faget", "latitude": 45.661_027, "longitude": 25.607_768},
    {"label": "Sc. Gen. 25", "latitude": 45.634_097_6, "longitude": 25.605_987_3},
    {"label": "Auchan Coresi", "latitude": 45.672_937, "longitude": 25.618_411},
    {"label": "Berzei", "latitude": 45.639_639_4, "longitude": 25.627_116_3},
    {"label": "Castanilor", "latitude": 45.649_182_1, "longitude": 25.604_190_3},
    {"label": "Primarie", "latitude": 45.646_530_299_999_99, "longitude": 25.596_260_7},
    {"label": "1 Decembrie 1918", "latitude": 45.666_568_2, "longitude": 25.598_536_1},
    {"label": "RAT Brasov", "latitude": 45.669_643, "longitude": 25.636_790_3},
    {"label": "Lanurilor", "latitude": 45.662_347, "longitude": 25.567_782_1},
    {"label": "CEC", "latitude": 45.654_601_000_000_01, "longitude": 25.615_245},
    {
        "label": "Autogara 3",
        "latitude": 45.663_395_000_000_01,
        "longitude": 25.629_060_1,
    },
    {"label": "Universitate", "latitude": 45.655_924, "longitude": 25.600_044},
    {"label": "Memorandului", "latitude": 45.654_966_2, "longitude": 25.583_075_5},
    {"label": "Zlatna", "latitude": 45.666_771_999_999_99, "longitude": 25.574_782},
    {"label": "Egretei", "latitude": 45.664_233_8, "longitude": 25.565_329_1},
    {"label": "Astra", "latitude": 45.647_333_3, "longitude": 25.589_327_8},
    {"label": "Fartec", "latitude": 45.666_141, "longitude": 25.589_035_9},
    {"label": "Marasesti", "latitude": 45.648_621_7, "longitude": 25.605_305_8},
    {"label": "Muncii", "latitude": 45.639_933_9, "longitude": 25.611_260_5},
    {"label": "Sc. Gen. 20", "latitude": 45.637_925, "longitude": 25.609_383},
    {"label": "Liceul Tractorul", "latitude": 45.668_581_3, "longitude": 25.610_155_5},
    {
        "label": "Mircea cel Batran",
        "latitude": 45.656_958_499_999_99,
        "longitude": 25.606_358_2,
    },
    {"label": "Caprioara", "latitude": 45.659_648_1, "longitude": 25.614_844_1},
    {"label": "F-ca de Var", "latitude": 45.643_260_9, "longitude": 25.624_210_5},
    {"label": "13 Decembrie", "latitude": 45.654_020_4, "longitude": 25.605_366_2},
    {"label": "Coresi 2", "latitude": 45.66986, "longitude": 25.621_812_1},
    {"label": "Saturn", "latitude": 45.634_544_299_999_99, "longitude": 25.63548},
    {"label": "Atelier", "latitude": 45.655_249_7, "longitude": 25.592_155_4},
    {"label": "Dambul Morii", "latitude": 45.594_584, "longitude": 25.634_977},
    {"label": "Hidro B", "latitude": 45.651_378, "longitude": 25.614_030_5},
    {"label": "Judetean", "latitude": 45.647_288, "longitude": 25.619_313},
    {"label": "Spitalul Judetean", "latitude": 45.647_288, "longitude": 25.619_313},
    {"label": "Facultativa**", "latitude": 45.657_975_5, "longitude": 25.601_197_7},
    {"label": "Hidro A", "latitude": 45.651_228, "longitude": 25.610_007_5},
    {"label": "Facultativa", "latitude": 45.648_398, "longitude": 25.530_777_9},
    {"label": "Biserica Tractorul", "latitude": 45.664_776, "longitude": 25.608_927},
    {"label": "Patria", "latitude": 45.648_621_7, "longitude": 25.605_305_8},
    {"label": "Rapid", "latitude": 45.659_648_1, "longitude": 25.614_844_1},
    {"label": "Carpatilor", "latitude": 45.64182, "longitude": 25.614_699},
    {"label": "Metabras", "latitude": 45.676_453, "longitude": 25.588_306},
    {"label": "Bd. Garii", "latitude": 45.660_813_999_999_99, "longitude": 25.613_418},
    {"label": "Energo", "latitude": 45.653_483, "longitude": 25.653_081},
    {"label": "IUS", "latitude": 45.656_460_7, "longitude": 25.618_341},
    {"label": "Piata Decebal", "latitude": 45.644_048, "longitude": 25.618_207},
    {"label": "Statie Epurare", "latitude": 45.680_881_7, "longitude": 25.572_957_4},
    {"label": "Gemenii", "latitude": 45.649_448_000_000_01, "longitude": 25.628_506},
    {"label": "Campus Genius", "latitude": 45.668_525, "longitude": 25.549_028},
    {"label": "Facultativa*", "latitude": 45.648_398, "longitude": 25.530_777_9},
    {"label": "Artera Sud-Est", "latitude": 45.629_532, "longitude": 25.654_986},
    {"label": "Carrefour", "latitude": 45.631_603, "longitude": 25.637_197},
    {"label": "Cosmesti", "latitude": 45.666_508, "longitude": 25.579_412},
    {"label": "Neptun", "latitude": 45.641_753, "longitude": 25.63532},
    {"label": "CET", "latitude": 45.661_623_2, "longitude": 25.640_872},
    {"label": "Varistei", "latitude": 45.629_433, "longitude": 25.568_957},
    {"label": "Diversitas", "latitude": 45.657_585, "longitude": 25.643_914},
    {"label": "Praktiker", "latitude": 45.630_515, "longitude": 25.63789},
    {"label": "Autogara 2", "latitude": 45.663_530_6, "longitude": 25.582_934_4},
    {"label": "Gh. Doja", "latitude": 45.667_685, "longitude": 25.577_942},
    {"label": "Cimitirul Central", "latitude": 45.672_738, "longitude": 25.575_189_1},
    {"label": "Oitelor", "latitude": 45.693_119, "longitude": 25.563_045_1},
    {"label": "IAR Ghimbav", "latitude": 45.663_299_1, "longitude": 25.507_228_4},
    {"label": "Panait Cerna", "latitude": 45.650_633, "longitude": 25.626_125},
    {"label": "Caramidariei", "latitude": 45.65838, "longitude": 25.563_361_9},
    {"label": "Bronzului", "latitude": 45.668_338_000_000_01, "longitude": 25.597_115},
    {"label": "Benzinaria Petrom", "latitude": 45.633_187_5, "longitude": 25.634_564_2},
    {"label": "Soarelui", "latitude": 45.637_016_5, "longitude": 25.631_421_9},
    {
        "label": "Liceul Informatica",
        "latitude": 45.643_337_5,
        "longitude": 25.624_186_1,
    },
    {"label": "Pavilioanele CFR", "latitude": 45.65982, "longitude": 25.632_079_9},
    {"label": "Turnului", "latitude": 45.659_648_1, "longitude": 25.614_844_1},
    {"label": "Poienelor", "latitude": 45.631_769_1, "longitude": 25.629_517},
    {"label": "Infostar", "latitude": 45.655_009_3, "longitude": 25.612_596_3},
    {"label": "Cernatului", "latitude": 45.649_055_999_999_99, "longitude": 25.651_757},
    {
        "label": "Complexul Mare",
        "latitude": 45.643_849_499_999_99,
        "longitude": 25.632_664_6,
    },
    {
        "label": "Facultativa Timis-Triaj",
        "latitude": 45.666_898,
        "longitude": 25.649_428,
    },
    {"label": "Morii", "latitude": 45.658_028, "longitude": 25.587_384},
    {"label": "Brancoveanu", "latitude": 45.639_159_4, "longitude": 25.582_833_1},
    {"label": "Coresi 1", "latitude": 45.668_853, "longitude": 25.629_482},
    {"label": "Halta Timisul de Jos", "latitude": 45.584_056, "longitude": 25.623_068},
    {"label": "Cineplex Coresi", "latitude": 45.671_791_8, "longitude": 25.613_591_5},
    {"label": "Silnef", "latitude": 45.663_261_8, "longitude": 25.585_580_1},
    {"label": "Roman", "latitude": 45.632_836_999_999_99, "longitude": 25.632_512_9},
    {"label": "Spital Marzescu", "latitude": 45.647_288, "longitude": 25.619_313},
    {"label": "Lujerului", "latitude": 45.714_389_999_999_99, "longitude": 25.551_206},
    {"label": "Branduselor", "latitude": 45.653_625_7, "longitude": 25.624_103},
    {"label": "Baumax", "latitude": 45.673_229, "longitude": 25.589_765},
    {
        "label": "Stupini Izvorului",
        "latitude": 45.702_300_000_000_01,
        "longitude": 25.555_653,
    },
    {"label": "Toamnei(CEC)", "latitude": 45.652_549_6, "longitude": 25.615_627_1},
    {"label": "Brintex", "latitude": 45.657_113, "longitude": 25.559_274},
    {"label": "Invatatorilor", "latitude": 45.627_904, "longitude": 25.56805},
    {"label": "Warte", "latitude": 45.646_103_3, "longitude": 25.577_040_9},
    {"label": "Traian", "latitude": 45.650_123_4, "longitude": 25.623_203_1},
    {"label": "Elmas", "latitude": 45.687_528_000_000_01, "longitude": 25.582_899},
    {"label": "Independentei", "latitude": 45.666_494_2, "longitude": 25.595_760_4},
    {"label": "Dimitrie Anghel", "latitude": 45.669_005, "longitude": 25.576_226},
    {
        "label": "Unitate Militara",
        "latitude": 45.676_307_000_000_01,
        "longitude": 25.58041,
    },
    {"label": "Hotel Trifan", "latitude": 45.670_973, "longitude": 25.590_543},
    {"label": "Pantex", "latitude": 45.60705, "longitude": 25.653_741},
    {"label": "Stadionul Municipal", "latitude": 45.659_872, "longitude": 25.569_987},
    {"label": "Podul Cretului", "latitude": 45.626_344, "longitude": 25.566_441},
    {"label": "Metrom", "latitude": 45.634_694, "longitude": 25.624_213},
    {"label": "Avicola Magurele", "latitude": 45.628_325, "longitude": 25.521_197},
    {
        "label": "Fundatura Harmanului",
        "latitude": 45.674_199_3,
        "longitude": 25.646_963_8,
    },
    {"label": "Hornbach", "latitude": 45.660_892, "longitude": 25.550_745},
    {"label": "Dacia", "latitude": 45.658_068_9, "longitude": 25.612_709},
    {"label": "Brintex*", "latitude": 45.657_113, "longitude": 25.559_274},
    {"label": "Rozmarinului", "latitude": 45.61899, "longitude": 25.637_326},
    {"label": "Stupinii Noi", "latitude": 45.720_472_5, "longitude": 25.570_910_2},
    {
        "label": "Tineretului (Cristian)",
        "latitude": 45.62853,
        "longitude": 25.481_581_8,
    },
    {"label": "Facultativa***", "latitude": 45.657_975_5, "longitude": 25.601_197_7},
    {"label": "Posta", "latitude": 45.667_924_6, "longitude": 25.571_074_8},
    {"label": "Plugarilor", "latitude": 45.680_881_7, "longitude": 25.572_957_4},
    {
        "label": "Fagurului",
        "latitude": 45.705_324_999_999_99,
        "longitude": 25.572_040_9,
    },
    {"label": "Rial", "latitude": 45.651_495_999_999_99, "longitude": 25.595_527},
    {
        "label": "Spital Tractorul",
        "latitude": 45.665_862_999_999_99,
        "longitude": 25.608_702_1,
    },
    {"label": "Timis Triaj", "latitude": 45.666_898, "longitude": 25.649_428},
    {"label": "Albinelor", "latitude": 45.687_453, "longitude": 25.545_552_1},
    {"label": "Depozite ILF", "latitude": 45.65838, "longitude": 25.563_361_9},
    {"label": "Craiter", "latitude": 45.656_910_3, "longitude": 25.633_522_9},
    {"label": "Junilor", "latitude": 45.629_773, "longitude": 25.57128},
    {"label": "Pompieri", "latitude": 45.637_155, "longitude": 25.622_295},
    {"label": "Ioan Clopotel", "latitude": 45.652_126, "longitude": 25.542_612},
    {"label": "Bellevue Residence", "latitude": 45.645_213_5, "longitude": 25.580_207},
    {"label": "Bariera Bartolomeu", "latitude": 45.664_274, "longitude": 25.577_953},
    {
        "label": "Romradiatoare",
        "latitude": 45.649_077_100_000_01,
        "longitude": 25.644_548_1,
    },
    {"label": "Aurora", "latitude": 45.617_662, "longitude": 25.651_754},
    {"label": "Biserica", "latitude": 45.664_776, "longitude": 25.608_927},
    {"label": "Liceul CFR", "latitude": 45.672_978, "longitude": 25.645_673},
    {"label": "Toamnei*", "latitude": 45.652_549_6, "longitude": 25.615_627_1},
    {"label": "Camine IAR", "latitude": 45.671_035, "longitude": 25.565_778_5},
    {"label": "Vulturului", "latitude": 45.639_286_2, "longitude": 25.619_711},
    {"label": "Bartolomeu Gara", "latitude": 45.662_661_7, "longitude": 25.574_600_1},
    {"label": "Parc Ind. Metrom", "latitude": 45.634_453, "longitude": 25.622_775_8},
    {"label": "Carfil", "latitude": 45.64918, "longitude": 25.647_395},
    {"label": "Cometei", "latitude": 45.63855, "longitude": 25.636_339},
    {"label": "Surlasului", "latitude": 45.693_613, "longitude": 25.552_418_1},
    {"label": "ICPC", "latitude": 45.673_158, "longitude": 25.542_709},
    {"label": "Piata Unirii", "latitude": 45.636_187, "longitude": 25.57924},
    {"label": "Poligrafie", "latitude": 45.648_931, "longitude": 25.640_641},
    {"label": "Iancu Jianu", "latitude": 45.660_427, "longitude": 25.600_816},
    {"label": "Star", "latitude": 45.644_806, "longitude": 25.598_713},
    {"label": "Facultativa II", "latitude": 45.648_398, "longitude": 25.530_777_9},
    {
        "label": "Biserica Neagra",
        "latitude": 45.640_391_400_000_01,
        "longitude": 25.585_655_3,
    },
    {"label": "Liceul Saguna", "latitude": 45.653_912, "longitude": 25.609_261_6},
    {"label": "Silver Mountain", "latitude": 45.604_879, "longitude": 25.54359},
    {"label": "Solomon", "latitude": 45.617_525_099_999_99, "longitude": 25.558_469_3},
    {
        "label": "Complex Bartolomeu",
        "latitude": 45.663_584_9,
        "longitude": 25.578_841_7,
    },
    {"label": "Magurele", "latitude": 45.636_126_999_999_99, "longitude": 25.523_686},
    {"label": "Merilor", "latitude": 45.690_475_600_000_01, "longitude": 25.566_191_3},
    {"label": "La Moara", "latitude": 45.657_975_5, "longitude": 25.601_197_7},
    {"label": "Sala Sporturilor", "latitude": 45.659_045_7, "longitude": 25.620_821_3},
    {"label": "Metro", "latitude": 45.622_209, "longitude": 25.646_676},
    {"label": "Pensiunea Stupina", "latitude": 45.686_708, "longitude": 25.569_921},
    {
        "label": "Sc. Gen. 4",
        "latitude": 45.637_661_000_000_01,
        "longitude": 25.612_853_8,
    },
    {"label": "Conforest", "latitude": 45.671_379_5, "longitude": 25.578_973_5},
    {"label": "Int. Ceferistilor", "latitude": 45.656_595, "longitude": 25.631_522},
    {"label": "Tocile", "latitude": 45.633_124_2, "longitude": 25.576_456_2},
    {
        "label": "Scriitorilor",
        "latitude": 45.650_505_500_000_01,
        "longitude": 25.620_652_3,
    },
    {"label": "Tipografia Brastar", "latitude": 45.697_849, "longitude": 25.582_073},
    {"label": "Selgros", "latitude": 45.624_402_6, "longitude": 25.644_803_2},
    {"label": "Dedeman", "latitude": 45.67905, "longitude": 25.586_858},
    {"label": "Facultativa (MTI)", "latitude": 45.648_398, "longitude": 25.530_777_9},
    {
        "label": "Patinoarul Olimpic",
        "latitude": 45.663_748_4,
        "longitude": 25.612_334_3,
    },
    {"label": "Service", "latitude": 45.65961, "longitude": 25.566_741},
    {"label": "Strand Noua", "latitude": 45.615_453_9, "longitude": 25.640_585_2},
    {"label": "Piata Auto", "latitude": 45.664, "longitude": 25.555_342},
    {"label": "Oligopol", "latitude": 45.682_348_999_999_99, "longitude": 25.581_729},
    {"label": "Panselelor", "latitude": 45.627_529, "longitude": 25.622_478},
    {"label": "Fantanii", "latitude": 45.708_144_399_999_99, "longitude": 25.577_247_1},
    {"label": "Baciului CL", "latitude": 45.715_795, "longitude": 25.588_896_1},
    {"label": "Noua", "latitude": 45.620_183, "longitude": 25.634},
    {
        "label": "Aleea Tiberiu Brediceanu",
        "latitude": 45.638_936_4,
        "longitude": 25.593_184_8,
    },
    {"label": "Poiana Darste", "latitude": 45.616_414, "longitude": 25.645_326_9},
    {
        "label": "Piata Agroalimentara",
        "latitude": 45.665_688_8,
        "longitude": 25.604_235,
    },
    {"label": "Mondotrans", "latitude": 45.706_104, "longitude": 25.580_377_9},
    {"label": "Telecabina", "latitude": 45.638_936_4, "longitude": 25.593_184_8},
    {
        "label": "Dulgherului",
        "latitude": 45.656_958_499_999_99,
        "longitude": 25.606_358_2,
    },
    {"label": "Mol", "latitude": 45.68437, "longitude": 25.58274},
    {"label": "Eroilor", "latitude": 45.645_514_5, "longitude": 25.588_325},
    {"label": "Opera Brasov", "latitude": 45.654_611_1, "longitude": 25.589_884_9},
    {"label": "Prunului", "latitude": 45.656_958_499_999_99, "longitude": 25.606_358_2},
    {"label": "Agetaps", "latitude": 45.688_705_9, "longitude": 25.581_594_2},
    {"label": "Balcescu", "latitude": 45.641_619_8, "longitude": 25.592_560_3},
    {
        "label": "Str. Izvorului",
        "latitude": 45.702_300_000_000_01,
        "longitude": 25.555_653,
    },
    {"label": "Fundaturii", "latitude": 45.685_755, "longitude": 25.541_413},
    {"label": "Targ Auto", "latitude": 45.664, "longitude": 25.555_342},
    {"label": "Iveco", "latitude": 45.682_978, "longitude": 25.584_294},
    {"label": "Poiana Mica", "latitude": 45.608_063_7, "longitude": 25.554_207_4},
    {"label": "Feldioarei", "latitude": 45.708_153, "longitude": 25.579_734},
    {
        "label": "Stupini Izvorului spre Lujerului",
        "latitude": 45.702_366,
        "longitude": 25.555_766,
    },
    {"label": "Stupini Centru", "latitude": 45.698_023, "longitude": 25.558_432},
    {"label": "Ceferistilor", "latitude": 45.6604, "longitude": 25.6259},
    {"label": "Gara Brasov", "latitude": 45.659_648_1, "longitude": 25.614_844_1},
    {"label": "Papa Reale", "latitude": 45.665_406, "longitude": 25.643_935},
    {"label": "Pod Barsa", "latitude": 45.682_648, "longitude": 25.553_421},
    {"label": "Str. Baciului", "latitude": 45.715_795, "longitude": 25.588_896_1},
    {"label": "Scoala", "latitude": 45.637_661_000_000_01, "longitude": 25.612_853_8},
    {"label": "Centru", "latitude": 45.657_715_2, "longitude": 25.622_170_5},
    {"label": "Iuliu Maniu", "latitude": 45.649_333_6, "longitude": 25.600_423_2},
    {"label": "Bartolomeu Nord", "latitude": 45.664_274, "longitude": 25.577_953},
    {
        "label": "Izvorului spre Baciului",
        "latitude": 45.702_103,
        "longitude": 25.556_061,
    },
    {"label": "Fundaturii cl", "latitude": 45.683_117, "longitude": 25.543_218},
    {"label": "Piata Sfatului", "latitude": 45.647_333_3, "longitude": 25.589_327_8},
    {
        "label": "Facultate Constructii",
        "latitude": 45.659_648_1,
        "longitude": 25.614_844_1,
    },
    {"label": "Str. Fagurului", "latitude": 45.698_023, "longitude": 25.558_432},
    {"label": "Roplant", "latitude": 45.660_892, "longitude": 25.55598},
    {"label": "Sc. Gen. 9", "latitude": 45.615_313, "longitude": 25.630_739},
    {"label": "Case", "latitude": 45.643_260_9, "longitude": 25.624_210_5},
    {"label": "Univ. Spiru Haret", "latitude": 45.664_776, "longitude": 25.608_927},
    {"label": "Stad. Municipal", "latitude": 45.659_872, "longitude": 25.569_987},
    {"label": "Poiana Brasov", "latitude": 45.59486, "longitude": 25.553_191},
]
STOP_MAP = {r["label"]: r for r in STOP_LIST}

"""
TODO: add missing GPS positions or map mismatched positions

brasov.py                  219 ERROR    Mising GPS position for stop: Fabrica de Var
brasov.py                  219 ERROR    Mising GPS position for stop: Colegiul N. Titulescu
brasov.py                  219 ERROR    Mising GPS position for stop: Pelicanului
brasov.py                  219 ERROR    Mising GPS position for stop: Racordnorm
brasov.py                  219 ERROR    Mising GPS position for stop: Facultativa Izv.
brasov.py                  219 ERROR    Mising GPS position for stop: Facultativa Fundaturii
brasov.py                  219 ERROR    Mising GPS position for stop: Liziera Brasov
brasov.py                  219 ERROR    Mising GPS position for stop: Cap Linie Rasnov
brasov.py                  219 ERROR    Mising GPS position for stop: Caragiale
brasov.py                  219 ERROR    Mising GPS position for stop: Biserica Rasnov
brasov.py                  219 ERROR    Mising GPS position for stop: Primaria Veche
brasov.py                  219 ERROR    Mising GPS position for stop: Mihai Viteazul
brasov.py                  219 ERROR    Mising GPS position for stop: F.S.R.
brasov.py                  219 ERROR    Mising GPS position for stop: Liceul Tehnologic
brasov.py                  219 ERROR    Mising GPS position for stop: Lukoil
brasov.py                  219 ERROR    Mising GPS position for stop: Blocurile MAN
brasov.py                  219 ERROR    Mising GPS position for stop: Unit. Militara (Cristian)
brasov.py                  219 ERROR    Mising GPS position for stop: Centru (Cristian)
brasov.py                  219 ERROR    Mising GPS position for stop: Eroilor (Cristian)
brasov.py                  219 ERROR    Mising GPS position for stop: Oituz
brasov.py                  219 ERROR    Mising GPS position for stop: Cos 2000
brasov.py                  219 ERROR    Mising GPS position for stop: Scoala (Cristian)
brasov.py                  219 ERROR    Mising GPS position for stop: Florilor
brasov.py                  219 ERROR    Mising GPS position for stop: Ghimbav Cap Linie
brasov.py                  219 ERROR    Mising GPS position for stop: Crizantemei
brasov.py                  219 ERROR    Mising GPS position for stop: Gentianei
brasov.py                  219 ERROR    Mising GPS position for stop: Tess
brasov.py                  219 ERROR    Mising GPS position for stop: Diamant
brasov.py                  219 ERROR    Mising GPS position for stop: Fagarasului
brasov.py                  219 ERROR    Mising GPS position for stop: Troita Unirii
brasov.py                  219 ERROR    Mising GPS position for stop: Troita Morii
brasov.py                  219 ERROR    Mising GPS position for stop: Piateta Stefan Cel Mare
brasov.py                  219 ERROR    Mising GPS position for stop: Codlea Nord
brasov.py                  219 ERROR    Mising GPS position for stop: Electrica
brasov.py                  219 ERROR    Mising GPS position for stop: Muzeu
brasov.py                  219 ERROR    Mising GPS position for stop: Colorom
brasov.py                  219 ERROR    Mising GPS position for stop: Stadion
brasov.py                  219 ERROR    Mising GPS position for stop: Centrul Istoric
brasov.py                  219 ERROR    Mising GPS position for stop: Rotbav
brasov.py                  219 ERROR    Mising GPS position for stop: Reconstructia
brasov.py                  219 ERROR    Mising GPS position for stop: Troita
brasov.py                  219 ERROR    Mising GPS position for stop: Agromec
brasov.py                  219 ERROR    Mising GPS position for stop: Cetate
brasov.py                  219 ERROR    Mising GPS position for stop: Bod Colonie
brasov.py                  219 ERROR    Mising GPS position for stop: Statia Radio
brasov.py                  219 ERROR    Mising GPS position for stop: Lalelelor
brasov.py                  219 ERROR    Mising GPS position for stop: Garii Bod
brasov.py                  219 ERROR    Mising GPS position for stop: Avram Iancu
brasov.py                  219 ERROR    Mising GPS position for stop: Primaria Bod
brasov.py                  219 ERROR    Mising GPS position for stop: Brasovului
brasov.py                  219 ERROR    Mising GPS position for stop: Matei Basarab
brasov.py                  219 ERROR    Mising GPS position for stop: Voievozi
brasov.py                  219 ERROR    Mising GPS position for stop: Spital Maria
brasov.py                  219 ERROR    Mising GPS position for stop: Morii Sanpetru
brasov.py                  219 ERROR    Mising GPS position for stop: Rahovei
brasov.py                  219 ERROR    Mising GPS position for stop: Centru Sanpetru
brasov.py                  219 ERROR    Mising GPS position for stop: Biserica Ortodoxa
brasov.py                  219 ERROR    Mising GPS position for stop: Cartier
brasov.py                  219 ERROR    Mising GPS position for stop: Triajului
brasov.py                  219 ERROR    Mising GPS position for stop: Sfantul Andrei
brasov.py                  219 ERROR    Mising GPS position for stop: Sc. Gimn. Lunca C.
brasov.py                  219 ERROR    Mising GPS position for stop: Gradinita
brasov.py                  219 ERROR    Mising GPS position for stop: Targ
brasov.py                  219 ERROR    Mising GPS position for stop: Pista Carting
brasov.py                  219 ERROR    Mising GPS position for stop: Gara Mare
brasov.py                  219 ERROR    Mising GPS position for stop: Izvorul Cucu
brasov.py                  219 ERROR    Mising GPS position for stop: Grindul Morii Mare
brasov.py                  219 ERROR    Mising GPS position for stop: Biserica Fortificata
brasov.py                  219 ERROR    Mising GPS position for stop: Colegiul Tara Barsei
brasov.py                  219 ERROR    Mising GPS position for stop: Ing. I. Toma
brasov.py                  219 ERROR    Mising GPS position for stop: Parc Industrial
brasov.py                  219 ERROR    Mising GPS position for stop: Harman
brasov.py                  219 ERROR    Mising GPS position for stop: Monumentul Eroilor 2
brasov.py                  219 ERROR    Mising GPS position for stop: Biserica Sfintii Trei Ierarhi
brasov.py                  219 ERROR    Mising GPS position for stop: Tineretului
brasov.py                  219 ERROR    Mising GPS position for stop: Parcul Eroilor
brasov.py                  219 ERROR    Mising GPS position for stop: Laterala
brasov.py                  219 ERROR    Mising GPS position for stop: Cantar Vulcanului
brasov.py                  219 ERROR    Mising GPS position for stop: Bisericuta de Lemn

"""
