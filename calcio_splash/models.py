from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Maschile'),
        (FEMALE, 'Femminile'),
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE
    )

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)


class Tournament(models.Model):
    name = models.CharField(max_length=250)
    edition_year = models.IntegerField()

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name


class Match(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_b')
    match_date_time = models.DateTimeField()

    next_match = models.ForeignKey('self', null=True, related_name='prev_matches')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='matches')

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return '{} vs {} ({})'.format(self.team_a, self.team_b, self.group)


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='goals')
    minute = models.IntegerField()

    def __str__(self):
        return "{}: goal by {} ({}) at {}'".format(self.match, self.player, self.team, self.minute)
