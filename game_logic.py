import random 
# bracket : 대진표

# (후보 목록)에 기반하여 (라운드)의 대진표(목록) 생성 함수
def create_brackets(round_num: int, candidates: list):
    random.shuffle(candidates)
    return candidates[:round_num]

# 대진표에서 랜덤으로 두 개씩 묶어서 매치하는 함수
def match_candidates(bracket: list):
    return [bracket[i:i+2] for i in range(0, len(bracket), 2)]
