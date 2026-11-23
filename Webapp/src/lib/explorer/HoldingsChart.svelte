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
    "#264cbe",
    "#5c7ee4",
    "#147d8d",
    "#cb7a29",
    "#795dbb",
    "#3d8c5f",
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
              color: "#b4c2dd",
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
    <div class="chart-body">
      <div class="chart-donut">
        <svg viewBox="0 0 160 160" aria-hidden="true">
          {#each segments as segment}
            {@const holding = segment.holding}
            <!-- svelte-ignore a11y_no_static_element_interactions (The chart key provides keyboard access to the same selections.) -->
            <circle
              cx="80"
              cy="80"
              r="62"
              pathLength="100"
              fill="none"
              stroke={segment.color}
              stroke-dasharray={`${segment.share} ${100 - segment.share}`}
              stroke-dashoffset={-segment.offset}
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
        <div
          class="chart-total"
          title={estimated ? undefined : formatDollars(total)}
        >
          <strong>{formatCompact(total)}</strong>
          <span
            >{omittedNegative
              ? "Positive total"
              : filtered
                ? "Matches"
                : estimated
                  ? "Estimated total"
                  : "Chart total"}</span
          >
        </div>
      </div>

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
    </div>
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
    padding: clamp(16px, 2vw, 24px);
    background: #fff;
    border: 1px solid var(--rule);
    border-radius: 13px;
  }

  h3 {
    font: 650 1.18rem/1.25 var(--display);
    letter-spacing: -0.035em;
  }

  .chart-body {
    display: grid;
    grid-template-columns: minmax(100px, 0.85fr) minmax(0, 1fr);
    align-items: center;
    gap: 10px;
    margin-top: 12px;
  }

  .chart-donut {
    position: relative;
    width: min(100%, 175px);
    margin-inline: auto;
  }

  svg {
    width: 100%;
  }
  circle {
    stroke-width: 23;
  }
  circle.selectable {
    cursor: pointer;
  }
  circle.chosen,
  circle.selectable:hover {
    stroke-width: 29;
  }

  .chart-total {
    position: absolute;
    inset: 0;
    display: grid;
    align-content: center;
    text-align: center;
    pointer-events: none;
  }

  .chart-total strong {
    font: 650 clamp(1rem, 1.65vw, 1.45rem)/1.2 var(--display);
    letter-spacing: -0.05em;
  }

  .chart-total span,
  .chart-note {
    color: var(--muted);
    font-size: 0.72rem;
  }

  .chart-key {
    list-style: none;
    min-width: 0;
  }

  .chart-key button,
  .chart-other {
    display: grid;
    grid-template-columns: 8px minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 6px;
    width: 100%;
    min-height: 30px;
    padding: 5px;
    border-radius: 4px;
    color: var(--ink);
    font-size: 0.74rem;
    line-height: 1.35;
    text-align: left;
  }

  .chart-key button {
    cursor: pointer;
  }
  .chart-key button:hover,
  .chart-key button[aria-pressed="true"] {
    background: #eaf0ff;
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
  }

  @media (min-width: 901px) {
    .holdings-chart {
      grid-column: 2;
      grid-row: 1;
    }
  }

  @media (max-width: 900px) {
    .chart-body {
      grid-template-columns: minmax(105px, 175px) minmax(0, 240px);
      justify-content: center;
      gap: 10px 20px;
    }

    .chart-key button,
    .chart-other {
      min-height: 34px;
    }
  }
</style>
