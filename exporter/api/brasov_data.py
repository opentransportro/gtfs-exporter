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
    {"label": "Triaj", "latitude": 45.675_677_1, "longitude": 25.647_312_1},
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
    {"label": "Huniade", "latitude": 45.666_561, "longitude": 25.588_858_9},
    {"label": "Vlahuta", "latitude": 45.657_715_2, "longitude": 25.622_170_5},
    {"label": "Carierei*", "latitude": 45.658_088_2, "longitude": 25.580_633_1},
    {"label": "Liceul Mesota", "latitude": 45.653_912, "longitude": 25.609_261_6},
    {"label": "Fragilor", "latitude": 45.633_068, "longitude": 25.605_555_5},
    {"label": "Tractorul", "latitude": 45.664_776, "longitude": 25.608_927},
    {"label": "Camera de Comert", "latitude": 45.651_061_9, "longitude": 25.608_276_1},
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
    {"label": "Primarie", "latitude": 45.646_530_3, "longitude": 25.596_260_7},
    {"label": "1 Decembrie 1918", "latitude": 45.666_568_2, "longitude": 25.598_536_1},
    {"label": "RAT Brasov", "latitude": 45.669_643, "longitude": 25.636_790_3},
    {"label": "Lanurilor", "latitude": 45.662_347, "longitude": 25.567_782_1},
    {"label": "CEC", "latitude": 45.654_601, "longitude": 25.615_245},
    {"label": "Autogara 3", "latitude": 45.663_395, "longitude": 25.629_060_1},
    {"label": "Universitate", "latitude": 45.655_924, "longitude": 25.600_044},
    {"label": "Memorandului", "latitude": 45.654_966_2, "longitude": 25.583_075_5},
    {"label": "Zlatna", "latitude": 45.666_772, "longitude": 25.574_782},
    {"label": "Egretei", "latitude": 45.664_233_8, "longitude": 25.565_329_1},
    {"label": "Astra", "latitude": 45.647_333_3, "longitude": 25.589_327_8},
    {"label": "Fartec", "latitude": 45.666_141, "longitude": 25.589_035_9},
    {"label": "Marasesti", "latitude": 45.648_621_7, "longitude": 25.605_305_8},
    {"label": "Muncii", "latitude": 45.639_933_9, "longitude": 25.611_260_5},
    {"label": "Sc. Gen. 20", "latitude": 45.637_925, "longitude": 25.609_383},
    {"label": "Liceul Tractorul", "latitude": 45.668_581_3, "longitude": 25.610_155_5},
    {"label": "Mircea cel Batran", "latitude": 45.656_958_5, "longitude": 25.606_358_2},
    {"label": "Caprioara", "latitude": 45.659_648_1, "longitude": 25.614_844_1},
    {"label": "F-ca de Var", "latitude": 45.643_260_9, "longitude": 25.624_210_5},
    {"label": "13 Decembrie", "latitude": 45.654_020_4, "longitude": 25.605_366_2},
    {"label": "Coresi 2", "latitude": 45.66986, "longitude": 25.621_812_1},
    {"label": "Saturn", "latitude": 45.634_544_3, "longitude": 25.63548},
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
    {"label": "Bd. Garii", "latitude": 45.660_814, "longitude": 25.613_418},
    {"label": "Energo", "latitude": 45.653_483, "longitude": 25.653_081},
    {"label": "IUS", "latitude": 45.656_460_7, "longitude": 25.618_341},
    {"label": "Piata Decebal", "latitude": 45.644_048, "longitude": 25.618_207},
    {"label": "Statie Epurare", "latitude": 45.680_881_7, "longitude": 25.572_957_4},
    {"label": "Gemenii", "latitude": 45.649_448, "longitude": 25.628_506},
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
    {"label": "Bronzului", "latitude": 45.668_338, "longitude": 25.597_115},
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
    {"label": "Cernatului", "latitude": 45.649_056, "longitude": 25.651_757},
    {"label": "Complexul Mare", "latitude": 45.643_849_5, "longitude": 25.632_664_6},
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
    {"label": "Roman", "latitude": 45.632_837, "longitude": 25.632_512_9},
    {"label": "Spital Marzescu", "latitude": 45.647_288, "longitude": 25.619_313},
    {"label": "Lujerului", "latitude": 45.714_390, "longitude": 25.551_206},
    {"label": "Branduselor", "latitude": 45.653_625_7, "longitude": 25.624_103},
    {"label": "Baumax", "latitude": 45.673_229, "longitude": 25.589_765},
    {"label": "Stupini Izvorului", "latitude": 45.702_300, "longitude": 25.555_653},
    {"label": "Toamnei(CEC)", "latitude": 45.652_549_6, "longitude": 25.615_627_1},
    {"label": "Brintex", "latitude": 45.657_113, "longitude": 25.559_274},
    {"label": "Invatatorilor", "latitude": 45.627_904, "longitude": 25.56805},
    {"label": "Warte", "latitude": 45.646_103_3, "longitude": 25.577_040_9},
    {"label": "Traian", "latitude": 45.650_123_4, "longitude": 25.623_203_1},
    {"label": "Elmas", "latitude": 45.687_528, "longitude": 25.582_899},
    {"label": "Independentei", "latitude": 45.666_494_2, "longitude": 25.595_760_4},
    {"label": "Dimitrie Anghel", "latitude": 45.669_005, "longitude": 25.576_226},
    {"label": "Unitate Militara", "latitude": 45.676_307, "longitude": 25.58041},
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
    {"label": "Fagurului", "latitude": 45.705_325, "longitude": 25.572_040_9},
    {"label": "Rial", "latitude": 45.651_496, "longitude": 25.595_527},
    {"label": "Spital Tractorul", "latitude": 45.665_863, "longitude": 25.608_702_1},
    {"label": "Timis Triaj", "latitude": 45.666_898, "longitude": 25.649_428},
    {"label": "Albinelor", "latitude": 45.687_453, "longitude": 25.545_552_1},
    {"label": "Depozite ILF", "latitude": 45.65838, "longitude": 25.563_361_9},
    {"label": "Craiter", "latitude": 45.656_910_3, "longitude": 25.633_522_9},
    {"label": "Junilor", "latitude": 45.629_773, "longitude": 25.57128},
    {"label": "Pompieri", "latitude": 45.637_155, "longitude": 25.622_295},
    {"label": "Ioan Clopotel", "latitude": 45.652_126, "longitude": 25.542_612},
    {"label": "Bellevue Residence", "latitude": 45.645_213_5, "longitude": 25.580_207},
    {"label": "Bariera Bartolomeu", "latitude": 45.664_274, "longitude": 25.577_953},
    {"label": "Romradiatoare", "latitude": 45.649_077_1, "longitude": 25.644_548_1},
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
    {"label": "Biserica Neagra", "latitude": 45.640_391_4, "longitude": 25.585_655_3},
    {"label": "Liceul Saguna", "latitude": 45.653_912, "longitude": 25.609_261_6},
    {"label": "Silver Mountain", "latitude": 45.604_879, "longitude": 25.54359},
    {"label": "Solomon", "latitude": 45.617_525_1, "longitude": 25.558_469_3},
    {
        "label": "Complex Bartolomeu",
        "latitude": 45.663_584_9,
        "longitude": 25.578_841_7,
    },
    {"label": "Magurele", "latitude": 45.636_127, "longitude": 25.523_686},
    {"label": "Merilor", "latitude": 45.690_475_6, "longitude": 25.566_191_3},
    {"label": "La Moara", "latitude": 45.657_975_5, "longitude": 25.601_197_7},
    {"label": "Sala Sporturilor", "latitude": 45.659_045_7, "longitude": 25.620_821_3},
    {"label": "Metro", "latitude": 45.622_209, "longitude": 25.646_676},
    {"label": "Pensiunea Stupina", "latitude": 45.686_708, "longitude": 25.569_921},
    {"label": "Sc. Gen. 4", "latitude": 45.637_661, "longitude": 25.612_853_8},
    {"label": "Conforest", "latitude": 45.671_379_5, "longitude": 25.578_973_5},
    {"label": "Int. Ceferistilor", "latitude": 45.656_595, "longitude": 25.631_522},
    {"label": "Tocile", "latitude": 45.633_124_2, "longitude": 25.576_456_2},
    {"label": "Scriitorilor", "latitude": 45.650_505_5, "longitude": 25.620_652_3},
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
    {"label": "Oligopol", "latitude": 45.682_349, "longitude": 25.581_729},
    {"label": "Panselelor", "latitude": 45.627_529, "longitude": 25.622_478},
    {"label": "Fantanii", "latitude": 45.708_144_4, "longitude": 25.577_247_1},
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
    {"label": "Dulgherului", "latitude": 45.656_958_5, "longitude": 25.606_358_2},
    {"label": "Mol", "latitude": 45.68437, "longitude": 25.58274},
    {"label": "Eroilor", "latitude": 45.645_514_5, "longitude": 25.588_325},
    {"label": "Opera Brasov", "latitude": 45.654_611_1, "longitude": 25.589_884_9},
    {"label": "Prunului", "latitude": 45.656_958_5, "longitude": 25.606_358_2},
    {"label": "Agetaps", "latitude": 45.688_705_9, "longitude": 25.581_594_2},
    {"label": "Balcescu", "latitude": 45.641_619_8, "longitude": 25.592_560_3},
    {"label": "Str. Izvorului", "latitude": 45.702_300, "longitude": 25.555_653},
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
    {"label": "Scoala", "latitude": 45.637_661, "longitude": 25.612_853_8},
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
    # added from https://www.google.com/maps/d/viewer?mid=18QDJjDFhFUJim323TpkxtlmAA0v5d0wO&ll=45.658605699999995%2C25.508909899999985&z=14
    {
        "latitude": 45.659_753_700,
        "longitude": 25.570_026_900,
        "label": "STAD. MUNICIPAL",
    },
    {"latitude": 45.632_449_300, "longitude": 25.491_054_700, "label": "OITUZ"},
    {"latitude": 45.632_546_800, "longitude": 25.491_483_900, "label": "OITUZ"},
    {
        "latitude": 45.625_090_900,
        "longitude": 25.479_942_600,
        "label": "PARCUL EROILOR",
    },
    {"latitude": 45.625_509_700, "longitude": 25.475_439_900, "label": "LATERALĂ"},
    {
        "latitude": 45.625_724_600,
        "longitude": 25.472_698_400,
        "label": "CANTAR VULCANULUI",
    },
    {
        "latitude": 45.620_621_200,
        "longitude": 25.468_187_900,
        "label": "BISERICUTA DE LEMN",
    },
    {"latitude": 45.617_237_900, "longitude": 25.470_811_100, "label": "TINERETULUI"},
    {
        "latitude": 45.659_781_000,
        "longitude": 25.570_041_100,
        "label": "STAD. MUNICIPAL",
    },
    {"latitude": 45.659_561_700, "longitude": 25.566_744_700, "label": "SERVICE"},
    {"latitude": 45.658_507_900, "longitude": 25.563_204_100, "label": "CARAMIDARIEI"},
    {
        "latitude": 45.648_395_900,
        "longitude": 25.530_778_400,
        "label": "FACULTATIVA MTI",
    },
    {"latitude": 45.636_523_100, "longitude": 25.498_967_100, "label": "COS 2000"},
    {
        "latitude": 45.629_770_100,
        "longitude": 25.486_547_200,
        "label": "SCOALA CRISTIAN",
    },
    {
        "latitude": 45.624_396_700,
        "longitude": 25.481_330_300,
        "label": "CENTRU CRISTIAN",
    },
    {
        "latitude": 45.616_373_800,
        "longitude": 25.475_623_900,
        "label": "UNITATE MILITARA",
    },
    {"latitude": 45.599_148_500, "longitude": 25.464_732_900, "label": "LUKOIL RASNOV"},
    {"latitude": 45.593_246_000, "longitude": 25.460_693_300, "label": "REPUBLICII"},
    {"latitude": 45.592_516_800, "longitude": 25.462_269_100, "label": "FLORILOR"},
    {"latitude": 45.590_258_600, "longitude": 25.463_344_000, "label": "MIHAI VITEAZU"},
    {
        "latitude": 45.587_730_200,
        "longitude": 25.462_243_900,
        "label": "PRIMARIA VECHE",
    },
    {
        "latitude": 45.583_854_100,
        "longitude": 25.461_386_300,
        "label": "BISERICA RASNOV",
    },
    {
        "latitude": 45.580_657_100,
        "longitude": 25.460_236_200,
        "label": "I.L. CARAGIALE",
    },
    {
        "latitude": 45.577_520_500,
        "longitude": 25.457_020_900,
        "label": "RASNOV CAP LINIE",
    },
    {
        "latitude": 45.580_320_800,
        "longitude": 25.460_297_900,
        "label": "I.L. CARAGIALE",
    },
    {
        "latitude": 45.583_538_300,
        "longitude": 25.461_355_400,
        "label": "BISERICA RASNOV",
    },
    {
        "latitude": 45.588_177_000,
        "longitude": 25.462_942_300,
        "label": "PRIMARIA VECHE",
    },
    {"latitude": 45.590_630_300, "longitude": 25.462_708_700, "label": "MIHAI VITEAZU"},
    {"latitude": 45.589_788_700, "longitude": 25.455_610_400, "label": "F.S.R."},
    {
        "latitude": 45.593_473_600,
        "longitude": 25.459_758_900,
        "label": "LICEUL TEHNOLOGIC",
    },
    {"latitude": 45.599_537_900, "longitude": 25.465_313_300, "label": "LUKOIL RASNOV"},
    {
        "latitude": 45.616_475_700,
        "longitude": 25.475_850_100,
        "label": "UNITATE MILITARA",
    },
    {
        "latitude": 45.624_839_400,
        "longitude": 25.481_958_400,
        "label": "CENTRU CRISTIAN",
    },
    {"latitude": 45.630_772_900, "longitude": 25.488_721_800, "label": "EROILOR"},
    {
        "latitude": 45.656_273_700,
        "longitude": 25.556_563_600,
        "label": "DEPOZITE  I.L.F.",
    },
    {"latitude": 45.657_098_600, "longitude": 25.559_288_700, "label": "BRINTEX"},
    {"latitude": 45.658_309_700, "longitude": 25.563_312_000, "label": "CARAMIDARIEI"},
    {"latitude": 45.660_886_200, "longitude": 25.550_752_100, "label": "HORNBACH"},
    {
        "latitude": 45.663_150_000,
        "longitude": 25.518_654_100,
        "label": "METRO Linia 220 (Codlea nu opreste",
    },
    {
        "latitude": 45.665_552_400,
        "longitude": 25.512_408_300,
        "label": "DIAMANT Linia 220 (Codlea) nu oprest",
    },
    {
        "latitude": 45.667_559_900,
        "longitude": 25.507_916_900,
        "label": "FAGARASULUI	Opresc liniile 210 si 22",
    },
    {
        "latitude": 45.668_408_600,
        "longitude": 25.505_081_400,
        "label": "TROITA FAGARASULUI	Linia 220 (Codlea) nu oprest",
    },
    {
        "latitude": 45.667_064_800,
        "longitude": 25.508_590_100,
        "label": "FAGARASULUI	Opresc liniile 210 si 22",
    },
    {"latitude": 45.663_197_800, "longitude": 25.506_769_800, "label": "MORII"},
    {"latitude": 45.661_006_700, "longitude": 25.501_670_800, "label": "TROITA MORII"},
    {
        "latitude": 45.657_506_600,
        "longitude": 25.501_868_100,
        "label": "STEFAN CEL MARE",
    },
    {
        "latitude": 45.654_872_200,
        "longitude": 25.503_481_400,
        "label": "GHIMBAV CAP LINIE",
    },
    {"latitude": 45.658_605_700, "longitude": 25.508_909_900, "label": "CRIZANTEMEI"},
    {"latitude": 45.661_291_100, "longitude": 25.513_058_800, "label": "GENTIANEI"},
    {"latitude": 45.662_715_800, "longitude": 25.514_249_700, "label": "TESS"},
    {"latitude": 45.688_792_600, "longitude": 25.452_944_900, "label": "COLOROM"},
    {"latitude": 45.691_513_700, "longitude": 25.448_578_600, "label": "STADION"},
    {
        "latitude": 45.699_030_500,
        "longitude": 25.446_612_700,
        "label": "CENTRUL ISTORIC",
    },
    {
        "latitude": 45.702_228_200,
        "longitude": 25.448_935_600,
        "label": "ELECTRICA CODLEA",
    },
    {"latitude": 45.706_730_300, "longitude": 25.452_613_600, "label": "CODLEA NORD"},
    {
        "latitude": 45.702_146_800,
        "longitude": 25.448_673_300,
        "label": "ELECTRICA CDLEA",
    },
    {
        "latitude": 45.699_179_700,
        "longitude": 25.446_570_000,
        "label": "CENTRU ISTORIC",
    },
    {
        "latitude": 45.692_161_700,
        "longitude": 25.447_957_700,
        "label": "PRIMARIA CODLEA",
    },
    {"latitude": 45.688_617_900, "longitude": 25.452_989_600, "label": "COLOROM"},
    {"latitude": 45.808_383_600, "longitude": 25.593_497_800, "label": "AGROMEC"},
    {"latitude": 45.808_981_900, "longitude": 25.593_052_500, "label": "AGROMEC"},
    {
        "latitude": 45.817_318_300,
        "longitude": 25.589_579_500,
        "label": "TROITA	Linia 310 opreste pe ambele sensuri de deplasar",
    },
    {
        "latitude": 45.820_083_100,
        "longitude": 25.600_805_700,
        "label": "CETATEA FELDIOAREI",
    },
    {
        "latitude": 45.818_924_600,
        "longitude": 25.593_543_300,
        "label": "CENTRU FELDIOARA",
    },
    {"latitude": 45.825_994_900, "longitude": 25.570_280_600, "label": "RECONSTRUCTIA"},
    {"latitude": 45.825_522_000, "longitude": 25.570_693_600, "label": "RECONSTRUCTIA"},
    {"latitude": 45.837_407_400, "longitude": 25.557_326_600, "label": "ROTBAV"},
    {"latitude": 45.660_795_900, "longitude": 25.594_769_200, "label": "PLEVNEI"},
    {"latitude": 45.679_057_700, "longitude": 25.586_948_300, "label": "DEDEMAN"},
    {"latitude": 45.676_423_000, "longitude": 25.588_214_300, "label": "METABRAS"},
    {"latitude": 45.690_093_400, "longitude": 25.583_478_200, "label": "PIATA AGRO"},
    {"latitude": 45.689_216_500, "longitude": 25.582_866_700, "label": "AGETAPS"},
    {
        "latitude": 45.659_933_900,
        "longitude": 25.570_017_500,
        "label": "STAD. MUNICIPAL",
    },
    {"latitude": 45.682_164_200, "longitude": 25.615_014_000, "label": "RULMENTUL"},
    {
        "latitude": 45.693_321_000,
        "longitude": 25.622_897_800,
        "label": "SFANTUL ANDREI",
    },
    {
        "latitude": 45.693_485_800,
        "longitude": 25.623_225_000,
        "label": "SFANTUL ANDREI",
    },
    {"latitude": 45.697_099_100, "longitude": 25.625_479_000, "label": "TRIAJULUI"},
    {"latitude": 45.697_387_600, "longitude": 25.625_961_800, "label": "TRIAJULUI"},
    {"latitude": 45.703_204_200, "longitude": 25.630_495_900, "label": "CARTIER"},
    {"latitude": 45.704_016_500, "longitude": 25.630_876_200, "label": "CARTIER"},
    {
        "latitude": 45.708_472_500,
        "longitude": 25.633_805_700,
        "label": "BISERICA ORTODOXA",
    },
    {
        "latitude": 45.708_135_300,
        "longitude": 25.633_435_600,
        "label": "BISERICA ORTODOXA",
    },
    {"latitude": 45.711_951_900, "longitude": 25.633_602_900, "label": "CENTRU"},
    {"latitude": 45.712_172_900, "longitude": 25.633_645_800, "label": "CENTRU"},
    {"latitude": 45.716_178_700, "longitude": 25.629_513_300, "label": "RAHOVEI"},
    {"latitude": 45.715_254_200, "longitude": 25.630_242_500, "label": "RAHOVEI"},
    {"latitude": 45.717_013_000, "longitude": 25.627_156_500, "label": "MORII"},
    {"latitude": 45.728_608_600, "longitude": 25.627_973_400, "label": "SPITAL MARIA"},
    {"latitude": 45.728_762_100, "longitude": 25.628_142_400, "label": "SPITAL MARIA"},
    {"latitude": 45.740_733_600, "longitude": 25.631_797_400, "label": "VOIEVOZI"},
    {"latitude": 45.740_355_500, "longitude": 25.631_872_500, "label": "VOIEVOZI"},
    {"latitude": 45.757_320_600, "longitude": 25.638_769_300, "label": "BRASOVULUI"},
    {"latitude": 45.757_586_300, "longitude": 25.639_064_400, "label": "BRASOVULUI"},
    {"latitude": 45.763_827_100, "longitude": 25.640_046_300, "label": "PRIMARIE BOD"},
    {"latitude": 45.763_587_100, "longitude": 25.626_602_000, "label": "GARII BOD"},
    {"latitude": 45.763_557_200, "longitude": 25.626_965_500, "label": "GARII BOD"},
    {"latitude": 45.758_708_700, "longitude": 25.608_266_900, "label": "STATIA RADIO"},
    {"latitude": 45.758_715_300, "longitude": 25.608_515_000, "label": "STATIA RADIO"},
    {"latitude": 45.755_378_700, "longitude": 25.597_967_500, "label": "BOD COLONIE"},
    {"latitude": 45.675_683_100, "longitude": 25.647_750_300, "label": "TRIAJ"},
    {"latitude": 45.669_589_600, "longitude": 25.638_685_400, "label": "RAT BRASOV"},
    {"latitude": 45.701_071_200, "longitude": 25.690_920_100, "label": "HARMAN"},
    {"latitude": 45.700_829_600, "longitude": 25.690_029_600, "label": "HARMAN"},
    {
        "latitude": 45.715_274_600,
        "longitude": 25.737_515_600,
        "label": "PARC INDUSTRIAL PREJMER",
    },
    {
        "latitude": 45.715_207_200,
        "longitude": 25.737_075_700,
        "label": "PARC INDUSTRIAL PREJMER",
    },
    {"latitude": 45.717_046_300, "longitude": 25.757_403_100, "label": "ING. I. TOMA"},
    {"latitude": 45.716_892_700, "longitude": 25.757_140_200, "label": "ING. I. TOMA"},
    {
        "latitude": 45.718_591_200,
        "longitude": 25.766_112_000,
        "label": "COLEGIUL TARA BARSEI",
    },
    {
        "latitude": 45.718_802_700,
        "longitude": 25.766_551_900,
        "label": "COLEGIUL TARA BARSEI",
    },
    {
        "latitude": 45.719_908_000,
        "longitude": 25.772_716_300,
        "label": "MONUMENTUL EROILOR",
    },
    {
        "latitude": 45.720_614_200,
        "longitude": 25.773_068_900,
        "label": "BISERICA FORTIFICATA",
    },
    {
        "latitude": 45.722_366_700,
        "longitude": 25.774_575_400,
        "label": "PRIMARIA PREJMER",
    },
    {
        "latitude": 45.722_947_100,
        "longitude": 25.775_007_600,
        "label": "BISERICA SFINTII TREI IERARHI",
    },
    {"latitude": 45.727_967_000, "longitude": 25.778_467_100, "label": "GRINDUL MORII"},
    {"latitude": 45.727_752_900, "longitude": 25.778_237_900, "label": "GRINDUL MORII"},
    {
        "latitude": 45.735_807_500,
        "longitude": 25.779_570_600,
        "label": "FACULTATIVA IZVORUL CUCU",
    },
    {
        "latitude": 45.735_710_100,
        "longitude": 25.779_377_500,
        "label": "FACULTATIVA IZVORUL CUCU",
    },
    {"latitude": 45.738_312_500, "longitude": 25.779_436_400, "label": "GARA MARE"},
    {"latitude": 45.738_533_400, "longitude": 25.779_562_500, "label": "GARA MARE"},
    {"latitude": 45.741_733_900, "longitude": 25.780_837_400, "label": "PISTA CARTING"},
    {"latitude": 45.742_070_900, "longitude": 25.780_735_500, "label": "PISTA CARTING"},
    {
        "latitude": 45.745_412_700,
        "longitude": 25.779_813_200,
        "label": "FACULTATIVA TARG",
    },
    {
        "latitude": 45.745_356_500,
        "longitude": 25.780_014_400,
        "label": "FACULTATIVA TARG",
    },
    {"latitude": 45.749_202_000, "longitude": 25.776_694_500, "label": "GRADINITA"},
    {"latitude": 45.749_140_200, "longitude": 25.776_517_400, "label": "GRADINITA"},
    {
        "latitude": 45.750_517_900,
        "longitude": 25.771_763_500,
        "label": "SCOALA GIMNAZIALA",
    },
    {
        "latitude": 45.750_504_800,
        "longitude": 25.771_420_200,
        "label": "SCOALA GIMNAZIALA",
    },
    {
        "latitude": 45.755_605_200,
        "longitude": 25.777_169_600,
        "label": "PICTOR A. BOANC",
    },
    {
        "latitude": 45.755_599_800,
        "longitude": 25.777_372_300,
        "label": "PICTOR A. BOANC",
    },
    {"latitude": 45.759_473_200, "longitude": 25.783_332_400, "label": "VIZAVIU"},
    {"latitude": 45.675_744_000, "longitude": 25.647_911_600, "label": "TRIAJ"},
    {"latitude": 45.669_589_500, "longitude": 25.638_644_300, "label": "RATBv"},
    {"latitude": 45.578_750_700, "longitude": 25.980_804_400, "label": "VAMA DE SUS"},
    {
        "latitude": 45.583_505_200,
        "longitude": 25.988_311_700,
        "label": "Pensiunea Alina",
    },
    {
        "latitude": 45.583_685_400,
        "longitude": 25.988_601_400,
        "label": "Pensiunea Alina",
    },
    {"latitude": 45.587_202_700, "longitude": 25.989_599_400, "label": "La Vlad"},
    {"latitude": 45.587_285_300, "longitude": 25.989_754_900, "label": "La Vlad"},
    {"latitude": 45.595_719_300, "longitude": 25.991_932_800, "label": "Primarie"},
    {"latitude": 45.595_888_200, "longitude": 25.992_158_100, "label": "Primarie"},
    {
        "latitude": 45.603_109_700,
        "longitude": 25.993_492_100,
        "label": "Complex Cultural",
    },
    {
        "latitude": 45.603_244_800,
        "longitude": 25.993_690_500,
        "label": "Complex Cultural",
    },
    {"latitude": 45.610_159_900, "longitude": 25.996_535_100, "label": "Gura Buzaiel"},
    {"latitude": 45.610_244_300, "longitude": 25.996_682_600, "label": "Gura Buzaiel"},
    {"latitude": 45.617_413_600, "longitude": 25.998_389_100, "label": "La Fabricuta"},
    {"latitude": 45.617_316_100, "longitude": 25.998_249_600, "label": "La Fabricuta"},
    {
        "latitude": 45.633_806_000,
        "longitude": 25.994_412_700,
        "label": "Rezervatia de zimbri",
    },
    {
        "latitude": 45.633_959_800,
        "longitude": 25.994_627_200,
        "label": "Rezervatia de zimbri",
    },
    {"latitude": 45.641_844_500, "longitude": 25.997_574_800, "label": "Acris"},
    {"latitude": 45.641_975_700, "longitude": 25.997_805_400, "label": "Acris"},
    {"latitude": 45.645_260_100, "longitude": 25.999_322_300, "label": "Acris Iesire"},
    {"latitude": 45.645_172_000, "longitude": 25.999_126_500, "label": "Acris Intrare"},
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

"""
Observatii / Exceptii de pe site: https://www.ratbv.ro/afisaje

3 - https://www.ratbv.ro/afisaje/3-dus.html
Nu circula SÂMBÃTÃ - DUMINICÃ

5 - https://www.ratbv.ro/afisaje/5m-dus.html
Orar separat sambata, duminica

9 - https://www.ratbv.ro/afisaje/9-dus.html
DUMINICA circula numai in intervalul 9:00 - 17:30.
Has partial/alternate trip when *

18 - https://www.ratbv.ro/afisaje/18-dus.html
Has partial/alternate trip when *

19 - https://www.ratbv.ro/afisaje/19-dus.html
Nu circula SÂMBÃTÃ - DUMINICÃ

22 - https://www.ratbv.ro/afisaje/22-dus.html
Some trips have accessibility features

23b - https://www.ratbv.ro/afisaje/23b-dus.html
Orar separat sambata, duminica

24 - https://www.ratbv.ro/afisaje/24-dus.html
Cursele marcate cu * circula si la Stupinii Noi.
Has partial/alternate trip when * or **

25 - https://www.ratbv.ro/afisaje/25-dus.html
Has partial/alternate trip when *

28 - https://www.ratbv.ro/afisaje/28-dus.html
Has partial/alternate trip when *

33 - https://www.ratbv.ro/afisaje/33-intors.html
Nu circula SÂMBÃTÃ - DUMINICÃ

35 - https://www.ratbv.ro/afisaje/35-intors.html
Some trips have accessibility features

50 - https://www.ratbv.ro/afisaje/50-dus.html
Has partial/alternate trip when *

52 - https://www.ratbv.ro/afisaje/52-dus.html
Has partial/alternate trip when *

53 - https://www.ratbv.ro/afisaje/53-intors.html
Nu circula DUMINICÃ

110 - https://www.ratbv.ro/afisaje/110-dus.html
Nu circula SÂMBÃTÃ - DUMINICÃ

220 - https://www.ratbv.ro/afisaje/220-dus.html
Orar separat sambata, duminica

310 - https://www.ratbv.ro/afisaje/310-dus.html
Orar separat sambata, duminica

"""
