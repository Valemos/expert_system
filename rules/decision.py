from durable.lang import *


# test ruleset
with ruleset('decision'):

    @when_all(+m.amount & (m.type == 'compensate_loss'))
    def decide_loss(c):
        pass

    @when_all(+m.part_rates & (m.type == 'replace_machine'))
    def decide_replace_machine(c):
        pass

    @when_all(+m.part_rate & (m.type == 'deficiency'))
    def deal_with_deficiency(c):
        pass


# with ruleset('decision'):
#
#     @when_all(+m.amount & (m.type == 'compensate_loss'))
#     def decide_loss(c):
#         loss_amount = c.m.amount
#         # todo invoke dialog to try compensate
#
#     @when_all(+m.part_rates & (m.type == 'replace_machine'))
#     def decide_replace_machine(c):
#         produced_parts = c.m.part_rates
#         # todo invoke dialog what to do with these rates
#
#     @when_all(+m.part_rate & (m.type == 'deficiency'))
#     def deal_with_deficiency(c):
#         pass
#
