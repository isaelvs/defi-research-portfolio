# Paper trading en vivo

[English](README.md) · **Español**

**Actualizado el 7 oct 2026.** Esta página la regenera un script una vez al día a partir del estado de los motores. El historial de commits de esta carpeta deja fechada cada foto.

![Equity](equity_es.png)

| Sistema | En marcha desde | Resultado | Caída máxima | Operaciones | Holdear en el periodo |
|---|---|---|---|---|---|
| Breakout long/short | 8 sep | +0,1% | −1,9% | 12 | +7,1% |
| Breakout spot, riesgo 1% | 8 sep | +1,9% | −3,7% | 6 | +7,5% |
| Ondas FVG 20% con filtro | 8 sep | +4,9% | −3,4% | 2 | +7,3% |
| Ondas FVG 10% con filtro | 8 sep* | +4,3% | −3,2% | 2 | +7,3% |
| Ruptura de estructura 20% | 14 sep | +3,6% | −2,2% | 3 | +8,4% |
| Ruptura de estructura 10% | 14 sep* | +3,9% | −2,5% | 3 | +8,4% |
| Corto ETH, colateral estable | 18 sep | −0,3% | −1,3% | 1 | ETH +4,8% |
| Rebalanceo EMA 50/150 | 27 sep | −0,2% | −2,0% | 0 | −0,3% |

*\* Las variantes del 10% se añadieron el 22 de septiembre de 2026. Su histórico anterior se reconstruyó aplicando el nuevo tamaño a las señales ya ejecutadas.*

## Cómo leerlo

- **1 de 8 sistemas van por delante de holdear** su activo desde que arrancaron. El más antiguo lleva 28 días: es poco tiempo para concluir nada sobre rentabilidad.
- **Es dinero simulado.** Cada sistema parte de 10.000 USD ficticios. Ninguno tiene capital real.
- **Se publica todo, también lo que va mal.** La tabla sale tal cual del estado de los motores, sin elegir sistemas ni periodos.
- **Lo que esta fase comprueba es la operativa:** que el sistema en vivo hace lo mismo que el backtest.

Las reglas de cada sistema y sus backtests están en el [caso del laboratorio](../case-studies/02-paper-trading-lab/README.es.md). La equity diaria de cada sistema está en [`data/daily.csv`](data/daily.csv).

---

*Metodología: los motores leen el precio de Binance cada 15 segundos y registran la equity a precio de mercado cada minuto. El resultado y la caída máxima se calculan sobre ese registro. «Operaciones» cuenta las cerradas en los sistemas de breakout y las compras y ventas en los de rebalanceo. «Holdear» es la variación del precio del activo entre el arranque de cada sistema y la última lectura. Resultados simulados; no garantizan resultados futuros.*
