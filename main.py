import asyncio
import time
from statistics import mean

import aiohttp

import docs
import markets

LIMIT = docs.LIMIT
VELOCITY_LIMIT = docs.VELOCITY_LIMIT
low_ceiling = docs.low_ceiling
height_ceiling = docs.height_ceiling

binance = markets.Binance()
gate = markets.Gate()
mexc = markets.Mexc()
huobi = markets.Huobi()
kucoin = markets.Kucoin()
bybit = markets.Bybit()
bitrue = markets.Bitrue()

all_coins = docs.recalibrate(binance.coins, gate.coins, mexc.coins, huobi.coins, kucoin.coins)


def smart_output(market_f, market_s, coin, asks_first, bids_first, asks_second, bids_second):
    asks_first_mean = mean(asks_first)  # Можно будет удалить мины, после отладки на массивах
    bids_first_mean = mean(bids_first)  # Ну, то есть не высчитывать их тут повторно, а сразу передавать в функцию
    asks_second_mean = mean(asks_second)
    bids_second_mean = mean(bids_second)
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("amount " + market_f + " asks", coin, " - ", asks_first_mean, "|||||", asks_first)
    print("amount " + market_f + " bids", coin, " - ", bids_first_mean, "|||||", bids_first, "\n")
    print("amount " + market_s + " asks", coin, " - ", asks_second_mean, "|||||", asks_second)
    print("amount " + market_s + " bids", coin, " - ", bids_second_mean, "|||||", bids_second, "\n")
    print("Типо спред - ", round(bids_second_mean / asks_first_mean, 2), " or - ",
          round(bids_first_mean / asks_second_mean, 2))
    print(market_f, " asks достигли ", VELOCITY_LIMIT, "USDT за ", len(asks_first), " ордера(-ов)")
    print(market_f, " bids достигли ", VELOCITY_LIMIT, "USDT за ", len(bids_first), " ордера(-ов)")
    print(market_s, " asks достигли ", VELOCITY_LIMIT, "USDT за ", len(asks_second), " ордера(-ов)")
    print(market_s, " bids достигли ", VELOCITY_LIMIT, "USDT за ", len(bids_second), " ордера(-ов)")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


final_binance_dict, final_gate_dict, final_mexc_dict, final_huobi_dict, final_kucoin_dict = {}, {}, {}, {}, {}


async def data_fetch():
    async with aiohttp.ClientSession() as session:

        tasks_binance, tasks_gate, tasks_mexc, tasks_huobi, tasks_kucoin = [], [], [], [], []

        final_binance, final_gate, final_mexc, final_huobi, final_kucoin = [], [], [], [], []

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

        responses_binance = await asyncio.gather(*tasks_binance)
        responses_gate = await asyncio.gather(*tasks_gate)
        responses_mexc = await asyncio.gather(*tasks_mexc)
        responses_huobi = await asyncio.gather(*tasks_huobi)
        responses_kucoin = await asyncio.gather(*tasks_kucoin)

        for b in responses_binance:
            try:
                final_binance.append(await b.json())
            except Exception as e:
                print("line 83, Rate limit binance??? - ", e)
                final_binance.append("_")

        for g in responses_gate:
            try:
                final_gate.append(await g.json())
            except Exception as e:
                print("line 90, Rate limit gate??? - ", e)
                final_gate.append("_")

        for m in responses_mexc:
            try:
                final_mexc.append(await m.json())
            except Exception as e:
                print("line 97, Rate limit mexc??? - ", e)
                final_mexc.append("_")

        for h in responses_huobi:
            try:
                final_huobi.append(await h.json())
            except Exception as e:
                print("line 104, Rate limit huobi??? - ", e)
                final_huobi.append("_")

        for k in responses_kucoin:
            try:
                final_kucoin.append(await k.json())
            except Exception as e:
                print("line 111, Rate limit kucoin??? - ", e)
                final_kucoin.append("_")

        for i, coin in zip(final_binance, binance.coins):
            final_binance_dict[coin] = i

        for i, coin in zip(final_gate, gate.coins):
            final_gate_dict[coin] = i

        for i, coin in zip(final_mexc, mexc.coins):
            final_mexc_dict[coin] = i

        for i, coin in zip(final_huobi, huobi.coins):
            final_huobi_dict[coin] = i

        for i, coin in zip(final_kucoin, gate.coins):
            final_kucoin_dict[coin] = i


def main():
    for coin in all_coins:
        counter_b_asks, counter_b_bids, counter_g_asks, counter_g_bids, counter_m_asks = 0, 0, 0, 0, 0
        counter_m_bids, counter_h_asks, counter_h_bids, counter_k_asks, counter_k_bids = 0, 0, 0, 0, 0

        binance_asks, binance_bids, gate_asks, gate_bids, mexc_asks = [], [], [], [], []
        mexc_bids, huobi_asks, huobi_bids, kucoin_asks, kucoin_bids = [], [], [], [], []

        b_ask, b_bid, g_ask, g_bid, h_ask, h_bid, m_ask, m_bid, k_ask, k_bid = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

        for lim in range(0, LIMIT):
            try:
                b_ask = float(final_binance_dict[coin]['asks'][lim][0])
                b_bid = float(final_binance_dict[coin]['bids'][lim][0])
                counter_b_asks += b_ask * float(final_binance_dict[coin]['asks'][lim][1])
                counter_b_bids += b_bid * float(final_binance_dict[coin]['bids'][lim][1])
            except Exception:
                pass

            try:
                g_ask = float(final_gate_dict[coin]['asks'][lim][0])
                g_bid = float(final_gate_dict[coin]['bids'][lim][0])
                counter_g_asks += g_ask * float(final_gate_dict[coin]['asks'][lim][1])
                counter_g_bids += g_bid * float(final_gate_dict[coin]['bids'][lim][1])
            except Exception:
                pass

            try:
                m_ask = float(final_mexc_dict[coin]['asks'][lim][0])
                m_bid = float(final_mexc_dict[coin]['bids'][lim][0])
                counter_m_asks += m_ask * float(final_mexc_dict[coin]['asks'][lim][1])
                counter_m_bids += m_bid * float(final_mexc_dict[coin]['bids'][lim][1])
            except Exception:
                pass

            try:
                h_ask = float(final_huobi_dict[coin]['tick']['asks'][lim][0])
                h_bid = float(final_huobi_dict[coin]['tick']['bids'][lim][0])
                counter_h_asks += h_ask * float(final_huobi_dict[coin]['tick']['asks'][lim][1])
                counter_h_bids += h_bid * float(final_huobi_dict[coin]['tick']['bids'][lim][1])
            except Exception:
                pass

            try:
                k_ask = float(final_kucoin_dict[coin]['data']['asks'][lim][0])
                k_bid = float(final_kucoin_dict[coin]['data']['bids'][lim][0])
                counter_k_asks += k_ask * float(final_kucoin_dict[coin]['data']['asks'][lim][1])
                counter_k_bids += k_bid * float(final_kucoin_dict[coin]['data']['bids'][lim][1])
            except Exception:
                pass

            if b_ask > 0 and counter_b_asks < VELOCITY_LIMIT:
                binance_asks.append(b_ask)
            if b_bid > 0 and counter_b_bids < VELOCITY_LIMIT:
                binance_bids.append(b_bid)
            if g_ask > 0 and counter_g_asks < VELOCITY_LIMIT:
                gate_asks.append(g_ask)
            if g_bid > 0 and counter_g_bids < VELOCITY_LIMIT:
                gate_bids.append(g_bid)
            if h_ask > 0 and counter_h_asks < VELOCITY_LIMIT:
                huobi_asks.append(h_ask)
            if h_bid > 0 and counter_h_bids < VELOCITY_LIMIT:
                huobi_bids.append(h_bid)
            if m_ask > 0 and counter_m_asks < VELOCITY_LIMIT:
                mexc_asks.append(m_ask)
            if m_bid > 0 and counter_m_bids < VELOCITY_LIMIT:
                mexc_bids.append(m_bid)
            if k_ask > 0 and counter_k_asks < VELOCITY_LIMIT:
                kucoin_asks.append(k_ask)
            if k_bid > 0 and counter_k_bids < VELOCITY_LIMIT:
                kucoin_bids.append(k_bid)

        binance_bids_mean = mean(binance_asks) if len(binance_asks) > 1 else -1
        binance_asks_mean = mean(binance_bids) if len(binance_bids) > 1 else -1
        gate_asks_mean = mean(gate_asks) if len(gate_asks) > 1 else -1
        gate_bids_mean = mean(gate_bids) if len(gate_bids) > 1 else -1
        huobi_asks_mean = mean(huobi_asks) if len(huobi_asks) > 1 else -1
        huobi_bids_mean = mean(huobi_bids) if len(huobi_bids) > 1 else -1
        mexc_asks_mean = mean(mexc_asks) if len(mexc_asks) > 1 else -1
        mexc_bids_mean = mean(mexc_bids) if len(mexc_bids) > 1 else -1
        kucoin_asks_mean = mean(kucoin_asks) if len(kucoin_asks) > 1 else -1
        kucoin_bids_mean = mean(kucoin_bids) if len(kucoin_bids) > 1 else -1

        if counter_b_asks > VELOCITY_LIMIT and counter_b_bids > VELOCITY_LIMIT:  # BINANCE with
            if height_ceiling > gate_bids_mean / binance_asks_mean > low_ceiling or height_ceiling > binance_bids_mean / gate_asks_mean > low_ceiling:  # gate
                smart_output("binance", "gate", coin, binance_asks, binance_bids, gate_asks, gate_bids)
            if height_ceiling > mexc_bids_mean / binance_asks_mean > low_ceiling or height_ceiling > binance_bids_mean / mexc_asks_mean > low_ceiling:  # mexc
                smart_output("binance", "mexc", coin, binance_asks, binance_bids, mexc_asks, mexc_bids)
            if height_ceiling > kucoin_bids_mean / binance_asks_mean > low_ceiling or height_ceiling > binance_bids_mean / kucoin_asks_mean > low_ceiling:  # kucoin
                smart_output("binance", "kucoin", coin, binance_asks, binance_bids, kucoin_asks, kucoin_bids)
            if height_ceiling > huobi_bids_mean / binance_asks_mean > low_ceiling or height_ceiling > binance_bids_mean / huobi_asks_mean > low_ceiling:  # huobi
                smart_output("binance", "huobi", coin, binance_asks, binance_bids, huobi_asks, huobi_bids)

        if counter_g_asks > VELOCITY_LIMIT and counter_g_bids > VELOCITY_LIMIT:  # GATE with
            if height_ceiling > mexc_bids_mean / gate_asks_mean > low_ceiling or height_ceiling > gate_bids_mean / mexc_asks_mean > low_ceiling:  # mexc
                smart_output("gate", "mexc", coin, gate_asks, gate_bids, mexc_asks, mexc_bids)
            if height_ceiling > kucoin_bids_mean / gate_asks_mean > low_ceiling or height_ceiling > gate_bids_mean / kucoin_asks_mean > low_ceiling:  # kucoin
                smart_output("gate", "kucoin", coin, gate_asks, gate_bids, kucoin_asks, kucoin_bids)
            if height_ceiling > huobi_bids_mean / gate_asks_mean > low_ceiling or height_ceiling > gate_bids_mean / huobi_asks_mean > low_ceiling:  # huobi
                smart_output("gate", "huobi", coin, gate_asks, gate_bids, huobi_asks, huobi_bids)

        if counter_m_asks > VELOCITY_LIMIT and counter_m_bids > VELOCITY_LIMIT:  # MEXC with
            if height_ceiling > kucoin_bids_mean / mexc_asks_mean > low_ceiling or height_ceiling > mexc_bids_mean / kucoin_asks_mean > low_ceiling:  # kucoin
                smart_output("mexc", "kucoin", coin, mexc_asks, mexc_bids, kucoin_asks, kucoin_bids)
            if height_ceiling > huobi_bids_mean / mexc_asks_mean > low_ceiling or height_ceiling > mexc_bids_mean / huobi_asks_mean > low_ceiling:  # huobi
                smart_output("mexc", "huobi", coin, mexc_asks, mexc_bids, huobi_asks, huobi_bids)

        if counter_h_asks > VELOCITY_LIMIT and counter_h_bids > VELOCITY_LIMIT:  # HUOBI with
            if height_ceiling > kucoin_bids_mean / huobi_asks_mean > low_ceiling or height_ceiling > huobi_bids_mean / kucoin_asks_mean > low_ceiling:
                smart_output("huobi", "kucoin", coin, huobi_asks, huobi_bids, kucoin_asks, kucoin_bids)


start = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(data_fetch())
main()
print("total time elapsed - " + str(time.time() - start))
