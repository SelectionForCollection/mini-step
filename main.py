import asyncio
import time
import aiohttp

import docs

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
        for coin in docs.binance_coins:
            tasks_binance.append(asyncio.create_task(session.get(docs.binance_url[0] + coin + docs.binance_url[1])))
        for coin in docs.gate_coins:
            tasks_gate.append(asyncio.create_task(session.get(docs.gate_url[0] + coin + docs.gate_url[1])))
        for coin in docs.mexc_coins:
            tasks_mexc.append(asyncio.create_task(session.get(docs.mexc_url[0] + coin + docs.mexc_url[1])))
        for coin in docs.huobi_coins:
            tasks_huobi.append(asyncio.create_task(session.get(docs.huobi_url[0] + coin + docs.huobi_url[1])))
        for coin in docs.kucoin_coins:
            tasks_kucoin.append(asyncio.create_task(session.get(docs.kucoin_url[0] + coin + docs.kucoin_url[1])))
        for coin in docs.bybit_coins:
            tasks_bybit.append(asyncio.create_task(session.get(docs.bybit_url[0] + coin + docs.bybit_url[1])))
        for coin in docs.bitrue_coins:
            tasks_bitrue.append(asyncio.create_task(session.get(docs.bitrue_url[0] + coin + docs.bitrue_url[1])))

        responses_binance = await asyncio.gather(*tasks_binance)
        responses_gate = await asyncio.gather(*tasks_gate)
        responses_mexc = await asyncio.gather(*tasks_mexc)
        responses_huobi = await asyncio.gather(*tasks_huobi)
        responses_kucoin = await asyncio.gather(*tasks_kucoin)
        # responses_bybit = await asyncio.gather(*tasks_bybit)
        # responses_bitrue = await asyncio.gather(*tasks_bitrue)
        # responses_okx = await asyncio.gather(*tasks_okx)

        try:
            final_binance = [await b.json() for b in responses_binance]
            final_gate = [await g.json() for g in responses_gate]
            final_mexc = [await m.json() for m in responses_mexc]
            final_huobi = [await h.json() for h in responses_huobi]
            final_kucoin = [await k.json() for k in responses_kucoin]
            # final_bybit = [await by.json() for by in responses_bybit]
            # final_bitrue = [await bit.json() for bit in responses_bitrue]
            # final_okx = [await okx.json() for okx in responses_okx]
        except Exception as e:
            print(e)
            exit(0)


start = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print("total time elapsed - " + str(time.time() - start))
