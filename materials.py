#!/usr/bin/env python

import os

import rectpack

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Packer(rectpack.PackerBBF):
    """rectpack packer wrapper to add user methods and views

    Attributes:
        rect_map (dict): Mapping of rectangle cuts which is
            populated with pack run method.
    """
    def __init__(self):
        super().__init__()
        self.rect_map = None


    def pack(self):
        """Pack override

        Runs parent pack method then generates rectangle cut
        mapping.

        Returns:
            None

        """
        super().pack()

        self.rect_map = {}
        for rect in self.rect_list():
            self.rect_map[rect[5]] = {
                'board': rect[0],
                'x': rect[1],
                'y': rect[2],
                'width': rect[3],
                'height': rect[4]
            }

    def get_rect(self, id):
        """Getter for rect information

        Args:
            id (str): Identification for cut rectangle;
                declared with add_rect method.

        Returns:
            Dictionary of rectangle information including
                bin, start width, start height, total width,
                and total height.

        Raises:
            EnvironmentError: If the pack method hasn't been run.
        """
        if not self.rect_map:
            raise EnvironmentError('Packer has not yet been packed; '
                                   'try self.pack() first')
        return self.rect_map[id]

    def cut_list(self):
        """Human readable cut list to work from

        Returns:
            instructions (str): Cut list as plain text.

        Raises:
            EnvironmentError: If the pack method hasn't been run.
        """
        if not self.rect_map:
            raise EnvironmentError('Packer has not yet been packed; '
                                   'try self.pack() first')

        instructions = ['-'*50, ' Cut List '.center(50, '-'), '-'*50, '']
        for id, result in self.rect_map.items():
            instructions.append(id)
            instructions.append('-'*50)
            instructions.append('\tboard:\t\t\t%s' % str(result['board'] + 1))
            instructions.append('\tstart-width:\t%s' % str(result['x']))
            instructions.append('\tstart-height:\t%s' % str(result['y']))
            instructions.append('')

        return '\n'.join(instructions)

    def _save_board(self, board_number, figure_path):
        """Internal method for generating board figure

        Args:
            board_number (int): Index for board to visualize.
            figure_path (str): System path for figure output.
                Should end in .png.

        Returns:
            None
        """
        bid = board_number - 1
        board = self[bid]
        x = board.width
        y = board.height

        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')

        ax.set_xlim(0, x)
        ax.set_ylim(0, y)

        ax.grid()

        for rect in board:
            ax.add_patch(
                patches.Rectangle(
                    (rect.x, rect.y),  # (x,y)
                    rect.width,  # width
                    rect.height,  # height
                    edgecolor='black'
                )
            )

        fig.savefig(figure_path, dpi=90, bbox_inches='tight')

    def save_boards(self, figure_folder):
        board_number = 1
        while True:
            figure_path = os.path.join(figure_folder,
                                       'board_%s.png' % board_number)
            try:
                self._save_board(board_number=board_number,
                                 figure_path=figure_path)
            except IndexError as e:
                break

            board_number += 1


def pack_test():
    rectangles = [
        {'width': 24, 'height': 38, 'rid': 'R1'},
        {'width': 12, 'height': 38, 'rid': 'R2'},
        {'width': 24, 'height': 38, 'rid': 'R3'},
        {'width': 24, 'height': 38, 'rid': 'R4'},
        {'width': 44, 'height': 13, 'rid': 'L1'},
        {'width': 24, 'height': 38, 'rid': 'L3'},
        {'width': 24, 'height': 78, 'rid': 'C1'}
    ]
    bins = [
        {'width': 48, 'height': 96},
        {'width': 48, 'height': 96},
        {'width': 48, 'height': 96}
    ]

    packer = Packer()

    [packer.add_rect(**x) for x in rectangles]
    [packer.add_bin(**x) for x in bins]

    packer.pack()
    print(packer.cut_list())

    packer.save_boards(figure_folder='boards')


if __name__ == '__main__':
    pack_test()
