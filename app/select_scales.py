def get_scales(instrument, grade):
    """
    :param instrument: string
    :param grade: string '1'-'8'
    :return: list of scales
    """
    if instrument == 'violin':
        if grade == '4':
            scales = ['Ab major scale, 2 octaves', 'B major scale, 2 octaves', 'C major scale, 2 octaves',
                      'E major scale, 2 octaves', 'G minor scale, 2 octaves', 'B minor scale, 2 octaves', 'C minor scale, 2 octaves',
                      'Ab major arpeggio, 2 octaves', 'B major arpeggio, 2 octaves', 'C major arpeggio, 2 octaves',
                      'E major arpeggio, 2 octaves', 'G minor arpeggio, 2 octaves', 'B minor arpeggio, 2 octaves',
                      'C minor arpeggio, 2 octaves', 'Dominant seventh in the key of C, 1 octave',
                      'Dominant seventh in the key of D, 1 octave', 'Chromatic scale starting on A, 1 octave',
                      'Chromatic scale starting on E, 1 octave']
        elif grade == '5':
            scales = ['Db major', 'Eb major', 'F major', 'B minor', 'C# minor', 'E minor']
    elif instrument == 'piano':
        if grade == '4':
            scales = ['test1', 'test2', 'cowboy']
        elif grade == '5':
            scales = ['test1', 'test2', 'alien']
    return scales
