<script lang="ts">
  import dataset from "../../../static/data/campus-endowments.json";
  import {
    formatCompact,
    formatDollars,
    formatSourceDate,
  } from "$lib/explorer/holdings";
  import "$lib/explorer/explorer.css";

  type Campus = (typeof dataset.campuses)[number];
  type MarketValues =
    Campus["market_value_usd"][keyof Campus["market_value_usd"]];
  const currentDate = dataset.as_of as keyof Campus["market_value_usd"];
  const priorDate = (
    Object.keys(
      dataset.campuses[0].market_value_usd,
    ) as (keyof Campus["market_value_usd"])[]
  ).find((date) => date !== currentDate);
  const labels = {
    regents: "Regents-designated assets",
    foundation_gep: "Foundation assets in GEP",
    foundation_bgp: "Foundation assets in Blue & Gold Pool",
    foundation_stip: "Foundation assets in STIP",
    foundation_other: "Other foundation assets",
  } satisfies Partial<Record<keyof MarketValues, string>>;
  const allocationLabels = {
    us_equity: "U.S. equity",
    non_us_equity: "Non-U.S. equity",
    global_equity: "Global equity",
    us_fixed_income: "U.S. fixed income",
    non_us_fixed_income: "Non-U.S. fixed income",
    absolute_return: "Absolute return",
    real_assets: "Real assets",
    real_estate: "Real estate",
    private_equity: "Private equity",
    private_credit: "Private credit",
    other: "Other",
    cash_equivalents: "Cash and equivalents",
  } satisfies Record<keyof Campus["foundation_allocation_percent"], string>;
  const marketFields = Object.entries(labels) as [
    keyof typeof labels,
    string,
  ][];
  const allocationFields = Object.entries(allocationLabels) as [
    keyof typeof allocationLabels,
    string,
  ][];
  const combined = dataset.campuses.reduce(
    (sum, campus) => sum + campus.market_value_usd[currentDate].total,
    0,
  );

  let selectedName = $state(dataset.campuses[0].campus);
  const selected = $derived(
    dataset.campuses.find((campus) => campus.campus === selectedName) ??
      dataset.campuses[0],
  );
  const market = $derived(selected.market_value_usd[currentDate]);

  const formatPercent = (value: number) =>
    `${value.toLocaleString("en-US", { maximumFractionDigits: 1 })}%`;
</script>

<svelte:head>
  <title>Campus endowments | UC Investment Explorer</title>
  <meta
    name="description"
    content="Compare endowment market values and foundation asset allocations across the ten UC campuses."
  />
</svelte:head>

<div class="investment-explorer">
  <section class="coverage-hero" aria-labelledby="campus-title">
    <div class="explorer-frame coverage-layout">
      <div class="coverage-intro">
        <div class="snapshot">
          <span></span> As of {formatSourceDate(dataset.as_of)}
        </div>
        <h1 id="campus-title">Campus endowments</h1>
        <p>
          Explore endowment values and foundation portfolios across UC’s ten
          campuses.
        </p>
        <a href={dataset.source_url}>Read the UC annual endowment report</a>
      </div>
      <div class="coverage-panel">
        <div class="coverage-meta"><h2>Campus endowment market value</h2></div>
        <div class="coverage-total">{formatCompact(combined)}</div>
        <p>Regents-designated and foundation assets across all 10 campuses</p>
      </div>
    </div>
  </section>

  <section
    class="explorer-frame holdings-section"
    aria-labelledby="campus-details"
  >
    <header class="holdings-header">
      <div>
        <h2 id="campus-details">Explore by campus</h2>
        <p>Select a campus to see its endowment and foundation portfolio.</p>
      </div>
      <label class="campus-picker"
        >Campus
        <select bind:value={selectedName}>
          {#each dataset.campuses as campus (campus.campus)}
            <option value={campus.campus}>UC {campus.campus}</option>
          {/each}
        </select>
      </label>
    </header>

    <div class="campus-columns">
      <section class="campus-card" aria-labelledby="market-value">
        <h3 id="market-value">UC {selected.campus} market value</h3>
        <table>
          <thead
            ><tr
              ><th scope="col">Assets</th><th scope="col"
                >{formatSourceDate(currentDate)}</th
              >{#if priorDate}<th scope="col">{formatSourceDate(priorDate)}</th
                >{/if}</tr
            ></thead
          >
          <tbody>
            {#each marketFields as [key, label] (key)}
              <tr>
                <th scope="row">{label}</th>
                <td>{formatDollars(market[key])}</td>
                {#if priorDate}<td
                    >{formatDollars(
                      selected.market_value_usd[priorDate][key],
                    )}</td
                  >{/if}
              </tr>
            {/each}
          </tbody>
          <tfoot>
            <tr
              ><th scope="row">Total</th><td>{formatDollars(market.total)}</td>
              {#if priorDate}<td
                  >{formatDollars(
                    selected.market_value_usd[priorDate].total,
                  )}</td
                >{/if}
            </tr>
          </tfoot>
        </table>
        <a
          href={`${dataset.source_url}#page=${dataset.pdf_pages.market_values}`}
          >Market values in the annual report</a
        >
      </section>

      <section class="campus-card" aria-labelledby="allocation">
        <h3 id="allocation">Foundation allocation</h3>
        <dl class="allocation-list">
          {#each allocationFields as [key, label] (key)}
            {@const value = selected.foundation_allocation_percent[key]}
            <div>
              <dt>{label}</dt>
              <dd>
                <span aria-hidden="true" class="allocation-track"
                  ><i style:width={`${value}%`}></i></span
                >
                {formatPercent(value)}
              </dd>
            </div>
          {/each}
        </dl>
        <dl class="campus-performance">
          <div>
            <dt>One-year net return</dt>
            <dd>{formatPercent(selected.foundation_return_percent)}</dd>
          </div>
          <div>
            <dt>Fiscal-year volatility</dt>
            <dd>{formatPercent(selected.foundation_volatility_percent)}</dd>
          </div>
        </dl>
        <a
          href={`${dataset.source_url}#page=${dataset.pdf_pages.foundation_allocations}`}
          >Foundation allocations in the annual report</a
        >
      </section>
    </div>

    <p class="source-line">
      {dataset.scope}
      <a href="/data/campus-endowments.json" download>Download JSON</a>
    </p>
  </section>
</div>

<style>
  .campus-picker {
    display: grid;
    gap: 4px;
    color: var(--muted);
    font-size: 0.85rem;
  }
  .campus-picker select {
    min-width: 210px;
    min-height: 44px;
    padding: 6px 10px;
    color: var(--ink);
    border: 1px solid #bdcbe2;
    border-radius: 6px;
    background: white;
  }
  .campus-picker select:focus-visible {
    outline: 2px solid var(--blue);
    outline-offset: 2px;
  }
  .campus-columns {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 18px;
    align-items: start;
  }
  .campus-card {
    min-width: 0;
    background: white;
    border: 1px solid var(--rule);
    border-radius: 13px;
    padding: clamp(13px, 2vw, 24px);
  }
  .campus-card h3 {
    font: 650 1.3rem/1.2 var(--display);
    margin-bottom: 14px;
  }
  .campus-card table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
  }
  .campus-card th,
  .campus-card td {
    padding: 8px 4px;
    border-bottom: 1px solid var(--rule);
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  .campus-card th[scope="row"],
  .campus-card th:first-child {
    text-align: left;
  }
  .campus-card tbody th {
    font-weight: 500;
  }
  .campus-card tfoot {
    font-weight: 650;
  }
  .campus-card a {
    display: inline-block;
    margin-top: 12px;
    color: #2348a9;
    font-size: 0.8rem;
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  .allocation-list > div,
  .campus-performance > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
    padding: 5px 0;
    border-bottom: 1px solid var(--rule);
    font-size: 0.85rem;
  }
  .allocation-list dd {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    width: max(33%, 100px);
  }
  .allocation-track {
    flex: 1;
    max-width: 75px;
    height: 5px;
    border-radius: 3px;
    overflow: hidden;
    background: #dce6f8;
  }
  .allocation-track i {
    display: block;
    height: 100%;
    background: var(--blue);
  }
  .campus-performance {
    margin-top: 12px;
  }
  .campus-performance dd {
    font-weight: 650;
  }
  @media (max-width: 900px) {
    .campus-columns {
      grid-template-columns: 1fr;
    }
  }
  @media (max-width: 480px) {
    .campus-card table {
      font-size: 0.72rem;
    }
    .campus-card th,
    .campus-card td {
      padding-inline: 2px;
    }
  }
</style>
