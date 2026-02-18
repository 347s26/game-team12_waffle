from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    win_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} has solved {self.win_streak} waffles in a row!"


class Waffle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Waffle {self.id}"


class Word(models.Model):
    waffle = models.ForeignKey(Waffle, on_delete=models.CASCADE, related_name="words")
    text = models.CharField(max_length=5)
    orientation = models.CharField(
        max_length=1, choices=[("H", "Horizontal"), ("V", "Vertical")]
    )
    index = models.IntegerField()

    def __str__(self):
        return self.text


class Tile(models.Model):
    waffle = models.ForeignKey(Waffle, on_delete=models.CASCADE, related_name="tiles")
    row = models.IntegerField()
    col = models.IntegerField()
    letter = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.letter} ({self.row},{self.col})"


class GameState(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="games")
    waffle = models.ForeignKey(Waffle, on_delete=models.CASCADE)
    moves_remaining = models.IntegerField(default=15)
    is_solved = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} — {self.player}"


class GameTile(models.Model):
    game = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name="tiles")
    row = models.IntegerField()
    col = models.IntegerField()
    letter = models.CharField(max_length=1)

    TILE_STATUS = (
        ("green", "Correct"),
        ("yellow", "In Word"),
        ("gray", "Incorrect"),
    )

    status = models.CharField(max_length=6, choices=TILE_STATUS, default="gray")

    @property
    def is_locked(self):
        return self.status == "green"

    def __str__(self):
        return f"{self.letter} ({self.row},{self.col})"
