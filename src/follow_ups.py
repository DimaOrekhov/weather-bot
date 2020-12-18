import random


greeting_follow_ups = [
    'Могу ли я чем-то помочь?',
    'Что вы хотели бы узнать?'
]

follow_ups = [
    'Могу ли я помочь чем-то еще?',
    'Интересует ли что-то еще?',
    'Интересно ли узнать что-то еще?',
    'Предоставить какой-нибудь другой прогноз?'
]


def random_greeting_followup():
    return random.choice(greeting_follow_ups)


def random_followup():
    return random.choice(follow_ups)
