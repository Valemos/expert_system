from durable.lang import *

with ruleset('account'):

    @when_all(+m.loss)
    def try_compensate_loss(c):
        # todo invoke dialog to try compensate
        c.s.balance -= c.m.loss

    @when_all(+m.income)
    def make_transfer(c):
        c.s.balance += c.m.income


def init_account():
    update_state('account', {'balance': 0})
