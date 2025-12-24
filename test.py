from config.loguru_config import logger

def test(var_a: int):
    var_a += 1
    
def test1(dct: dict):
    dct[2] = "twotwo"
    dct[3] = "three"
    
import os

def main():
    # ss = "abcd"
    # for i, s in enumerate(ss[1:]):
    #     logger.info(f"{i = } {s = }")
    # if 1 < 2 and 3 < 4:
    #     logger.info("T")

    dct = dict()
    dct["1"] = 1
    print(dct)
 
if __name__ == "__main__":
    main()
