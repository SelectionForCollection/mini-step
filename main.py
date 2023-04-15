import asyncio
import time
from statistics import mean

import aiohttp

import docs
import markets


LIMIT = docs.LIMIT
binance = markets.Binance()
gate = markets.Gate()
mexc = markets.Mexc()
huobi = markets.Huobi()
kucoin = markets.Kucoin()
bybit = markets.Bybit()
bitrue = markets.Bitrue()

all_coins = docs.recalibrate(binance.coins, gate.coins, mexc.coins, huobi.coins, kucoin.coins)

tasks_binance = []
tasks_gate = []
tasks_mexc = []
tasks_huobi = []
tasks_kucoin = []
tasks_bybit = []
tasks_bitrue = []
tasks_okx = []


async def main():
    async with aiohttp.ClientSession() as session:
        for coin in binance.coins:
            tasks_binance.append(asyncio.create_task(session.get(docs.binance_url[0] + coin + docs.binance_url[1])))
        for coin in gate.coins:
            tasks_gate.append(asyncio.create_task(session.get(docs.gate_url[0] + coin + docs.gate_url[1])))
        for coin in mexc.coins:
            tasks_mexc.append(asyncio.create_task(session.get(docs.mexc_url[0] + coin + docs.mexc_url[1])))
        for coin in huobi.coins:
            tasks_huobi.append(asyncio.create_task(session.get(docs.huobi_url[0] + coin + docs.huobi_url[1])))
        for coin in kucoin.coins:
            tasks_kucoin.append(asyncio.create_task(session.get(docs.kucoin_url[0] + coin + docs.kucoin_url[1])))
        for coin in bybit.coins:
            tasks_bybit.append(asyncio.create_task(session.get(docs.bybit_url[0] + coin + docs.bybit_url[1])))
        for coin in bitrue.coins:
            tasks_bitrue.append(asyncio.create_task(session.get(docs.bitrue_url[0] + coin + docs.bitrue_url[1])))

        responses_binance = await asyncio.gather(*tasks_binance)
        responses_gate = await asyncio.gather(*tasks_gate)
        responses_mexc = await asyncio.gather(*tasks_mexc)
        responses_huobi = await asyncio.gather(*tasks_huobi)
        responses_kucoin = await asyncio.gather(*tasks_kucoin)

        try:
            final_binance = [await b.json() for b in responses_binance]
            final_gate = [await g.json() for g in responses_gate]
            final_mexc = [await m.json() for m in responses_mexc]
            final_huobi = [await h.json() for h in responses_huobi]
            final_kucoin = [await k.json() for k in responses_kucoin]
        except Exception as e:
            print(e)
            exit(0)

        final_binance_dict = {}
        for i, coin in final_binance, binance.coins:
            final_binance_dict[coin] = i

        print(final_binance_dict)
        exit(0)


start = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print("total time elapsed - " + str(time.time() - start))
