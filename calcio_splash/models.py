from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=False, blank=False, default=2017)

    MALE = 'M'
    FEMALE = 'F'
    BEACH = 'B'
    GENDER_CHOICES = ((MALE, 'Maschile'), (FEMALE, 'Femminile'), (BEACH, 'Beach Volley'))
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE)

    def _get_symbol_for_team(self):
        if self.gender == Team.BEACH:
            return '🏖'
        if self.gender == Team.FEMALE:
            return '♀'
        return '♂'

    def __str__(self):
        return '{} {} ({})'.format(self._get_symbol_for_team(), self.name, self.year)


class Player(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    nickname = models.CharField(max_length=50, blank=True, null=True)
    teams = models.ManyToManyField(Team, related_name='player', blank=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return " ".join([self.name, self.surname])


class Tournament(models.Model):
    name = models.CharField(max_length=250)
    edition_year = models.IntegerField()
    team_1 = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name='rankings_1')
    team_2 = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name='rankings_2')
    team_3 = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name='rankings_3')

    goalkeeper = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name='goalkeeper')
    top_scorer = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name='top_scorer')

    def __str__(self):
        return '{} ({})'.format(self.name, self.edition_year)

    @property
    def gender(self):
        if self.team_1 is not None:
            return self.team_1.gender
        if "beach" in self.name.lower():
            return Team.BEACH
        return Team.MALE if "maschile" in self.name.lower() else Team.FEMALE


class Group(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')

    is_final = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ("ordering", "pk")

    def __str__(self):
        return '{} ({})'.format(self.name, self.tournament.edition_year)


class Match(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_a', null=True, blank=True)
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_b', null=True, blank=True)
    match_date_time = models.DateTimeField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='matches')

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    end_primo_tempo = models.DateTimeField(null=True, blank=True)
    start_secondo_tempo = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self):
        return '{} vs {} ({})'.format(self.team_a, self.team_b, self.group)

    @property
    def score_a(self) -> int:
        return self.goals.filter(team=self.team_a).count()

    @property
    def score_b(self) -> int:
        return self.goals.filter(team=self.team_b).count()

    @property
    def team_a_score(self):
        return self.score_a

    @property
    def team_b_score(self):
        return self.score_b

    @property
    def winner(self):
        if not self.ended:
            return None
        return self.team_a if self.score_a > self.score_b else self.team_b

    @property
    def loser(self):
        if not self.ended:
            return None
        return self.team_b if self.score_a > self.score_b else self.team_a

    @property
    def ended(self):
        return self.end_time is not None

    @property
    def started(self):
        # [sp] it would be nice to use `start_date`, but we are not setting it anywhere; let's rely on the score;
        return self.score_a > 0 or self.score_b > 0 or self.ended


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='goals', null=True, blank=True)
    minute = models.IntegerField()


class BeachMatch(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='beach_matches_a', null=True, blank=True)
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='beach_matches_b', null=True, blank=True)
    match_date_time = models.DateTimeField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='beach_matches')

    team_a_set_1 = models.IntegerField(null=True, blank=True)
    team_b_set_1 = models.IntegerField(null=True, blank=True)

    team_a_set_2 = models.IntegerField(null=True, blank=True)
    team_b_set_2 = models.IntegerField(null=True, blank=True)

    team_a_set_3 = models.IntegerField(null=True, blank=True)
    team_b_set_3 = models.IntegerField(null=True, blank=True)

    ended = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Beach Matches'

    def __str__(self):
        return '{} vs {} ({})'.format(self.team_a, self.team_b, self.group)

    def to_dict(self):
        return {
            'id': self.id,
            'team_a_set_1': self.team_a_set_1,
            'team_b_set_1': self.team_b_set_1,
            'team_a_set_2': self.team_a_set_2,
            'team_b_set_2': self.team_b_set_2,
            'team_a_set_3': self.team_a_set_3,
            'team_b_set_3': self.team_b_set_3,
        }

    @property
    def winner(self):
        if not self.ended:
            return None
        set_a_won, set_b_won = self._compute_set_won()
        return self.team_a if set_a_won > set_b_won else self.team_b

    @property
    def loser(self):
        if not self.ended:
            return None
        set_a_won, set_b_won = self._compute_set_won()
        return self.team_a if set_a_won < set_b_won else self.team_b

    @property
    def is_tie(self):
        if not self.ended:
            return None
        set_a_won, set_b_won = self._compute_set_won()
        # [sp] in a "final" match, ties can't happen; in a "girone" match, we only have one set, and a tie
        # is represented by both teams winning no sets
        return set_a_won == set_b_won == 0

    def _compute_set_won(self) -> (int, int):
        set_a_won = 0
        set_b_won = 0
        if self.team_a_set_3 is not None:
            set_a_won += 1 if self.team_a_set_3 > self.team_b_set_3 else 0
            set_b_won += 1 if self.team_b_set_3 > self.team_a_set_3 else 0
        if self.team_a_set_2 is not None:
            set_a_won += 1 if self.team_a_set_2 > self.team_b_set_2 else 0
            set_b_won += 1 if self.team_b_set_2 > self.team_a_set_2 else 0
        if self.team_a_set_1 is not None:
            set_a_won += 1 if self.team_a_set_1 > self.team_b_set_1 else 0
            set_b_won += 1 if self.team_b_set_1 > self.team_a_set_1 else 0
        return set_a_won, set_b_won
