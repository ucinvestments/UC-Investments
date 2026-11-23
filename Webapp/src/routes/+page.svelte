<script lang="ts">
  import { onMount, tick } from "svelte";
  import posthog from "posthog-js";
  import FundDisclosures from "$lib/explorer/FundDisclosures.svelte";
  import HoldingsChart from "$lib/explorer/HoldingsChart.svelte";
  import {
    formatCompact,
    formatDollars,
    formatShare,
    formatSourceDate,
    loadSnapshot,
    sumHoldings,
    views,
  } from "$lib/explorer/holdings";
  import type { Holding, HoldingsSnapshot, View } from "$lib/explorer/holdings";
  import "$lib/explorer/explorer.css";

  const order: View[] = ["company", "fund", "asset", "reported"];
  const pageSize = 12;

  let view: View = $state("company");
  let consolidate = $state(true);
  let snapshot = $state.raw<HoldingsSnapshot>();
  let search = $state("");
  let page = $state(0);
  let selection = $state.raw<Holding>();
  let loading = $state(false);
  let failed = $state(false);
  let detailHeading = $state<HTMLHeadingElement>();
  let searchInput: HTMLInputElement;

  const rows = $derived.by(() => {
    if (!snapshot) return [];
    switch (view) {
      case "company":
        return snapshot.companies[consolidate ? "grouped" : "separate"];
      case "fund":
        return snapshot.funds;
      case "asset":
        return snapshot.assetClasses;
      case "reported":
        return snapshot.reported;
    }
  });
  const coverage = $derived(snapshot?.coverage);
  const sharedDisclosureDate = $derived(
    snapshot && snapshot.disclosures.ucrp.date === snapshot.disclosures.gep.date
      ? snapshot.disclosures.ucrp.date
      : undefined,
  );
  const query = $derived(search.trim().toLowerCase());
  const matches = $derived(
    rows.filter((row) => row.name.toLowerCase().includes(query)),
  );
  const selected = $derived(
    selection ??
      matches.find((row) => row.name.toLowerCase() === query) ??
      matches[0],
  );
  const visible = $derived(
    matches.slice(page * pageSize, (page + 1) * pageSize),
  );
  const viewTotal = $derived(sumHoldings(rows));
  const assignedShare = $derived(
    coverage && coverage.total > 0 ? coverage.assigned / coverage.total : 0,
  );

  async function refreshView() {
    if (loading || snapshot) return;
    loading = true;
    failed = false;
    try {
      snapshot = await loadSnapshot();
    } catch {
      failed = true;
    } finally {
      loading = false;
    }
  }

  function changeView(next: View, query = "") {
    const previous = view;
    view = next;
    updateSearch(query);
    if (previous !== next) {
      posthog.capture("view_mode_changed", {
        previous_mode: previous,
        new_mode: next,
      });
    }
  }

  async function openFund(name: string) {
    changeView("fund", name);
    await tick();
    searchInput.focus();
  }

  function clearSearch() {
    updateSearch("");
    searchInput.focus();
  }

  function turnPage(offset: number) {
    page += offset;
    selection = visible[0];
  }

  function updateSearch(value: string) {
    search = value;
    selection = undefined;
    page = 0;
  }

  function toggleShares() {
    consolidate = !consolidate;
    page = 0;
    selection = undefined;
    posthog.capture("composition_toggled", {
      view_mode: view,
      consolidate_shares: consolidate,
    });
  }

  async function selectHolding(row: Holding) {
    selection = row;
    page = Math.floor(matches.indexOf(row) / pageSize);
    if (window.matchMedia("(max-width: 900px)").matches) {
      await tick();
      detailHeading?.focus();
    }
  }

  onMount(() => {
    void refreshView();
  });
</script>

<svelte:head>
  <title>UC Investment Explorer</title>
  <meta
    name="description"
    content="Explore University of California pension and endowment disclosures by company, fund, and asset class."
  />
</svelte:head>

<div class="investment-explorer">
  <section class="coverage-hero" aria-labelledby="explorer-title">
    <div class="explorer-frame coverage-layout">
      <div class="coverage-intro">
        <div class="snapshot">
          <span></span>
          {sharedDisclosureDate
            ? `UC holdings as of ${formatSourceDate(sharedDisclosureDate)}`
            : "UC holdings disclosures"}
        </div>
        <h1 id="explorer-title">
          UC Investment<br class="desktop-break" /> Explorer
        </h1>
        <p>
          Follow the University of California’s pension and endowment
          investments from disclosed funds to estimated company exposure.
        </p>
        <a href="/about"
          >Read the methodology <span aria-hidden="true">↗</span></a
        >
      </div>

      <div class="coverage-panel" aria-live="polite">
        <div class="coverage-meta">
          <h2>Disclosure coverage</h2>
          <span>UCRP + GEP</span>
        </div>
        {#if coverage}
          <div class="coverage-total">{formatCompact(coverage.total)}</div>
          <p>Listed pension and endowment holdings</p>
          <div class="coverage-bar" aria-hidden="true">
            <div
              style:width={`${Math.min(1, Math.max(0, assignedShare)) * 100}%`}
            ></div>
          </div>
          <div class="coverage-key">
            <div>
              <strong>{formatCompact(coverage.assigned)}</strong><span
                ><i></i>Mapped to companies using estimates</span
              >
            </div>
            <div>
              <strong
                >{formatCompact(coverage.total - coverage.assigned)}</strong
              ><span><i></i>Without a company breakdown</span>
            </div>
          </div>
        {:else if failed}
          <p class="coverage-status">
            Coverage totals are unavailable. <button onclick={refreshView}
              >Try again</button
            >
          </p>
        {:else}
          <p class="coverage-status">Loading coverage totals…</p>
        {/if}
      </div>
    </div>
  </section>

  <section
    class="explorer-frame holdings-section"
    aria-labelledby="holdings-title"
  >
    <header class="holdings-header">
      <div>
        <h2 id="holdings-title">Explore holdings</h2>
        <p>{views[view].description}</p>
      </div>
      <div class="view-switch" role="group" aria-label="Holdings view">
        {#each order as mode (mode)}
          <button aria-pressed={view === mode} onclick={() => changeView(mode)}
            >{views[mode].label}</button
          >
        {/each}
      </div>
    </header>

    <div class="holdings-grid">
      {#if selected && !loading}
        <HoldingsChart
          holdings={matches}
          {selected}
          filtered={Boolean(query)}
          estimated={view === "company"}
          onselect={selectHolding}
        />
      {/if}
      <div class="holdings-panel" aria-busy={loading}>
        <div class="explorer-tools">
          <div class="holdings-search">
            <span class="search-mark" aria-hidden="true"></span>
            <input
              type="search"
              aria-label={`Search ${views[view].label.toLowerCase()}`}
              placeholder={`Search ${views[view].label.toLowerCase()}`}
              bind:this={searchInput}
              value={search}
              oninput={(event) => updateSearch(event.currentTarget.value)}
            />
            {#if search}<button aria-label="Clear search" onclick={clearSearch}
                >×</button
              >{/if}
          </div>
          {#if view === "company"}
            <label class="share-setting"
              ><input
                type="checkbox"
                checked={consolidate}
                onchange={toggleShares}
              /> Group share classes</label
            >
          {/if}
        </div>

        {#if loading || (!snapshot && !failed)}
          <p class="explorer-status" role="status">
            Loading {views[view].label.toLowerCase()}…
          </p>
        {:else if failed}
          <div class="explorer-status" role="status">
            <p>Couldn’t load this view.</p>
            <button onclick={refreshView}>Try again</button>
          </div>
        {:else if matches.length === 0}
          <div class="explorer-status" role="status">
            {#if search}<p>No matches for “{search}”.</p>
              <button onclick={clearSearch}>Clear search</button>
            {:else}<p>No holdings are available for this view.</p>{/if}
          </div>
        {:else}
          <table class="holdings-table">
            <thead
              ><tr
                ><th scope="col">{views[view].singular}</th><th scope="col"
                  >{view === "company"
                    ? "Estimated exposure"
                    : view === "reported"
                      ? "Reported value"
                      : "Market value"}</th
                ><th scope="col">Share</th></tr
              ></thead
            >
            <tbody>
              {#each visible as row, index (row)}
                <tr class:current={selected === row}>
                  <td>
                    <button
                      class="holding-name"
                      aria-pressed={selected === row}
                      onclick={() => selectHolding(row)}
                    >
                      <span class="holding-rank" aria-hidden="true"
                        >{page * pageSize + index + 1}</span
                      ><span>{row.name}</span>
                    </button>
                  </td>
                  <td
                    title={row.basis === "estimate"
                      ? undefined
                      : formatDollars(row.amount)}
                    >{formatCompact(row.amount)}</td
                  >
                  <td
                    ><div class="share-cell">
                      <span class="share-track" aria-hidden="true"
                        ><i
                          style:width={`${Math.max(0, (row.amount / (viewTotal || 1)) * 100)}%`}
                        ></i></span
                      >
                      <span>{formatShare(row.amount, viewTotal)}</span>
                    </div></td
                  >
                </tr>
              {/each}
            </tbody>
          </table>
          <div class="holdings-pagination">
            <span aria-live="polite"
              >{page * pageSize + 1}–{Math.min(
                (page + 1) * pageSize,
                matches.length,
              )} of {matches.length.toLocaleString("en-US")}</span
            >
            {#if matches.length > pageSize}
              <div>
                <button disabled={page === 0} onclick={() => turnPage(-1)}
                  >Previous</button
                >
                <button
                  disabled={(page + 1) * pageSize >= matches.length}
                  onclick={() => turnPage(1)}>Next</button
                >
              </div>
            {/if}
          </div>
        {/if}
      </div>

      {#if selected && !loading}
        <aside class="holding-detail" aria-labelledby="holding-detail-name">
          <div class="detail-kicker">
            {view === "company"
              ? "Estimated company exposure"
              : view === "reported"
                ? "Reported by the UC Regents"
                : view === "fund"
                  ? "Fund allocation"
                  : "Asset class allocation"}
          </div>
          <h3 id="holding-detail-name" tabindex="-1" bind:this={detailHeading}>
            {selected.name}
          </h3>
          <div
            class="detail-amount"
            title={selected.basis === "estimate"
              ? undefined
              : formatDollars(selected.amount)}
          >
            {formatCompact(selected.amount)}
          </div>
          <p class="detail-share">
            {#if selected.basis !== "estimate"}{formatDollars(selected.amount)} ·
            {/if}{formatShare(selected.amount, viewTotal)} of {view ===
            "company"
              ? "estimated exposure"
              : view === "reported"
                ? "reported 13F value"
                : "listed holdings"}
          </p>

          {#if selected.category}<p class="detail-category">
              {selected.category}
            </p>{/if}

          {#if selected.funds}
            <h4>Funds in this class <span>{selected.funds.length}</span></h4>
            <ul class="detail-list">
              {#each selected.funds as fund}
                <li>
                  <button onclick={() => openFund(fund)}
                    >{fund} <span aria-hidden="true">↗</span></button
                  >
                </li>
              {/each}
            </ul>
          {:else if selected.allocations.length}
            <h4>
              {view === "company" ? "Contributing funds" : "Source pools"}
            </h4>
            <ul class="detail-list">
              {#each selected.allocations as allocation (allocation.name)}
                {@const proxy =
                  allocation.source && snapshot?.proxies[allocation.source]}
                {@const disclosure =
                  snapshot?.disclosures[allocation.name.toLowerCase()]}
                <li>
                  {#if proxy}
                    <div>
                      <button onclick={() => openFund(allocation.name)}
                        >{allocation.name}
                        <span aria-hidden="true">↗</span></button
                      >
                      <a class="allocation-source" href={proxy.url}>
                        {proxy.method} · {formatSourceDate(proxy.date)}
                        <span>{proxy.name}</span>
                      </a>
                    </div>
                  {:else if disclosure}
                    <a class="allocation-source" href={disclosure.url}>
                      {disclosure.name} · {formatSourceDate(disclosure.date)}
                    </a>
                  {:else}
                    <span>{allocation.name}</span>
                  {/if}
                  <strong
                    title={proxy ? undefined : formatDollars(allocation.amount)}
                    >{formatCompact(allocation.amount)}</strong
                  >
                </li>
              {/each}
            </ul>
          {/if}
          {#if selected.disclosures && snapshot?.privateMarkets}
            <FundDisclosures
              disclosures={selected.disclosures}
              sources={snapshot.privateMarkets}
            />
          {/if}
          {#if selected.basis === "estimate"}
            <p class="detail-note">
              We apply weights from the sources above to UC’s reported fund
              allocations. Proxy holdings can differ from the UC funds. <a
                href="/about">How estimates work</a
              >
            </p>
          {:else if selected.basis === "reported" && snapshot}
            <p class="detail-note">
              <a href={snapshot.regents.url}>Regents Form 13F</a> for {formatSourceDate(
                snapshot.regents.date,
              )}, filed {formatSourceDate(snapshot.regents.filed)}.
            </p>
          {/if}
          {#if selected.lookThrough && snapshot}
            {@const etf = selected.lookThrough}
            <h4>{etf.ticker} ETF holdings</h4>
            <a class="allocation-source" href={etf.url}
              >State Street workbook · {formatSourceDate(etf.date)}</a
            >
            {#if etf.estimates}
              <details class="look-through">
                <summary>Estimated indirect company exposure</summary>
                <p>
                  Estimate based on the ETF equity weights and Regents position
                  dated {formatSourceDate(snapshot.regents.date)}.
                </p>
                <ul class="detail-list">
                  {#each etf.estimates as holding}
                    <li>
                      <span>{holding.name} · {holding.ticker}</span><strong
                        >{formatCompact(holding.amount)}</strong
                      >
                    </li>
                  {/each}
                </ul>
              </details>
            {:else}
              <p class="detail-note">
                Company estimates require an ETF holdings file dated {formatSourceDate(
                  snapshot.regents.date,
                )} to match the Regents position.
              </p>
            {/if}
          {/if}
        </aside>
      {/if}
    </div>
    {#if snapshot}
      <div class="source-line">
        <h3>Source dates</h3>
        <ul>
          {#each Object.values(snapshot.disclosures) as source (source.name)}
            <li>
              <a href={source.url}>{source.name} holdings</a> as of {formatSourceDate(
                source.date,
              )}
            </li>
          {/each}
          {#each Object.values(snapshot.privateMarkets ?? {}) as source (source.name)}
            <li>
              <a href={source.url}>{source.name}</a> as of {formatSourceDate(
                source.date,
              )}
            </li>
          {/each}
          <li>
            <a href={snapshot.regents.url}>Regents Form 13F</a> as of {formatSourceDate(
              snapshot.regents.date,
            )}
          </li>
        </ul>
        <p>
          Sources checked {formatSourceDate(snapshot.checkedAt)}.
          <a href="/resources">More sources</a>
        </p>
      </div>
    {/if}
  </section>
</div>
