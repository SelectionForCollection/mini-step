import docs


class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    TEAL = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(f"{bcolors.TEAL}SelectionForCollection{bcolors.ENDC} presents:\n")
#coins len
print(f"{bcolors.YELLOW}Coins in USDT pair from each market info:{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}binance{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.binance_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}gate{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.gate_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}mexc{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.mexc_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}huobi{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.huobi_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}kucoin{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.kucoin_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}bybit{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.bybit_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}bitrue{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.bitrue_coins)}{bcolors.ENDC}\n"
      f"\t{bcolors.BOLD}okx{bcolors.ENDC} - {bcolors.UNDERLINE}{len(docs.okx_coins)}{bcolors.ENDC}")
#base info
print(f"{bcolors.YELLOW}General info:{bcolors.ENDC}\n"
      f"\tLIMIT - {bcolors.UNDERLINE}{docs.LIMIT}{bcolors.ENDC}\n"
      f"\tVELOCITY_LIMIT - {bcolors.UNDERLINE}{docs.VELOCITY_LIMIT}{bcolors.ENDC}\n"
      f"\theight_celling - {bcolors.UNDERLINE}{docs.height_ceiling}{bcolors.ENDC}\n"
      f"\tlow_celling - {bcolors.UNDERLINE}{docs.low_ceiling}{bcolors.ENDC}")
