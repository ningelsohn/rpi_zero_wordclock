class De():

    def __init__(self):

        self.char_layout = 'eskistlfünfzehnzwanzigdreivierteltgnachvorjmhalbqZWÖLFpZWEINSIEBENkDREIrhFÜNFELFNEUNVIERwACHTZEHNrsbSECHSfmuhr'
        self.time_base = ['es', 'ist']
        self.numbers = [
            'ZWÖLF',
            'EINS',
            'ZWEI',
            'DREI',
            'VIER',
            'FÜNF',
            'SECHS', 
            'SIEBEN',
            'ACHT',
            'NEUN',
            'ZEHN',
            'ELF'
        ]
        self.steps = {
            0: ['uhr'],
            1: ['fünf', 'nach'],
            2: ['zehn', 'nach'],
            3: ['viertel', 'nach'],
            4: ['zwanzig', 'nach'], 
            5: ['fünf', 'vor', 'halb'],
            6: ['halb', ],
            7: ['fünf', 'nach', 'halb'],
            8: ['zwanzig', 'vor'], 
            9: ['viertel', 'vor'],
            10: ['zehn', 'vor'],
            11: ['fünf', 'vor']
        }