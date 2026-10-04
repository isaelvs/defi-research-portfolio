#!/usr/bin/env python3
"""
update_live.py — Foto diaria del paper trading para el portfolio.

Lee el estado de cada motor (live_*_state/ del laboratorio), y regenera en live/:
  README.md, README.es.md   tabla de resultados frente a holdear
  equity_en.png, equity_es.png
  data/daily.csv            equity diaria de cada sistema (para quien quiera comprobar)

Uso:  python3 tools/update_live.py [--src ~/breakout_bt]
"""
import argparse, os
from datetime import datetime, timezone

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "live")
BG, GRID, INK, MUTED = "#fcfcfb", "#e8e7e3", "#0b0b0b", "#52514e"
BLUE = "#2a78d6"
CAPITAL = 10000.0

# (carpeta, clave, nombre es, nombre en, activo de referencia, histórico reconstruido)
SYSTEMS = [
    ("live_state",       "breakout_ls", "Breakout long/short",          "Breakout long/short",         "BTC", False),
    ("live_spot_state",  "breakout_spot", "Breakout spot, riesgo 1%",   "Spot breakout, 1% risk",      "BTC", False),
    ("live_fvg_state",   "fvg20",  "Ondas FVG 20% con filtro",          "FVG waves 20%, with filter",  "BTC", False),
    ("live_fvg10_state", "fvg10",  "Ondas FVG 10% con filtro",          "FVG waves 10%, with filter",  "BTC", True),
    ("live_bos_state",   "bos20",  "Ruptura de estructura 20%",         "Structure break 20%",         "BTC", False),
    ("live_bos10_state", "bos10",  "Ruptura de estructura 10%",         "Structure break 10%",         "BTC", True),
    ("live_short_state", "eth_short", "Corto ETH, colateral estable",   "ETH short, stable collateral", "ETH", False),
    ("live_ema_state",   "ema",    "Rebalanceo EMA 50/150",             "EMA 50/150 rebalancing",      "BTC", False),
]
MES = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
       "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}


def fecha(d, lang, year=False):
    s = f"{d.day} {MES[lang][d.month - 1]}"
    return f"{s} {d.year}" if year else s


def pct(v, lang, dec=1):
    v = round(v, dec) + 0.0
    s = f"{abs(v):.{dec}f}%"
    if lang == "es":
        s = s.replace(".", ",")
    return ("+" if v > 0 else "−" if v < 0 else "") + s


def load(src):
    out = []
    for folder, key, es, en, ref, rebuilt in SYSTEMS:
        d = os.path.join(src, folder)
        eq = pd.read_csv(os.path.join(d, "live_equity.csv"), usecols=["datetime", "equity_mtm", "price"])
        eq.index = pd.to_datetime(eq.pop("datetime"), utc=True, format="ISO8601")
        eq = eq[~eq.index.duplicated()].sort_index()
        tp = os.path.join(d, "live_trades.csv")
        n = max(0, sum(1 for _ in open(tp)) - 1) if os.path.exists(tp) else 0
        e = eq["equity_mtm"]
        out.append({
            "key": key, "es": es, "en": en, "ref": ref, "rebuilt": rebuilt,
            "start": eq.index[0], "last": eq.index[-1],
            "ret": (e.iloc[-1] / CAPITAL - 1) * 100,
            "dd": (e / e.cummax() - 1).min() * 100,
            "trades": n,
            "ref_ret": (eq["price"].iloc[-1] / eq["price"].iloc[0] - 1) * 100,
            "sys_curve": (e / CAPITAL - 1) * 100,
            "ref_curve": (eq["price"] / eq["price"].iloc[0] - 1) * 100,
            "daily": eq.resample("1D").last().dropna(),
        })
    return out


def chart(data, lang):
    t = {"es": dict(title="Paper trading en vivo: cada sistema frente a holdear",
                    sub="Resultado desde el arranque de cada sistema · 10.000 USD simulados · comisiones y slippage incluidos",
                    sys="Sistema", ref="Holdear {}"),
         "en": dict(title="Live paper trading: each system versus holding",
                    sub="Result since each system started · 10,000 simulated USD · fees and slippage included",
                    sys="System", ref="Hold {}")}[lang]
    fig, axes = plt.subplots(2, 4, figsize=(15, 8.1), dpi=100, sharey=True)
    fig.patch.set_facecolor(BG)
    for ax, s in zip(axes.flat, data):
        ax.set_facecolor(BG)
        ax.axhline(0, color=MUTED, lw=1, zorder=1)
        r = s["ref_curve"].resample("1h").last().dropna()
        y = s["sys_curve"].resample("1h").last().dropna()
        ax.plot(r.index, r.values, color="#a9a8a3", lw=1.6, zorder=2)
        ax.plot(y.index, y.values, color=BLUE, lw=2.0, zorder=3, solid_capstyle="round")
        ax.set_title(f"{s[lang]}\n{pct(s['ret'], lang)}  ·  {t['ref'].format(s['ref'])} {pct(s['ref_ret'], lang)}",
                     loc="left", fontsize=12, color=INK, pad=8, linespacing=1.5)
        ax.grid(axis="y", color=GRID, lw=1.2); ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(length=0, labelsize=11, colors=MUTED)
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=3))
        ax.xaxis.set_major_formatter(lambda x, _: fecha(mdates.num2date(x), lang))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        ax.yaxis.set_major_formatter(lambda v, _: pct(v, lang, 0) if v else "0%")
    h = [plt.Line2D([], [], color=BLUE, lw=3), plt.Line2D([], [], color="#a9a8a3", lw=3)]
    fig.legend(h, [t["sys"], t["ref"].format("BTC / ETH")], loc="upper right", bbox_to_anchor=(0.97, 0.985),
               frameon=False, fontsize=13, handlelength=1.6, ncol=2)
    fig.suptitle(t["title"], x=0.05, y=0.965, ha="left", fontsize=20, fontweight="bold", color=INK)
    fig.text(0.05, 0.905, t["sub"], fontsize=13, color=MUTED)
    fig.subplots_adjust(left=0.05, right=0.97, top=0.80, bottom=0.06, wspace=0.12, hspace=0.42)
    fig.savefig(os.path.join(OUT, f"equity_{lang}.png"), facecolor=BG)
    plt.close(fig)


def readme(data, lang, now):
    es = lang == "es"
    last = max(s["last"] for s in data)
    L = []
    if es:
        L += ["# Paper trading en vivo", "", "[English](README.md) · **Español**", "",
              f"**Actualizado el {fecha(last, lang, True)}.** Esta página la regenera un script una vez al día a partir "
              "del estado de los motores. El historial de commits de esta carpeta deja fechada cada foto.", "",
              "![Equity](equity_es.png)", "",
              "| Sistema | En marcha desde | Resultado | Caída máxima | Operaciones | Holdear en el periodo |",
              "|---|---|---|---|---|---|"]
    else:
        L += ["# Live paper trading", "", "**English** · [Español](README.es.md)", "",
              f"**Updated on {fecha(last, lang, True)}.** A script regenerates this page once a day from the state "
              "of the engines. The commit history of this folder timestamps every snapshot.", "",
              "![Equity](equity_en.png)", "",
              "| System | Running since | Result | Max drawdown | Trades | Holding over the period |",
              "|---|---|---|---|---|---|"]
    for s in data:
        ref = pct(s["ref_ret"], lang) if s["ref"] == "BTC" else f"ETH {pct(s['ref_ret'], lang)}"
        L.append(f"| {s[lang]} | {fecha(s['start'], lang)}{'*' if s['rebuilt'] else ''} | {pct(s['ret'], lang)} | "
                 f"{pct(s['dd'], lang)} | {s['trades']} | {ref} |")
    ahead = sum(s["ret"] > s["ref_ret"] for s in data)
    days = (last - min(s["start"] for s in data)).days
    if es:
        L += ["",
              "*\\* Las variantes del 10% se añadieron el 22 de septiembre de 2026. Su histórico anterior se "
              "reconstruyó aplicando el nuevo tamaño a las señales ya ejecutadas.*", "",
              "## Cómo leerlo", "",
              f"- **{ahead} de {len(data)} sistemas van por delante de holdear** su activo desde que arrancaron. "
              f"El más antiguo lleva {days} días: es poco tiempo para concluir nada sobre rentabilidad.",
              "- **Es dinero simulado.** Cada sistema parte de 10.000 USD ficticios. Ninguno tiene capital real.",
              "- **Se publica todo, también lo que va mal.** La tabla sale tal cual del estado de los motores, sin elegir sistemas ni periodos.",
              "- **Lo que esta fase comprueba es la operativa:** que el sistema en vivo hace lo mismo que el backtest.",
              "", "Las reglas de cada sistema y sus backtests están en el "
              "[caso del laboratorio](../case-studies/02-paper-trading-lab/README.es.md). "
              "La equity diaria de cada sistema está en [`data/daily.csv`](data/daily.csv).", "",
              "---", "",
              "*Metodología: los motores leen el precio de Binance cada 15 segundos y registran la equity a precio de mercado "
              "cada minuto. El resultado y la caída máxima se calculan sobre ese registro. «Operaciones» cuenta las "
              "cerradas en los sistemas de breakout y las compras y ventas en los de rebalanceo. «Holdear» es la variación "
              "del precio del activo entre el arranque de cada sistema y la última lectura. Resultados simulados; no garantizan resultados futuros.*"]
    else:
        L += ["",
              "*\\* The 10% variants were added on 22 September 2026. Their earlier history was rebuilt by applying "
              "the new size to the signals already executed.*", "",
              "## How to read it", "",
              f"- **{ahead} of {len(data)} systems are ahead of holding** their asset since they started. "
              f"The oldest has been running for {days} days: too short to conclude anything about profitability.",
              "- **It is simulated money.** Each system starts from 10,000 fictional USD. None has real capital.",
              "- **Everything is published, including what goes badly.** The table comes straight from the state of the engines, with no picking of systems or periods.",
              "- **What this phase checks is the operation:** that the live system does the same as the backtest.",
              "", "The rules of each system and their backtests are in the "
              "[lab case study](../case-studies/02-paper-trading-lab/README.md). "
              "The daily equity of each system is in [`data/daily.csv`](data/daily.csv).", "",
              "---", "",
              "*Methodology: the engines read the Binance price every 15 seconds and record mark-to-market equity every "
              "minute. Result and max drawdown are computed on that record. \"Trades\" counts closed trades for the breakout "
              "systems and buys and sells for the rebalancing ones. \"Holding\" is the change in the asset's price between "
              "each system's start and the last reading. Simulated results; they do not guarantee future results.*"]
    name = "README.es.md" if es else "README.md"
    open(os.path.join(OUT, name), "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.expanduser("~/breakout_bt"))
    args = ap.parse_args()
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    data = load(args.src)
    now = datetime.now(timezone.utc)
    rows = []
    for s in data:
        d = s["daily"]
        rows.append(pd.DataFrame({"date": d.index.strftime("%Y-%m-%d"), "system": s["key"],
                                  "equity_usd": d["equity_mtm"].round(2).values,
                                  "price": d["price"].round(2).values}))
    pd.concat(rows).to_csv(os.path.join(OUT, "data", "daily.csv"), index=False)
    for lang in ("es", "en"):
        chart(data, lang)
        readme(data, lang, now)
    for s in data:
        print(f"{s['es']:32s} {s['ret']:+6.1f}%  dd {s['dd']:5.1f}%  ops {s['trades']:2d}  ref {s['ref_ret']:+6.1f}%")


if __name__ == "__main__":
    main()
