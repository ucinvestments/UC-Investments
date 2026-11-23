<script lang="ts">
  import {
    formatCompact,
    formatDollars,
    formatShare,
    sumHoldings,
  } from "./holdings";
  import type { Holding } from "./holdings";

  let {
    holdings,
    selected,
    filtered,
    estimated,
    onselect,
  }: {
    holdings: Holding[];
    selected?: Holding;
    filtered: boolean;
    estimated: boolean;
    onselect: (holding: Holding) => void;
  } = $props();

  const colors = [
    "#3b7ea1",
    "#fdb515",
    "#003262",
    "#c4820e",
    "#00b0da",
    "#00a598",
    "#859438",
    "#ed4e33",
    "#d9661f",
    "#ee1f60",
    "#46535e",
    "#6c3302",
    "#cfdd45",
    "#b9d3b6",
    "#ddd5c7",
    "#8b4513",
    "#2e8b57",
    "#4682b4",
    "#cd853f",
    "#ff6347",
    "#4169e1",
    "#32cd32",
    "#ffd700",
    "#ff69b4",
  ];

  const positive = $derived(holdings.filter((holding) => holding.amount > 0));
  const total = $derived(sumHoldings(positive));
  const omittedNegative = $derived(
    holdings.some((holding) => holding.amount < 0),
  );

  const segments = $derived.by(() => {
    const largest = positive.slice(0, colors.length);
    const other = positive.slice(colors.length);
    let offset = 0;
    return [
      ...largest.map((holding, index) => ({
        holding,
        name: holding.name,
        amount: holding.amount,
        color: colors[index],
      })),
      ...(other.length
        ? [
            {
              holding: undefined,
              name: `Other (${other.length.toLocaleString("en-US")})`,
              amount: sumHoldings(other),
              color: "#8b8b8b",
            },
          ]
        : []),
    ].map((segment) => {
      const share = (segment.amount / total) * 100;
      const slice = { ...segment, share, offset };
      offset += share;
      return slice;
    });
  });
</script>

<section class="holdings-chart" aria-labelledby="distribution-title">
  <h3 id="distribution-title">
    {filtered
      ? estimated
        ? "Estimated exposure for matches"
        : "Distribution of matches"
      : estimated
        ? "Estimated exposure distribution"
        : "Holdings distribution"}
  </h3>
  {#if total > 0}
    <div
      class="chart-total"
      title={estimated ? undefined : formatDollars(total)}
    >
      {formatCompact(total)}
    </div>
    <div class="chart-body">
      <div class="chart-donut">
        <svg viewBox="0 0 160 160" aria-hidden="true">
          {#each segments as segment}
            {@const holding = segment.holding}
            {@const gap =
              segments.length > 1 ? Math.min(0.32, segment.share * 0.22) : 0}
            <!-- svelte-ignore a11y_no_static_element_interactions (The chart key provides keyboard access to the same selections.) -->
            <circle
              cx="80"
              cy="80"
              r="62"
              pathLength="100"
              fill="none"
              stroke={segment.color}
              stroke-dasharray={`${segment.share - gap} ${100 - segment.share + gap}`}
              stroke-dashoffset={-segment.offset - gap / 2}
              transform="rotate(-90 80 80)"
              class:selectable={holding}
              class:chosen={holding && holding === selected}
              onpointerup={holding
                ? (event) => {
                    if (event.button === 0) onselect(holding);
                  }
                : undefined}
            >
              <title
                >{segment.name} · {formatShare(segment.amount, total)}</title
              >
            </circle>
          {/each}
        </svg>
        {#if selected}
          <div class="chart-current">
            <span>{selected.name}</span>
            <strong>{formatCompact(selected.amount)}</strong>
            {#if selected.amount > 0}<span
                >{formatShare(selected.amount, total)}</span
              >{/if}
          </div>
        {/if}
      </div>
    </div>
    <details class="chart-breakdown">
      <summary>Chart breakdown</summary>
      <ul class="chart-key" aria-label="Chart breakdown">
        {#each segments as segment}
          {@const holding = segment.holding}
          <li style:--slice={segment.color}>
            {#if holding}
              <button
                aria-pressed={holding === selected}
                onclick={() => onselect(holding)}
              >
                <span class="chart-swatch" aria-hidden="true"></span>
                <span class="chart-label">{segment.name}</span>
                <span class="chart-share"
                  >{formatShare(segment.amount, total)}</span
                >
              </button>
            {:else}
              <div class="chart-other">
                <span class="chart-swatch" aria-hidden="true"></span>
                <span class="chart-label">{segment.name}</span>
                <span class="chart-share"
                  >{formatShare(segment.amount, total)}</span
                >
              </div>
            {/if}
          </li>
        {/each}
      </ul>
    </details>
    {#if omittedNegative}
      <p class="chart-note">
        The chart shows positive amounts only. The table includes negative
        entries.
      </p>
    {/if}
  {:else}
    <p class="chart-note">There are no positive amounts to chart.</p>
  {/if}
</section>

<style>
  .holdings-chart {
    min-width: 0;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--border);
    border-radius: 1rem;
    box-shadow: var(--shadow-md);
    text-align: center;
  }

  h3 {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 650;
  }

  .chart-total {
    margin-top: 4px;
    color: var(--pri);
    font: 700 1.75rem/1.25 var(--display);
  }

  .chart-body {
    display: grid;
    place-items: center;
    margin: 6px auto 2px;
  }

  .chart-donut {
    position: relative;
    width: min(100%, 380px);
  }

  svg {
    width: 100%;
  }
  circle {
    stroke-width: 25;
  }
  circle.selectable {
    cursor: pointer;
  }
  circle.chosen,
  circle.selectable:hover {
    stroke-width: 28;
  }

  .chart-current {
    position: absolute;
    inset: 0;
    display: grid;
    align-content: center;
    width: 48%;
    margin-inline: auto;
    gap: 3px;
    color: var(--pri);
    font-size: 0.85rem;
    font-weight: 650;
    line-height: 1.3;
    overflow-wrap: anywhere;
    pointer-events: none;
  }

  .chart-current strong {
    margin-top: 3px;
    color: var(--founder);
    font: 700 1.3rem/1.2 var(--display);
  }

  .chart-current span:last-child {
    color: var(--text-secondary);
  }

  .chart-breakdown summary {
    margin-inline: auto;
    width: fit-content;
    color: var(--pri);
    cursor: pointer;
    font-size: 0.82rem;
  }

  .chart-key {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 2px 8px;
    margin-top: 10px;
  }

  .chart-key button,
  .chart-other {
    display: grid;
    grid-template-columns: 8px minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 6px;
    width: 100%;
    min-height: 36px;
    padding: 5px;
    border-radius: 4px;
    color: var(--ink);
    font-size: 0.76rem;
    line-height: 1.35;
    text-align: left;
  }

  .chart-key button {
    cursor: pointer;
  }
  .chart-key button:hover,
  .chart-key button[aria-pressed="true"] {
    background: var(--bg-secondary);
  }
  .chart-swatch {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--slice);
  }
  .chart-label {
    overflow-wrap: anywhere;
  }
  .chart-share {
    color: var(--muted);
    font-variant-numeric: tabular-nums;
  }
  .chart-note {
    margin-top: 10px;
    color: var(--muted);
    font-size: 0.75rem;
  }

  @media (max-width: 620px) {
    .chart-current {
      font-size: 0.75rem;
    }
    .chart-key {
      grid-template-columns: 1fr;
    }
  }
</style>
