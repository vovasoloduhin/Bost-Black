import pygame

from settings import *

class Renderer:
    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont("arial", 32)

        self.combo_font = pygame.font.SysFont("arial", 42)

        self.big_font = pygame.font.SysFont(
            "arial",
            72,
            bold=True
        )

    def draw(self, game):
        self.screen.fill(BACKGROUND_COLOR)

        self.draw_board(game)

        self.draw_score(game)

        self.draw_best_score(game)

        self.draw_combo(game)

        self.draw_pieces(game)

        self.draw_dragging_piece(game)

        self.draw_restart_button(game)

        if game.game_over:
            self.draw_game_over(game)

        if game.restart_fade > 0:
            self.draw_restart_fade(game)

    def draw_board(self, game):
        board = game.board

        pulse = 0

        if game.clear_animation_timer > 0:
            pulse = game.clear_animation_timer * 2

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * CELL_SIZE,
                    BOARD_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    self.screen,
                    GRID_COLOR,
                    rect,
                    2,
                    border_radius=6
                )

                if board.grid[y][x]:
                    inner = rect.inflate(
                        -6 - pulse,
                        -6 - pulse
                    )

                    pygame.draw.rect(
                        self.screen,
                        BLOCK_COLOR,
                        inner,
                        border_radius=10
                    )

    def draw_piece(self, piece, px, py):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):

                if not cell:
                    continue

                rect = pygame.Rect(
                    px + x * CELL_SIZE,
                    py + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                inner = rect.inflate(-6, -6)

                pygame.draw.rect(
                    self.screen,
                    PREVIEW_COLOR,
                    inner,
                    border_radius=10
                )

    def draw_pieces(self, game):
        for piece in game.pieces:
            if piece.selected:
                continue

            self.draw_piece(
                piece,
                piece.preview_x,
                piece.preview_y
            )

    def draw_dragging_piece(self, game):
        if not game.selected_piece:
            return

        piece = game.selected_piece

        offset_x = (
            piece.width * CELL_SIZE
        ) // 2

        offset_y = (
            piece.height * CELL_SIZE
        ) // 2

        px = game.mouse_x - offset_x
        py = game.mouse_y - offset_y

        self.draw_piece(piece, px, py)

    def draw_score(self, game):
        text = self.font.render(
            f"Score: {game.score_manager.score}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (20, 20))

    def draw_best_score(self, game):
        text = self.font.render(
            f"Best: {game.score_manager.best_score}",
            True,
            (255, 220, 80)
        )

        self.screen.blit(text, (20, 60))

    def draw_combo(self, game):
        if game.combo <= 1:
            return

        scale = 1 + (
            game.combo_timer / 180
        ) * 0.2

        text = self.combo_font.render(
            f"COMBO x{game.combo}",
            True,
            (255, 180, 50)
        )

        size = text.get_size()

        scaled = pygame.transform.scale(
            text,
            (
                int(size[0] * scale),
                int(size[1] * scale)
            )
        )

        self.screen.blit(scaled, (20, 110))

    def draw_restart_button(self, game):
        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            game.restart_button,
            border_radius=10
        )

        text = self.font.render(
            "Restart",
            True,
            (255, 255, 255)
        )

        rect = text.get_rect(
            center=game.restart_button.center
        )

        self.screen.blit(text, rect)

    def draw_game_over(self, game):
        alpha = min(
            255,
            game.game_over_anim * 2
        )

        scale = 1 + (
            game.game_over_anim / 120
        ) * 0.25

        text = self.big_font.render(
            "GAME OVER",
            True,
            (255, 70, 70)
        )

        size = text.get_size()

        scaled = pygame.transform.scale(
            text,
            (
                int(size[0] * scale),
                int(size[1] * scale)
            )
        )

        scaled.set_alpha(alpha)

        rect = scaled.get_rect(
            center=(400, 300)
        )

        self.screen.blit(scaled, rect)

    def draw_restart_fade(self, game):
        alpha = int(
            (game.restart_fade / 30) * 255
        )

        overlay = pygame.Surface(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT
            )
        )

        overlay.set_alpha(alpha)

        overlay.fill((255, 255, 255))

        self.screen.blit(overlay, (0, 0))