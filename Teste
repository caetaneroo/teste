{
  "chart": {
    "type": "scatter"
  },
  "xAxis": {
    "type": "category",
    "categories": ["unique", ["getColumn", 0]], // Intervalo de Tempo (30 min)
    "labels": {
      "step": 1,
      "align": "right",
      "style": {
        "fontSize": "12px"
      }
    }
  },
  "yAxis": {
    "title": {
      "text": "Tempo de Fila (em minutos)"
    }
  },
  "tooltip": {
    "pointFormat": "<b>{series.name}</b>: <b>{point.y:,.2f}</b> minutos"
  },
  "plotOptions": {
    "scatter": {
      "marker": {
        "radius": 4
      }
    }
  },
  "series": [
    {
      "name": "Dispersão do Tempo de Fila por Contato",
      "type": "scatter",
      "data": [
        "map",
        ["getColumn", 0, 1, 2], // Intervalo de Tempo, Tempo de Fila, ID do Contato
        {
          "x": ["get", ["item"], 0], // Intervalo de Tempo
          "y": ["get", ["item"], 1], // Tempo de Fila
          "contactId": ["get", ["item"], 2] // ID do Contato (para a dispersão por contato)
        }
      ]
    },
    {
      "name": "Média do Tempo de Fila",
      "type": "line",
      "data": [
        "map",
        ["unique", ["getColumn", 0]], // Intervalo de Tempo
        {
          "y": [
            "/",
            ["reduce",
              ["filter",
                ["getColumn", 0, 1], // Intervalo de Tempo, Tempo de Fila
                ["==", ["get", ["item"], 0], ["item", 0]] // Filtrando por Intervalo de Tempo
              ],
              ["+", ["acc"], ["get", ["item"], 1]], // Soma dos Tempos de Fila
              0 // Valor inicial do acumulador
            ],
            ["reduce",
              ["filter",
                ["getColumn", 0, 1],
                ["==", ["get", ["item"], 0], ["item", 0]]
              ],
              ["+", ["acc"], 1],
              0
            ] // Contagem de linhas por Intervalo de Tempo
          ]
        }
      ]
    }
  ]
}
