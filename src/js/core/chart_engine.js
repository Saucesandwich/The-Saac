/**
 * The Saac Financial Terminal - Universal Chart Engine
 * Modular wrapper around Chart.js supporting multi-asset line, caves (area),
 * and custom candlestick rendering, drag-to-measure tool, and dynamic point sizing.
 */

import { Analytics } from './analytics.js';

export const candlestickPlugin = {
  id: 'candlestickRenderer',
  beforeDatasetsDraw(chart) {
    if (chart.canvas.id !== 'historicalChartCanvas') return;
    const style = chart.config._saacStyle || 'line';
    if (style !== 'candles') return;

    const meta = chart.getDatasetMeta(0);
    if (!meta || meta.hidden) return;

    const ctx = chart.ctx;
    const xAxis = chart.scales.x;
    const yAxis = chart.scales.y;
    if (!xAxis || !yAxis) return;

    const activeData = chart.config._saacActiveData || [];
    const dataLen = activeData.length;
    if (!dataLen) return;

    ctx.save();
    ctx.beginPath();
    ctx.rect(chart.chartArea.left, chart.chartArea.top, chart.chartArea.width, chart.chartArea.height);
    ctx.clip();

    const candleWidth = Math.max(3, Math.min(22, (chart.chartArea.width / dataLen) * 0.65));

    activeData.forEach((candle, i) => {
      if (!candle) return;
      const x = Math.round(xAxis.getPixelForValue(i));
      const openVal = candle.open !== undefined ? candle.open : candle.close;
      const closeVal = candle.close;
      const highVal = candle.high !== undefined ? candle.high : Math.max(openVal, closeVal);
      const lowVal = candle.low !== undefined ? candle.low : Math.min(openVal, closeVal);

      const openY = yAxis.getPixelForValue(openVal);
      const closeY = yAxis.getPixelForValue(closeVal);
      const highY = yAxis.getPixelForValue(highVal);
      const lowY = yAxis.getPixelForValue(lowVal);

      const isUp = closeVal >= openVal;
      const color = isUp ? '#00c853' : '#ef4444';

      // Wick
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.moveTo(x, highY);
      ctx.lineTo(x, lowY);
      ctx.stroke();

      // Body
      const topY = Math.min(openY, closeY);
      const height = Math.max(2, Math.abs(closeY - openY));

      ctx.fillStyle = color;
      ctx.fillRect(x - candleWidth / 2, topY, candleWidth, height);
      ctx.strokeStyle = color;
      ctx.strokeRect(x - candleWidth / 2, topY, candleWidth, height);
    });

    ctx.restore();
  }
};

export class ChartEngine {
  constructor() {
    this.liveChartInstance = null;
    this.histChartInstance = null;
    this.currentStyle = 'line';
    this.currentScaleType = 'linear';
  }

  /**
   * Initializes or updates the real-time tick chart.
   * @param {HTMLCanvasElement} canvas
   * @param {Array<string>} labels
   * @param {Array<number>} data
   * @param {object} instrument
   */
  initLiveChart(canvas, labels, data, instrument) {
    if (!canvas || typeof Chart === 'undefined') return null;
    const ctx = canvas.getContext('2d');
    const themeColor = instrument?.themeColor || '#ff9800';

    const minP = Math.min(...data);
    const maxP = Math.max(...data);
    const pad = Math.max(1.0, (maxP - minP) * 0.15);

    if (this.liveChartInstance) {
      this.liveChartInstance.destroy();
    }

    this.liveChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: `${instrument?.shortName || 'Asset'} Intraday (${instrument?.primaryTicker || 'LIVE'})`,
          data: data,
          borderColor: themeColor,
          backgroundColor: 'transparent',
          borderWidth: 2,
          tension: 0.1,
          fill: false,
          pointBackgroundColor: themeColor,
          pointBorderColor: '#0a0b0d',
          pointBorderWidth: 1,
          pointRadius: (ctx) => (ctx.dataIndex === data.length - 1 ? 4 : 1.5),
          pointHoverRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 150 },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#12151b',
            titleColor: themeColor,
            titleFont: { family: 'JetBrains Mono', size: 11, weight: 'bold' },
            bodyFont: { family: 'JetBrains Mono', size: 11 },
            borderColor: '#2e3546',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {
              title: (items) => `${items[0].label} (Live 5m)`,
              label: (item) => {
                const lines = [` ${instrument?.shortName || 'Asset'} (${instrument?.primaryTicker || 'Spot'}): $${item.parsed.y.toLocaleString('en-US', { minimumFractionDigits: 1 })} USD/${instrument?.unit || 'unit'}`];
                if (instrument?.id === 'gold') {
                  const thbVal = Math.round((item.parsed.y * (window.currentUsdThb || 33.56) / 31.1034768) * 0.965 * 15.244);
                  lines.push(` Thai Gold Bar: ฿${thbVal.toLocaleString()} THB`);
                }
                return lines;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#181d26' },
            ticks: { color: '#828a99', font: { family: 'JetBrains Mono', size: 10 }, maxTicksLimit: 8 }
          },
          y: {
            grid: { color: '#181d26' },
            min: Math.floor(minP - pad),
            max: Math.ceil(maxP + pad),
            title: { display: true, text: `USD / ${instrument?.unit || 'unit'}`, color: themeColor, font: { family: 'JetBrains Mono', weight: '700', size: 10 } },
            ticks: {
              color: themeColor,
              font: { family: 'JetBrains Mono', size: 10 },
              callback: (v) => '$' + v.toLocaleString()
            }
          }
        }
      }
    });

    return this.liveChartInstance;
  }

  /**
   * Initializes the historical interactive chart.
   * @param {HTMLCanvasElement} canvas
   * @param {Array<object>} activeData
   * @param {object} instrument
   */
  initHistoricalChart(canvas, activeData, instrument) {
    if (!canvas || typeof Chart === 'undefined') return null;
    const ctx = canvas.getContext('2d');
    const themeColor = instrument?.themeColor || '#ff9800';

    const labels = activeData.map(d => d.date);
    const primaryData = activeData.map(d => d.close);
    const sec1Config = instrument?.secondarySeries?.[0];
    const sec2Config = instrument?.secondarySeries?.[1];

    const sec1Data = sec1Config ? activeData.map(d => sec1Config.getValue(d)) : [];
    const sec2Data = sec2Config ? activeData.map(d => sec2Config.getValue(d)) : [];

    const isOver50 = activeData && activeData.length > 50;
    const initNodeRadius = isOver50 ? 0 : 2;

    const datasets = [
      {
        label: `${instrument?.shortName || 'Asset'} (${instrument?.currency || 'USD'}/${instrument?.unit || 'unit'})`,
        data: primaryData,
        borderColor: this.currentStyle === 'candles' ? 'transparent' : themeColor,
        backgroundColor: this.currentStyle === 'caves' ? 'rgba(255, 152, 0, 0.15)' : 'transparent',
        borderWidth: 2,
        fill: this.currentStyle === 'caves',
        borderDash: [],
        stepped: false,
        tension: 0.1,
        pointRadius: this.currentStyle === 'candles' ? 0 : initNodeRadius,
        pointHoverRadius: 5,
        pointBackgroundColor: themeColor,
        yAxisID: 'y'
      }
    ];

    if (sec1Config) {
      datasets.push({
        label: `${sec1Config.label} (${sec1Config.unit})`,
        data: sec1Data,
        borderColor: sec1Config.color,
        backgroundColor: this.currentStyle === 'caves' ? 'rgba(56, 189, 248, 0.10)' : 'transparent',
        borderWidth: 1.8,
        fill: this.currentStyle === 'caves',
        borderDash: [],
        stepped: false,
        tension: 0.1,
        pointRadius: initNodeRadius,
        pointHoverRadius: 5,
        pointBackgroundColor: sec1Config.color,
        yAxisID: sec1Config.yAxisID || 'y1'
      });
    }

    if (sec2Config) {
      datasets.push({
        label: `${sec2Config.label} (${sec2Config.unit})`,
        data: sec2Data,
        borderColor: sec2Config.color,
        backgroundColor: this.currentStyle === 'caves' ? 'rgba(168, 85, 247, 0.10)' : 'transparent',
        borderWidth: 1.8,
        fill: this.currentStyle === 'caves',
        borderDash: [5, 4],
        stepped: false,
        tension: 0.1,
        pointRadius: initNodeRadius,
        pointHoverRadius: 5,
        pointBackgroundColor: sec2Config.color,
        yAxisID: sec2Config.yAxisID || 'y2'
      });
    }

    if (this.histChartInstance) {
      this.histChartInstance.destroy();
    }

    this.histChartInstance = new Chart(ctx, {
      type: 'line',
      plugins: [candlestickPlugin],
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 150 },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#12151b',
            titleColor: themeColor,
            titleFont: { family: 'JetBrains Mono', size: 11, weight: 'bold' },
            bodyFont: { family: 'JetBrains Mono', size: 11 },
            borderColor: '#2e3546',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {
              title: (items) => {
                const idx = items[0].dataIndex;
                const entry = activeData[idx];
                return `${entry.date} ${entry.note ? '• ' + entry.note : ''}`;
              },
              label: (item) => {
                const idx = item.dataIndex;
                const candle = activeData[idx];
                if (item.datasetIndex === 0) {
                  if (this.currentStyle === 'candles' && candle.open !== undefined) {
                    return [
                      ` ${instrument?.shortName || 'Asset'} OHLC:`,
                      `   Open:  $${candle.open.toFixed(1)}`,
                      `   High:  $${candle.high.toFixed(1)}`,
                      `   Low:   $${candle.low.toFixed(1)}`,
                      `   Close: $${candle.close.toFixed(1)}`
                    ];
                  }
                  return ` ${instrument?.shortName || 'Asset'} Close: $${item.parsed.y.toLocaleString()} USD/${instrument?.unit || 'unit'}`;
                } else if (item.datasetIndex === 1 && sec1Config) {
                  return ` ${sec1Config.label}: ${sec1Config.formatValue(item.parsed.y)}`;
                } else if (item.datasetIndex === 2 && sec2Config) {
                  return ` ${sec2Config.label}: ${sec2Config.formatValue(item.parsed.y)}`;
                }
              },
              afterBody: (items) => {
                if (instrument?.id === 'gold') {
                  const idx = items[0].dataIndex;
                  const entry = activeData[idx];
                  const derived = instrument.computeDerived(entry);
                  return [
                    ` ---------------------------`,
                    ` Gold in THB: ฿${Math.round(derived.gold_thb_oz).toLocaleString()} / oz`,
                    ` 1 Baht Gold Bar: ฿${Math.round(derived.thai_gold_bar).toLocaleString()} THB`
                  ];
                }
                return [];
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#181d26' },
            ticks: { color: '#828a99', font: { family: 'JetBrains Mono', size: 10 }, maxTicksLimit: 14 }
          },
          y: {
            type: 'linear', display: true, position: 'left', grid: { color: '#181d26' },
            title: { display: true, text: `${instrument?.shortName || 'Asset'} Price ($/${instrument?.unit || 'unit'})`, color: themeColor, font: { family: 'JetBrains Mono', weight: '700', size: 10 } },
            ticks: { color: themeColor, font: { family: 'JetBrains Mono', size: 10 }, callback: (v) => '$' + v.toLocaleString() }
          },
          y1: {
            type: 'linear', display: !!sec1Config, position: 'right', grid: { drawOnChartArea: false },
            title: { display: !!sec1Config, text: sec1Config ? `${sec1Config.label} (${sec1Config.unit})` : '', color: sec1Config?.color || '#38bdf8', font: { family: 'JetBrains Mono', weight: '700', size: 10 } },
            ticks: {
              color: sec1Config?.color || '#38bdf8',
              font: { family: 'JetBrains Mono', size: 10 },
              callback: function(v) {
                const range = (this.max || 40) - (this.min || 20);
                return (sec1Config?.unit === '฿' ? '฿' : '') + (range < 2 ? v.toFixed(2) : v.toFixed(1));
              }
            }
          },
          y2: {
            type: 'linear', display: !!sec2Config, position: 'right', grid: { drawOnChartArea: false },
            title: { display: !!sec2Config, text: sec2Config ? `${sec2Config.label} (${sec2Config.unit})` : '', color: sec2Config?.color || '#a855f7', font: { family: 'JetBrains Mono', weight: '700', size: 10 } },
            ticks: {
              color: sec2Config?.color || '#a855f7',
              font: { family: 'JetBrains Mono', size: 10 },
              callback: function(v) {
                const range = (this.max || 10) - (this.min || 0);
                return (range < 0.5 ? v.toFixed(2) : v.toFixed(1)) + (sec2Config?.unit === '%' ? '%' : '');
              }
            }
          }
        }
      }
    });

    this.histChartInstance.config._saacStyle = this.currentStyle;
    this.histChartInstance.config._saacActiveData = activeData;
    this.updateHistScales(activeData);

    return this.histChartInstance;
  }

  /**
   * Updates historical chart point radius according to the 50-node threshold.
   * @param {number} dataCount
   */
  updatePointRadii(dataCount) {
    if (!this.histChartInstance) return;
    const isOver50 = dataCount > 50;
    const nodeRadius = isOver50 ? 0 : 2;

    const ds0 = this.histChartInstance.data.datasets[0];
    const ds1 = this.histChartInstance.data.datasets[1];
    const ds2 = this.histChartInstance.data.datasets[2];

    if (ds0) ds0.pointRadius = this.currentStyle === 'candles' ? 0 : nodeRadius;
    if (ds1) ds1.pointRadius = nodeRadius;
    if (ds2) ds2.pointRadius = nodeRadius;
  }

  /**
   * Sets chart style to 'line', 'caves', or 'candles'.
   * @param {string} style
   * @param {string} [themeColor='#ff9800']
   */
  setStyle(style, themeColor = '#ff9800') {
    this.currentStyle = style;
    if (!this.histChartInstance) return;
    this.histChartInstance.config._saacStyle = style;

    const ds0 = this.histChartInstance.data.datasets[0];
    const ds1 = this.histChartInstance.data.datasets[1];
    const ds2 = this.histChartInstance.data.datasets[2];

    if (style === 'candles') {
      if (ds0) {
        ds0.borderColor = 'transparent';
        ds0.backgroundColor = 'transparent';
        ds0.fill = false;
        ds0.borderDash = [];
      }
      if (ds1) { ds1.fill = false; ds1.borderDash = []; }
      if (ds2) { ds2.fill = false; ds2.borderDash = [5, 4]; }
    } else if (style === 'caves') {
      if (ds0) {
        ds0.borderColor = themeColor;
        ds0.backgroundColor = 'rgba(255, 152, 0, 0.15)';
        ds0.fill = true;
        ds0.borderDash = [];
      }
      if (ds1) {
        ds1.backgroundColor = 'rgba(56, 189, 248, 0.10)';
        ds1.fill = true;
        ds1.borderDash = [];
      }
      if (ds2) {
        ds2.backgroundColor = 'rgba(168, 85, 247, 0.10)';
        ds2.fill = true;
        ds2.borderDash = [5, 4];
      }
    } else if (style === 'line') {
      if (ds0) {
        ds0.borderColor = themeColor;
        ds0.backgroundColor = 'transparent';
        ds0.fill = false;
        ds0.borderDash = [];
      }
      if (ds1) {
        ds1.backgroundColor = 'transparent';
        ds1.fill = false;
        ds1.borderDash = [];
      }
      if (ds2) {
        ds2.backgroundColor = 'transparent';
        ds2.fill = false;
        ds2.borderDash = [5, 4];
      }
    }

    const dataCount = this.histChartInstance.data.labels?.length || 0;
    this.updatePointRadii(dataCount);
    this.histChartInstance.update();
  }

  /**
   * Recalculates dynamic scale padding for the active series.
   * @param {Array<object>} activeData
   */
  updateHistScales(activeData) {
    if (!this.histChartInstance || !activeData || !activeData.length) return;

    // Primary Scale
    const allLows = activeData.map(d => d.low !== undefined ? d.low : d.close);
    const allHighs = activeData.map(d => d.high !== undefined ? d.high : d.close);
    const minP = Math.min(...allLows);
    const maxP = Math.max(...allHighs);
    const padP = Math.max(1, (maxP - minP) * 0.06);

    this.histChartInstance.options.scales.y.type = this.currentScaleType;
    this.histChartInstance.options.scales.y.min = Math.max(0.1, Math.floor(minP - padP));
    this.histChartInstance.options.scales.y.max = Math.ceil(maxP + padP);

    // Secondary y1 Scale
    if (this.histChartInstance.options.scales.y1?.display) {
      const all1 = activeData.map(d => d.usd_thb !== undefined ? d.usd_thb : (d.qqq || d.spy || d.eth || 0));
      const min1 = Math.min(...all1);
      const max1 = Math.max(...all1);
      const pad1 = Math.max(0.15, (max1 - min1) * 0.12);
      this.histChartInstance.options.scales.y1.min = Math.floor((min1 - pad1) * 10) / 10;
      this.histChartInstance.options.scales.y1.max = Math.ceil((max1 + pad1) * 10) / 10;
    }

    // Secondary y2 Scale
    if (this.histChartInstance.options.scales.y2?.display) {
      const all2 = activeData.map(d => d.us10y !== undefined ? d.us10y : (d.vix || 0));
      const min2 = Math.min(...all2);
      const max2 = Math.max(...all2);
      const pad2 = Math.max(0.10, (max2 - min2) * 0.12);
      this.histChartInstance.options.scales.y2.min = Math.floor((min2 - pad2) * 10) / 10;
      this.histChartInstance.options.scales.y2.max = Math.ceil((max2 + pad2) * 10) / 10;
    }
  }

  /**
   * Toggles visibility of a dataset by index.
   * @param {number} index
   * @returns {boolean} - New hidden state
   */
  toggleDataset(index) {
    if (!this.histChartInstance) return false;
    const meta = this.histChartInstance.getDatasetMeta(index);
    if (!meta) return false;
    meta.hidden = !meta.hidden;
    this.histChartInstance.update();
    return meta.hidden;
  }
}

export const chartEngine = new ChartEngine();

if (typeof window !== 'undefined') {
  window.ChartEngine = ChartEngine;
  window.chartEngine = chartEngine;
  window.candlestickPlugin = candlestickPlugin;
}
