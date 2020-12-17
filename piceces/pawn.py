from .chesspiece import ChessPiece, Team


class Pawn(ChessPiece):
    pawn_moves = [(1, 0), (2, 0)]

    def __init__(self, image, position, team):
        super().__init__(image, position, team)
        self.was_moved = False
        self.direction = -1 if self.team == Team.WHITE else 1

    def move_to(self, new_position):
        self.was_moved = True
        super().move(new_position)

    def precalculated_moves(self):
        row, col = self.position
        precalculated_set = Pawn.pawn_moves if not self.was_moved else [Pawn.pawn_moves[0]]
        return [(row + d_row * self.direction, col + d_col) for (d_row, d_col) in precalculated_set]

