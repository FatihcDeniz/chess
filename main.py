import time
import numpy as np
import pygame
from pygame.locals import *

# Fix Some logics, pieces should not move when there is something in front of them
# Add time for both of the players ??

width = 820
height = 640
Dimension = 8
size = 80


class Board:
    def __init__(self, surface):
        self.surface = surface
        self.wp = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/pawn white.png")
        self.bp = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/pawn black.png")
        self.wr = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/rookw.png")
        self.br = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/rookb.png")
        self.wb = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/bishopw.png")
        self.bb = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/bishopb.png")
        self.wk = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/knightw.png")
        self.bk = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/knightb.png")
        self.wki = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/queenw.png")
        self.bki = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/queenb.png")
        self.wq = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/kingw.png")
        self.bq = pygame.image.load("/Users/fatihdeniz/Desktop/projects/chess/kingb.png")
        self.turn_text = "White"

    def draw_board(self):
        colors = [pygame.Color("white"), (65, 65, 65)]
        for r in range(Dimension):
            for c in range(Dimension):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.surface, color, pygame.Rect(c * size, r * size, size, size))

    def create_board(self):
        self.piece = [["br", "bk", "bb", "bq", "bki", "bb", "bk", "br"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wr", "wk", "wb", "wq", "wki", "wb", "wk", "wr"]]

        self.white_pieces = ["wp", "wr", "wk", "wb", "wq", "wki", "wb", "wk", "wr"]

        self.black_pieces = ["bp", "br", "bk", "bb", "bq", "bki", "bb", "bk", "br"]

    def draw_pieces(self):
        for r in range(Dimension):
            for c in range(Dimension):
                piece = self.piece[r][c]
                if piece != "-":
                    if piece == "wp":
                        self.surface.blit(self.wp, (c * size, r * size, size, size))
                    if piece == "bp":
                        self.surface.blit(self.bp, (c * size, r * size, size, size))
                    if piece == "wr":
                        self.surface.blit(self.wr, (c * size, r * size, size, size))
                    if piece == "br":
                        self.surface.blit(self.br, (c * size, r * size, size, size))
                    if piece == "wk":
                        self.surface.blit(self.wk, (c * size, r * size, size, size))
                    if piece == "bk":
                        self.surface.blit(self.bk, (c * size, r * size, size, size))
                    if piece == "wq":
                        self.surface.blit(self.wq, (c * size, r * size, size, size))
                    if piece == "bq":
                        self.surface.blit(self.bq, (c * size, r * size, size, size))
                    if piece == "wki":
                        self.surface.blit(self.wki, (c * size, r * size, size, size))
                    if piece == "bki":
                        self.surface.blit(self.bki, (c * size, r * size, size, size))
                    if piece == "wb":
                        self.surface.blit(self.wb, (c * size, r * size, size, size))
                    if piece == "bb":
                        self.surface.blit(self.bb, (c * size, r * size, size, size))

    def draw_side(self):
        pygame.draw.line(self.surface, (0, 0, 0), (640, 0), (640, 640), 2)
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(640, 0, 180, 50))
        pygame.draw.rect(self.surface, (0, 0, 0), (640, 0, 180, 50), 3)
        pygame.draw.line(self.surface, (0, 0, 0), (640, 320), (820, 320), 5)

        self.LETTER_FONT = pygame.font.SysFont('comicsans', 15)
        self.text = self.LETTER_FONT.render(self.turn_text, True, (0, 0, 0))
        self.surface.blit(self.text, (710, 15))

    def get_square(self):
        self.pos = pygame.Vector2(pygame.mouse.get_pos())
        self.x, self.y = [int(v // size) for v in self.pos]
        if self.x >= 0 and self.y >= 0:
            return self.piece[self.y][self.x], self.x, self.y


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        self.board = Board(self.surface)
        self.board.create_board()

    def pawn_logic(self):
        if self.stored_piece == "wp":
            if self.board.piece[self.new_y][self.new_x] not in self.board.black_pieces:
                if self.new_y == self.old_y - 1 and self.new_x == self.old_x:
                    return self.new_x, self.new_y
                else:
                    return self.old_x, self.old_y
            if self.board.piece[self.new_y][self.new_x] in self.board.black_pieces:
                if self.new_y == self.old_y - 1 and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                    return self.new_x, self.new_y
                else:
                    return self.old_x, self.old_y

        if self.stored_piece == "bp":
            if self.board.piece[self.new_y][self.new_x] not in self.board.white_pieces:
                if self.new_y == self.old_y + 1 and self.new_x == self.old_x:
                    return self.new_x, self.new_y
                else:
                    return self.old_x, self.old_y
            if self.board.piece[self.new_y][self.new_x] in self.board.white_pieces:
                if self.new_y == self.old_y + 1 and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                    return self.new_x, self.new_y
                else:
                    return self.old_x, self.old_y

    def rook_logic(self):
        if self.stored_piece == "wr" or self.stored_piece == "br":
            for i in range(1,7):
                    print("idk")
                    if (self.new_x == self.old_x and self.new_y == self.old_y - i):
                        return self.new_x, self.new_y
                    if self.new_x == self.old_x + i and self.new_y == self.old_y:
                        return self.new_x, self.new_y
                    if self.new_x == self.old_x and self.new_y == self.old_y + i:
                        return self.new_x, self.new_y
                    if self.new_x == self.old_x - i and self.new_y == self.old_y:
                        return self.new_x, self.new_y
            else:
                return self.old_x, self.old_y

    def bishop_logic(self):
        if self.stored_piece == "wb" or self.stored_piece == "bb":
            for i in range(7):
                if self.new_x == self.old_x + i and self.new_y == self.old_y + i:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x - i and self.new_y == self.old_y - i:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x + i and self.new_y == self.old_y - i:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x - i and self.new_y == self.old_y + i:
                    return self.new_x, self.new_y
            else:
                return self.old_x, self.old_y

    def knight_logic(self):
        if self.stored_piece == "wk" or self.stored_piece == "bk":
            if self.new_y == self.old_y - 2 and self.new_x == self.old_x + 1:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y - 2 and self.new_x == self.old_x - 1:
                return self.new_x, self.new_y
            elif self.new_x == self.old_x + 2 and self.new_y == self.old_y - 1:
                return self.new_x, self.new_y
            elif self.new_x == self.old_x - 2 and self.new_y == self.old_y - 1:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 2 and self.new_x == self.old_x + 1:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 2 and self.new_x == self.old_x - 1:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 1 and self.new_x == self.old_x + 2:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 1 and self.new_x == self.old_x - 2:
                return self.new_x, self.new_y
            else:
                return self.old_x, self.old_y

    def queen_logic(self):
        if self.stored_piece == "wq" or self.stored_piece == "bq":
            for i in range(7):
                if self.new_x == self.old_x and self.new_y == self.old_y - i:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x + i and self.new_y == self.old_y:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x and self.new_y == self.old_y + i:
                    return self.new_x, self.new_y
                if self.new_x == self.old_x - i and self.new_y == self.old_y:
                    return self.new_x, self.new_y
                if (self.new_x == self.old_x - i or self.new_x == self.old_x + i) and (
                        self.new_y == self.old_y - i or self.new_y == self.old_y + i):
                    return self.new_x, self.new_y
            else:
                return self.old_x, self.old_y

    def king_logic(self):
        if self.stored_piece == "wki" or self.stored_piece == "bki":
            if self.new_y == self.old_y - 1 and self.new_x == self.old_x:
                return self.new_x, self.new_y
            elif self.new_y == self.old_y - 1 and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 1 and self.new_x == self.old_x:
                return self.new_x, self.new_y
            elif self.new_y == self.new_y + 1 and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                return self.new_x, self.new_y
            elif self.new_y == self.old_y and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                return self.new_x, self.new_y
            elif self.new_y == self.old_y + 1 and (self.new_x == self.old_x + 1 or self.new_x == self.old_x - 1):
                return self.new_x, self.new_y
            else:
                return self.old_x, self.old_y

    def collusion(self):
        if self.stored_piece in self.board.white_pieces:
            for x in self.board.white_pieces:
                if self.board.piece[self.new_y][self.new_x] == x:
                    return self.old_x, self.old_y
            else:
                return self.new_x, self.new_y

        if self.stored_piece in self.board.black_pieces:
            for y in self.board.black_pieces:
                if self.board.piece[self.new_y][self.new_x] == y:
                    return self.old_x, self.old_y
            else:
                return self.new_x, self.new_y

    def checkmate(self):
        self.LETTER_FONT = pygame.font.SysFont('comicsans', 40)
        if sum(x.count("wki") for x in self.board.piece) == 0:
            self.text = self.LETTER_FONT.render("Black Wins", True, (51, 0, 25))
            self.surface.blit(self.text, (250, 250))
            self.pause = True

        if sum(x.count("bki") for x in self.board.piece) == 0:
            self.text = self.LETTER_FONT.render("White Wins", True, (51, 0, 25))
            self.surface.blit(self.text, (250, 250))
            self.pause = True

    def side_pieces(self):
        if sum(x.count("wp") for x in self.board.piece) <= 8:
            self.surface.blit(self.board.wp, (640, 50))
        if sum(x.count("wr") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.wr, (700, 50))
        if sum(x.count("wk") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.wk, (760, 50))
        if sum(x.count("wb") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.wb, (640, 200))
        if sum(x.count("wq") for x in self.board.piece) <= 1:
            self.surface.blit(self.board.wq, (700, 200))
        if sum(x.count("wki") for x in self.board.piece) <= 1:
            self.surface.blit(self.board.wki, (760, 200))

        if sum(x.count("bp") for x in self.board.piece) <= 8:
            self.surface.blit(self.board.bp, (640, 330))
        if sum(x.count("br") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.br, (700, 330))
        if sum(x.count("bk") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.bk, (760, 330))
        if sum(x.count("bb") for x in self.board.piece) <= 2:
            self.surface.blit(self.board.bb, (640, 480))
        if sum(x.count("bq") for x in self.board.piece) <= 1:
            self.surface.blit(self.board.bq, (700, 480))
        if sum(x.count("bki") for x in self.board.piece) <= 1:
            self.surface.blit(self.board.bki, (760, 480))

        # Text for White pieces
        self.LETTER_FONT = pygame.font.SysFont('comicsans', 20)
        self.text = self.LETTER_FONT.render(str(8 - sum(x.count("wp") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (665, 100))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("wr") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (725, 100))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("wk") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (785, 100))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("wb") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (665, 250))
        self.text = self.LETTER_FONT.render(str(1 - sum(x.count("wq") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (725, 250))
        self.text = self.LETTER_FONT.render(str(1 - sum(x.count("wki") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (785, 250))

        # Text for Black pieces
        self.text = self.LETTER_FONT.render(str(8 - sum(x.count("bp") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (665, 380))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("br") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (725, 380))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("bk") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (785, 380))
        self.text = self.LETTER_FONT.render(str(2 - sum(x.count("bb") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (665, 530))
        self.text = self.LETTER_FONT.render(str(1 - sum(x.count("bq") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (725, 530))
        self.text = self.LETTER_FONT.render(str(1 - sum(x.count("bki") for x in self.board.piece)), True, (0, 0, 0))
        self.surface.blit(self.text, (785, 530))

    def change(self):
        if self.stored_piece == "wp" and self.new_y == 0:
            self.board.piece[self.old_y][self.old_x] = "-"
            self.board.piece[self.new_y][self.new_x] = "wq"

        if self.stored_piece == "bp" and self.new_y == 7:
            self.board.piece[self.old_y][self.old_x] = "-"
            self.board.piece[self.new_y][self.new_x] = "bq"

    def reset(self):
        self.board.piece = [["br", "bk", "bb", "bq", "bki", "bb", "bk", "br"],
                            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                            ["wr", "wk", "wb", "wq", "wki", "wb", "wk", "wr"]]

        self.board.draw_board()
        self.board.draw_pieces()

    def run(self):
        running = True
        white = True
        black = False
        self.pause = False
        while running:
            if not self.pause:
                self.surface.fill((65, 65, 65, 1))
                self.board.draw_board()
                self.board.draw_pieces()
                self.checkmate()
                self.board.draw_side()
                self.side_pieces()
                for event in pygame.event.get():
                    piece, x, y = self.board.get_square()
                    # print(x,y,piece)
                    rect = (x * 80, y * 80, 80, 80)
                    pygame.draw.rect(self.surface, (255, 0, 0), rect, 3)
                    if event.type == MOUSEBUTTONDOWN:
                        self.stored_piece = piece
                        self.old_x, self.old_y = x, y
                        self.board.piece[y][x] = self.stored_piece
                    if event.type == MOUSEBUTTONUP:
                        self.new_x, self.new_y = x, y
                        print("old", self.old_y, self.old_x)
                        print("new", self.new_y, self.new_x)
                        self.old_piece = self.board.piece[self.new_y][self.new_x]
                        if self.stored_piece in self.board.white_pieces and white == True:
                            self.board.piece[self.old_y][self.old_x] = "-"
                            if self.stored_piece in self.board.white_pieces:
                                self.new_x, self.new_y = self.collusion()
                            if self.stored_piece in self.board.black_pieces:
                                self.new_x, self.new_y = self.collusion()
                            if self.stored_piece == "wp" or self.stored_piece == "bp":
                                self.new_x, self.new_y = self.pawn_logic()
                            elif self.stored_piece == "wr" or self.stored_piece == "br":
                                self.new_x, self.new_y = self.rook_logic()
                            elif self.stored_piece == "wb" or self.stored_piece == "bb":
                                self.new_x, self.new_y = self.bishop_logic()
                            elif self.stored_piece == "wk" or self.stored_piece == "bk":
                                self.new_x, self.new_y = self.knight_logic()
                            elif self.stored_piece == "wq" or self.stored_piece == "bq":
                                self.new_x, self.new_y = self.queen_logic()
                            elif self.stored_piece == "bki" or self.stored_piece == "wki":
                                self.new_x, self.new_y = self.king_logic()
                            self.board.piece[self.new_y][self.new_x] = self.stored_piece
                            self.change()
                            white = False
                            black = True
                            self.board.turn_text = "Black"
                            self.board.draw_side()

                        if self.stored_piece in self.board.black_pieces and black == True:
                            self.board.piece[self.old_y][self.old_x] = "-"
                            if self.stored_piece in self.board.white_pieces:
                                self.new_x, self.new_y = self.collusion()
                            if self.stored_piece in self.board.black_pieces:
                                self.new_x, self.new_y = self.collusion()
                            if self.stored_piece == "wp" or self.stored_piece == "bp":
                                self.new_x, self.new_y = self.pawn_logic()
                            elif self.stored_piece == "wr" or self.stored_piece == "br":
                                self.new_x, self.new_y = self.rook_logic()
                            elif self.stored_piece == "wb" or self.stored_piece == "bb":
                                self.new_x, self.new_y = self.bishop_logic()
                            elif self.stored_piece == "wk" or self.stored_piece == "bk":
                                self.new_x, self.new_y = self.knight_logic()
                            elif self.stored_piece == "wq" or self.stored_piece == "bq":
                                self.new_x, self.new_y = self.queen_logic()
                            elif self.stored_piece == "bki" or self.stored_piece == "wki":
                                self.new_x, self.new_y = self.king_logic()
                            self.board.piece[self.new_y][self.new_x] = self.stored_piece
                            self.change()
                            white = True
                            black = False
                            self.board.turn_text = "White"
                            self.board.draw_side()
                        if self.old_piece in self.board.black_pieces:
                            pass
                    if event.type == KEYDOWN:
                        if event.key == K_q:
                            running = False
                        if event.key == K_ESCAPE:
                            running = False

                pygame.display.flip()
                pygame.display.update()
            if self.pause:
                self.checkmate()
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_q:
                            running = False
                        if event.key == K_SPACE:
                            self.reset()
                            self.pause = False
                            white = True
                            black = False
                            self.board.turn_text = "White"
                            pygame.display.flip()
                            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
