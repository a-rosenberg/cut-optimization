from cutoptimizer import Packer


def main():
    """Van side polyiso insulation optimization

    Returns:
        None
    """


    rectangles = [
        {'width': 46.5, 'height': 9, 'rid': 'R1'},
        {'width': 47.25, 'height': 23.5, 'rid': 'R2'},
        {'width': 18.25, 'height': 10.5, 'rid': 'R3'},
        {'width': 25.5, 'height': 10.5, 'rid': 'R4'},
        {'width': 24.75, 'height': 10.5, 'rid': 'R5'},
        {'width': 19.25, 'height': 24.75, 'rid': 'R6'},
        {'width': 26.5, 'height': 24.75, 'rid': 'R7'},
        {'width': 24.5, 'height': 24.75, 'rid': 'R8'},
        {'width': 24.75, 'height': 10.5, 'rid': 'L1'},
        {'width': 25.5, 'height': 10.5, 'rid': 'L2'},
        {'width': 18.25, 'height': 10.5, 'rid': 'L3'},
        {'width': 25.5, 'height': 10.5, 'rid': 'L4'},
        {'width': 25, 'height': 10.5, 'rid': 'L5'},
        {'width': 24.5, 'height': 24.75, 'rid': 'L6'},
        {'width': 26.5, 'height': 24.75, 'rid': 'L7'},
        {'width': 19.25, 'height': 24.75, 'rid': 'L8'}
    ]

    bins = [
        {'width': 48, 'height': 96},
        {'width': 48, 'height': 96},
        {'width': 48, 'height': 96},
    ]

    van_packer = Packer()

    [van_packer.add_rect(**x) for x in rectangles]
    [van_packer.add_bin(**x) for x in bins]

    van_packer.pack()
    print(van_packer.cut_list())

    van_packer.save_boards(figure_folder='boards/van')


if __name__ == '__main__':
    main()