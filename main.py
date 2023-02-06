import random
from combinations import test_comb, ddl

# 掉落模拟器
class Generator:
    def __init__(self):
        # 各个部位掉落概率，分别为生之花、死之羽、时之沙、空之杯和理之冠的掉落概率
        self.p_part = [0.2, 0.2, 0.2, 0.2, 0.2]

        # 时之沙主次条的掉落概率，分别为生命值，攻击力，防御力，元素充能效率和元素精通的概率
        self.p_sandClock = [0.2668, 0.2666, 0.2666, 0.1, 0.1]

        # 空之杯主次条的掉落概率，分别为生命值，攻击力，防御力，火、雷、冰、水、风、岩伤害加成和物理伤害加成以及元素精通的概率
        self.p_cup = [0.2125, 0.2125, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.025]

        # 理之冠主词条的掉落概率，分别为生命值，攻击力，防御力，暴击率，暴击伤害，治疗加成和元素精通的概率
        self.p_hat = [0.22, 0.22, 0.22, 0.1, 0.1, 0.1, 0.04]

    def generate(self):
        # 掉落的部位，0 - 4分别代表花、羽、沙、杯和冠
        # 需要python的版本大等于3.6
        loc = random.choices(range(5), weights = self.p_part)[0]

        if loc == 0 or loc == 1:
            main_term = -1
        elif loc == 2:
            main_term = random.choices(range(5), weights = self.p_sandClock)[0]
        elif loc == 3:
            main_term = random.choices(range(11), weights = self.p_cup)[0]
        else:
            main_term = random.choices(range(7), weights = self.p_hat)[0]

        return loc, main_term

# 历史记录
class History:
    def __init__(self):
        # 历史记录是一个bool字典
        self.records = []

        # 历史记录的第一维记录时之沙各个属性是否出现过，顺序同上
        self.records.append([False] * 5)

        # 历史记录的第二维记录空之杯各个属性是否出现过，顺序同上
        self.records.append([False] * 11)

        # 历史记录的第三维记录理之冠各个属性是否出现过，顺序同上
        self.records.append([False] * 7)

    # 增加历史记录
    def add_record(self, loc, main_term):
        if loc <= 1:
            return
        self.records[loc-2][main_term] = True

    def has_holy_relic(self, loc, main_term):
        return self.records[loc][main_term]


# 毕业的圣遗物
class Qualified_Holy_Relic:
    def __init__(self):
        # 圣遗物的组合，是一个三维向量，编号顺序同上
        # 第一个数表示时之沙的属性，编号为0-4
        # 第二个数表示空之杯的属性，编号为0-10
        # 第三个数表示理之冠的属性，编号为0-6
        self.groups=[]

    # 增添合法的圣遗物组合
    def add_group(self, group):
        self.groups.append(group)

    # 检验是否已经抽到了毕业的圣遗物
    # 注意：沙、杯和冠只需要抽到两个主次条正确的即可
    def is_ok(self, history):
        ok_num = 3
        for group in self.groups:
            for loc in range(3):
                if not history.has_holy_relic(loc, group[loc]):
                    ok_num -= 1
            if ok_num >= 2:
                return True
        return False


if __name__ == '__main__':
    groups = Qualified_Holy_Relic()

    for group in test_comb:
        groups.add_group(group)


    gen = Generator()

    # Monte-Carlo模拟的次数
    num_epoch = 2000

    # 期望刷本次数
    avg_iter = 0
    # 在deadline前出结果的次数
    before_ddl = 0
    for epoch in range(num_epoch):
        history = History()
        # 本轮迭代刷本次数
        num_iter = 0
        while not groups.is_ok(history):
            # 每个本一般有两套圣遗物，所以只有1/2的概率能刷到想要的那套
            if random.randint(0,1) > 0:
                history.add_record(*gen.generate())
            num_iter += 1
        print(f'第{epoch + 1}轮刷本次数：{num_iter}')
        # ddl的单位是天数，9这个常数是每天最大刷本次数(不考虑用脆弱树脂)
        before_ddl += int(num_iter <= ddl * 9)
        avg_iter = (avg_iter * epoch + num_iter) / (epoch + 1)

    print('')
    print(f'期望刷本次数：{avg_iter:.3f}')
    print(f'期望刷本天数: {avg_iter / 9: .3f}')
    if ddl > 0:
        print(f'在{ddl}天内出货的概率是：{before_ddl / num_epoch :.3f}')
