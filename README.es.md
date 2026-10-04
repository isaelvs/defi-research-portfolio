# Research de estrategias DeFi y cripto

[English](README.md) · **Español**

*Por Isael*

Diseño estrategias de inversión y trading sobre BTC y DeFi, las valido con backtests y las pongo a prueba en paper trading automatizado antes de arriesgar capital real. Este repositorio documenta ese trabajo en forma de casos, incluidas las ideas que no pasaron la validación y por qué.

## Casos

| | Caso | Qué muestra |
|---|---|---|
| 01 | [Bot de liquidez concentrada en Uniswap v3](case-studies/01-uniswap-v3-lp-bot/README.es.md) | Un bot en Arbitrum con dinero real, medido frente a holdear y descartado. Incluye un error que encontré en mi propia métrica. |
| 02 | [Laboratorio de trading sistemático](case-studies/02-paper-trading-lab/README.es.md) | Un backtester y 8 sistemas sobre BTC en paper trading, validados en tres regímenes de mercado. |
| 03 | [Copiar a un streamer de trading](case-studies/03-copy-trading-validation/README.es.md) | Un estudio de cómo engaña una muestra de un mes, a partir de 198 directos transcritos. Las cifras son orientativas; las limitaciones están en el caso. |
| 04 | [Estrategia de ciclos del halving de BTC](case-studies/04-halving-cycle-strategy/README.es.md) | Una regla de calendario probada en tres ciclos, con siete variantes de entrada y cinco de salida, y un cuarto ciclo en marcha. |

## Paper trading en vivo

[**Foto diaria de los 8 sistemas frente a holdear**](live/README.es.md), regenerada automáticamente una vez al día. El historial de commits deja fechada cada foto, y los resultados se publican sean buenos o malos.

## Cómo trabajo

- **Comparar contra holdear, no contra cero.** En un mercado alcista casi cualquier regla gana dinero y casi ninguna gana a no hacer nada.
- **Reservar datos que la idea no ha visto.** Una idea solo avanza si aguanta fuera de muestra, en mercado alcista y en bajista.
- **Paper trading antes que capital.** Sirve para comprobar que el sistema en vivo hace lo mismo que el backtest.
- **Saber descartar.** Dos de los cuatro casos terminan con la idea abandonada.

El desarrollo es asistido por IA: el diseño de las estrategias, las reglas de riesgo y la validación son míos.

*Nada de esto es una recomendación de inversión. Resultados pasados y simulados no garantizan resultados futuros.*
