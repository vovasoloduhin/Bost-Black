import pygame

from core.board import Board
from core.piece import Piece
from core.score import ScoreManager
from settings import *


class Game:
    def __init__(self):
        self.board = Board()

        self.score_manager = ScoreManager()

        self.pieces = self.generate_pieces()

        self.selected_piece = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.game_over = False

        self.combo = 0
        self.combo_timer = 0

        self.clear_animation_timer = 0

        self.restart_button = pygame.Rect(
            620,
            20,
            150,
            50
        )

        self.game_over_anim = 0

        self.restart_fade = 0

    def restart(self):

        self.restart_fade = 30

    def full_restart(self):

        best = self.score_manager.best_score

        self.__init__()

        self.score_manager.best_score = best

    def generate_pieces(self):

        pieces = [Piece(), Piece(), Piece()]

        start_x = 140

        for i, piece in enumerate(pieces):

            piece.preview_x = start_x + i * 200
            piece.preview_y = 620

        return pieces

    def update(self):
        if self.restart_fade > 0:
            self.restart_fade -= 1
            if self.restart_fade <= 0:
                self.full_restart()

            return

        if self.game_over:
            if self.game_over_anim < 120:
                self.game_over_anim += 4

            return

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0

        if self.clear_animation_timer > 0:
            self.clear_animation_timer -= 1

        if not self.board.has_moves(self.pieces):
            self.game_over = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if self.restart_button.collidepoint(mx, my):
                self.restart()
                return

            if self.game_over:
                return

            for piece in self.pieces:
                pw = piece.width * CELL_SIZE
                ph = piece.height * CELL_SIZE

                rect = pygame.Rect(
                    piece.preview_x,
                    piece.preview_y,
                    pw,
                    ph
                )

                if rect.collidepoint(mx, my):
                    self.selected_piece = piece
                    piece.selected = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_piece:
                self.try_place_piece()

                self.selected_piece.selected = False
                self.selected_piece = None

    def try_place_piece(self):
        piece = self.selected_piece

        offset_x = (piece.width * CELL_SIZE) // 2
        offset_y = (piece.height * CELL_SIZE) // 2

        gx = int(
            (
                self.mouse_x
                - offset_x
                - BOARD_OFFSET_X
                + CELL_SIZE / 2
            ) // CELL_SIZE
        )

        gy = int(
            (
                self.mouse_y
                - offset_y
                - BOARD_OFFSET_Y
                + CELL_SIZE / 2
            ) // CELL_SIZE
        )

        if self.board.can_place(piece, gx, gy):
            blocks, cleared = self.board.place_piece(
                piece,
                gx,
                gy
            )

            if cleared > 0:
                self.combo += 1
                self.combo_timer = 180
                combo_bonus = self.combo * 50

                gained = (
                    blocks * 5 +
                    cleared * 100 +
                    combo_bonus
                )

                self.clear_animation_timer = 20
            else:
                gained = blocks * 5

            self.score_manager.add(gained)

            self.pieces.remove(piece)

            if len(self.pieces) == 0:
                self.pieces = self.generate_pieces()