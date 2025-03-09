import random


class Bridge:

    def __init__(self):
        self.N_card_library = {'♠': [], '♥': [], '♦': [], '♣': []}  # 北家牌库
        self.S_card_library = {'♠': [], '♥': [], '♦': [], '♣': []}  # 南家牌库
        self.W_card_library = {'♠': [], '♥': [], '♦': [], '♣': []}  # 西家牌库
        self.E_card_library = {'♠': [], '♥': [], '♦': [], '♣': []}  # 东家牌库
        self.N_distribution = []  # 北家分布
        self.S_distribution = []  # 南家分布
        self.W_distribution = []  # 西家分布
        self.E_distribution = []  # 东家分布

    def new_game(self):  # 新一局的创建
        def deal(library):  # 定义发牌函数
            lst = library[:13]  # 从打乱的牌库中选取前13张
            library[:13] = []  # 删除被选取的牌
            return lst  # 返回列表

        def append(lst, dic):  # 定义添加函数
            for card in lst:
                dic[card[0]].append(card)  # 根据花色分类添加

        def sort_(dic):  # 定义排序函数
            for v in dic.values():  # 遍历字典值
                v.sort(key=lambda x: rank_value(x[1:]), reverse=True)  # 按照牌面大小排序

        def rank_value(rank):  # 定义牌面大小
            match rank:
                case "A":
                    return 14
                case "K":
                    return 13
                case "Q":
                    return 12
                case "J":
                    return 11
                case "10":
                    return 10
                case _:
                    return int(rank)

        def points_calculation(card_library_):  # 定义算点函数
            points = 0
            for v in card_library_.values():
                for n1 in v:
                    match n1[1:]:
                        case "A":
                            points += 4
                        case "K":
                            points += 3
                        case "Q":
                            points += 2
                        case "J":
                            points += 1
                        case _:
                            pass
            card_library_["points"] = points

        def deal_all(card_library_):  # 发牌排序合并函数
            lst_ = deal(card_library)
            append(lst_, card_library_)
            sort_(card_library_)
            points_calculation(card_library_)
            print(card_library_)

        def distribution_get(card_library_, distribution):  # 定义牌型获取函数
            for v in card_library_.values():
                if type(v) != int:  # 检测到数字跳过
                    distribution.append(len(v))  # X-X-X-X ♠ ♥ ♦ ♣
            print(distribution)

        ranks = ['A', 'J', 'Q', 'K', '10', '9', '8', '7', '6', '5', '4', '3', '2']  # 牌库
        suits = ['♠', '♥', '♦', '♣']
        card_library = [suit + rank for rank in ranks for suit in suits]

        random.shuffle(card_library)  # 随机打乱牌库
        print("N家牌：")  # 牌型整理和输出
        deal_all(self.N_card_library)
        distribution_get(self.N_card_library, self.N_distribution)
        print("S家牌：")
        deal_all(self.S_card_library)
        distribution_get(self.S_card_library, self.S_distribution)
        print("E家牌：")
        deal_all(self.E_card_library)
        distribution_get(self.E_card_library, self.E_distribution)
        print("W家牌：")
        deal_all(self.W_card_library)
        distribution_get(self.W_card_library, self.W_distribution)
        print("新一局创建完毕")  # 创建完毕

    def bidding(self, opening_bidder):  # 叫牌阶段
        def ai_open_bidder(opening_bidder_):  # 选择AI开叫位置
            bid = " "  # 传递变量
            match opening_bidder_:
                case "N":
                    bid = ai_opening_bid(self.N_card_library, self.N_distribution)
                case "S":
                    bid = ai_opening_bid(self.S_card_library, self.S_distribution)
                case "W":
                    bid = ai_opening_bid(self.W_card_library, self.W_distribution)
                case "E":
                    bid = ai_opening_bid(self.E_card_library, self.E_distribution)
            print(f"{opening_bidder_}家AI开叫：{bid}")
            return bid  # 测试用临时传递变量

        def ai_opening_bid(card_library_, distribution):  # AI首家开叫逻辑（自然12点）
            if card_library_["points"] > 21:  # 22点以上或6点以下的任意牌型
                return "2♣"  # 22点及以上开叫2♣
            elif card_library_["points"] < 6:
                return "PASS"  # 6点以下PASS
            if card_library_["points"] < 12:  # 12点以下阻击叫
                n2 = 0  # 花色计数器 1 2 3 4 ♠ ♥ ♦ ♣
                for length in distribution:
                    n2 += 1
                    if 5 < length < 9:  # 6点以上12点以下6 ~ 8张
                        match n2:  # 2♠ 2♥ 2♦ PASS
                            case 1:
                                return "2♠"
                            case 2:
                                return "2♥"
                            case 3:
                                return "2♦"
                            case 4:
                                return "PASS"
                    elif length > 8:  # 6点以上12点以下9张以上
                        match n2:  # 3♠ 3♥ 3♦ 3♣
                            case 1:
                                return "3♠"
                            case 2:
                                return "3♥"
                            case 3:
                                return "3♦"
                            case 4:
                                return "3♣"
                    elif n2 == 4 and length < 6:  # 限定到草花
                        return "PASS"  # 11点以下无6张以上PASS
            if 14 < card_library_["points"] < 18:  # 15 ~ 17点
                n1 = 0  # 花色计数器 1 2 3 4 ♠ ♥ ♦ ♣
                if set(distribution) == {2, 3, 4} or set(distribution) == {3, 4}:  # 保证均型牌仅允许234张
                    return "1NT"  # 15 ~ 17点仅有234张开叫1NT
                else:  # 非均型牌
                    for length in distribution:
                        n1 += 1
                        if length > 4:  # 花色为5张以上
                            match n1:  # 1♠ 1♥ 1♦ 1♣
                                case 1:
                                    return "1♠"
                                case 2:
                                    return "1♥"
                                case 3:
                                    return "1♦"
                                case 4:
                                    return "1♣"
                        else:
                            return "1♣"  # 4441的15~17点叫1♣
            if card_library_["points"] > 19:  # 20 ~ 21 点
                n2 = 0  # 花色计数器 1 2 3 4 ♠ ♥ ♦ ♣
                if set(distribution) == {3, 4}:  # 保证4333
                    return "2NT"  # 20 ~ 21 均型牌叫2NT
                else:
                    for length in distribution:
                        n2 += 1
                        if length > 4:  # 花色为5张以上
                            match n2:  # 1♠ 1♥ 1♦ 1♣
                                case 1:
                                    return "1♠"
                                case 2:
                                    return "1♥"
                                case 3:
                                    return "1♦"
                                case 4:
                                    return "1♣"
                        else:  # 20 ~ 21点 没有5张以上
                            return "1♣"  # 叫1♣
            n2 = 0
            for length in distribution:  # 12 ~ 21点但不是NT的情况
                n2 += 1
                if length > 4:  # 花色5张以上
                    match n2:  # 1♠ 1♥ 1♦ 1♣
                        case 1:
                            return "1♠"
                        case 2:
                            return "1♥"
                        case 3:
                            return "1♦"
                        case 4:
                            return "1♣"
                elif n2 == 4 and length < 5:  # 限定到草花没有5张以上的花色
                    return "1♣"  # 叫1♣

        bid_ = ai_open_bidder(opening_bidder)  # 开叫
        return bid_


n = 0  # 计数器
a = " "  # 目标叫品
while a != "2♣":
    n += 1
    test = Bridge()  # 创建实例
    test.new_game()  # 发牌
    a = test.bidding("W")  # AI开叫
    print(n)
