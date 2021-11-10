from durable.lang import *


with ruleset('decision'):

    @when_all(+m.amount & (m.type == 'compensate_loss'))
    def decide_loss(c):
        loss_amount = c.m.amount

    @when_all(+m.part_rate & (m.type == 'production_stopped'))
    def decide_production_stopped(c):
        produced_parts = c.m.part_rates
        # todo invoke dialog what to do with these rates

    @when_all(+m.part_rate & (m.type == 'deficiency'))
    def deal_with_deficiency(c):
        pass
