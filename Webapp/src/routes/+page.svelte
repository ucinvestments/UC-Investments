<script lang="ts">
  import "../app.css";
  import Icon from "@iconify/svelte";
  import Pi from "$lib/pi.svelte";
  import { onMount } from "svelte";
  import Loading from "$lib/loading.svelte";
  import { fade, fly, scale } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  
  let end;
  type button = "Asset" | "Company" | "Fund";
  
  let mounted = false;

  function asset() {
    activeButton = "Asset";
    fetchListedAssets();
  }
  function company() {
    activeButton = "Company";
    fetchListedAssets();
  }
  function fund() {
    activeButton = "Fund";
    fetchListedAssets();
  }

  function estim() {
    if (estimation == "true") {
      estimation = "false";
      fetchListedAssets();
    } else {
      estimation = "true";
      fetchListedAssets();
    }
  }

  function comp() {
    if (composition == "true") {
      composition = "false";
      fetchListedAssets();
    } else {
      composition = "true";
      fetchListedAssets();
    }
  }
  
  const API = "https://uc-investments-80f94956a47a.herokuapp.com";
  let activeButton: button = "Company";
  let searchTerm = "";
  let totalInvestedInChart = 0;
  let data;
  let selectedSlice;
  let filteredData;
  let loading = true;
  let composition = "true";
  let estimation = "true";
  
  function cap(s) {
    if (s && typeof s === "string") {
      return s
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
    } else {
      return "";
    }
  }

  function formatNumber(num) {
    let numStr = num.toString();
    let [integerPart, decimalPart] = numStr.split(".");
    let formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return formattedInteger;
  }

  async function fetchListedAssets() {
    loading = true;
    if (activeButton == "Company") {
      end = "/company-composition/" + composition + "/" + estimation;
    } else if (activeButton == "Fund") {
      end = "/listed-assets";
    } else {
      end = "/asset-classes";
    }

    try {
      console.log('Fetching data for:', activeButton, 'from:', API + end);
      const response = await fetch(API + end);
      if (!response.ok) {
        throw new Error("Failed to fetch listed assets");
      }
      const d = await response.json();
      console.log('Received data:', d);
      
      if (!d || !Array.isArray(d) || d.length === 0) {
        console.log('No valid data received');
        data = [];
        selectedSlice = null;
        filteredData = [];
      } else {
        data = d;
        selectedSlice = data[0];
        filteredData = data;
      }
      
      loading = false;
      sumTotalInvestments();
    } catch (err) {
      console.error('Error fetching data:', err);
      loading = false;
      data = [];
      selectedSlice = null;
      filteredData = [];
    }
  }

  function handleSliceClicked(event) {
    searchTerm = "";
    selectedSlice = event.detail;
  }
  
  function filterSearch() {
    const normalizedSearchTerm = searchTerm.trim().toLowerCase();
    if (activeButton == "Company") {
      filteredData = data.filter((item) =>
        item["asset"].toLowerCase().includes(normalizedSearchTerm),
      );
    } else if (activeButton == "Asset") {
      filteredData = data.filter((item) =>
        item["A.s.set ._Class"].toLowerCase().includes(normalizedSearchTerm),
      );
    } else {
      filteredData = data.filter((item) =>
        item["Asset Name"].toLowerCase().includes(normalizedSearchTerm),
      );
    }
  }

  let timeoutId;

  function handleSearch() {
    clearTimeout(timeoutId);
    const normalizedSearchTerm = searchTerm.trim().toLowerCase();
    let matchingSlice;
    if (activeButton == "Company") {
      matchingSlice = data.find((item) =>
        item["asset"].toLowerCase().includes(normalizedSearchTerm),
      );
    } else if (activeButton == "Asset") {
      matchingSlice = data.find((item) =>
        item["A.s.set ._Class"].toLowerCase().includes(normalizedSearchTerm),
      );
    } else {
      matchingSlice = data.find((item) =>
        item["Asset Name"].toLowerCase().includes(normalizedSearchTerm),
      );
    }
    if (matchingSlice) {
      timeoutId = setTimeout(() => {
        selectedSlice = matchingSlice;
        filterSearch();
        sumTotalInvestments();
      }, 300);
    } else {
      selectedSlice = data[0];
      if (filteredData.length === 0) {
        selectedSlice = data[0];
      } else {
        selectedSlice = filteredData[0];
      }
    }
  }

  function sumTotalInvestments() {
    let totalSum = 0;
    for (let i = 0; i < filteredData.length; i++) {
      if (activeButton == "Company") {
        totalSum += parseInt(filteredData[i]["total investment"]);
      } else if (activeButton == "Fund") {
        totalSum += parseInt(filteredData[i]["Total Investment"]);
      } else {
        totalSum += parseInt(filteredData[i]["Total Iℂnvest∈d"]);
      }
    }
    totalInvestedInChart = totalSum;
  }

  onMount(() => {
    mounted = true;
    fetchListedAssets();
  });
</script>

<!-- Data Warning Banner -->
<div class="warning-banner" in:fade={{ duration: 400 }}>
  <Icon icon="mdi:alert-circle" class="warning-icon" />
  <span>This data is from 2023. The UC releases updated investment reports annually.</span>
</div>

<!-- Hero Section -->
<div class="hero-section">
  {#if mounted}
    <div class="hero-content" in:fade={{ duration: 800, delay: 200 }}>
      <h1 class="hero-title">UC Investment Explorer</h1>
      <div class="hero-stats">
        <div class="stat-item" in:fade={{ duration: 600, delay: 400 }}>
          <span class="stat-value">$162B</span>
          <span class="stat-divider">•</span>
          <span class="stat-label">Total AUM</span>
        </div>
        <div class="stat-item" in:fade={{ duration: 600, delay: 500 }}>
          <span class="stat-value">$110B</span>
          <span class="stat-divider">•</span>
          <span class="stat-label">Published</span>
        </div>
        <div class="stat-item" in:fade={{ duration: 600, delay: 600 }}>
          <span class="stat-value">68%</span>
          <span class="stat-divider">•</span>
          <span class="stat-label">Transparent</span>
        </div>
      </div>
      <p class="hero-description" in:fade={{ duration: 800, delay: 700 }}>
        Explore UC's endowment and pension fund investments with full transparency.
      </p>
    </div>
  {/if}
</div>

{#if loading}
  <div in:fade={{ duration: 300 }}>
    <Loading />
  </div>
{:else}
  <div class="main-container" in:fade={{ duration: 600 }}>
    <!-- Navigation Tabs -->
    <div class="nav-tabs" in:fly={{ y: -20, duration: 500, delay: 200 }}>
      <button 
        class="nav-tab" 
        class:active={activeButton === "Company"} 
        on:click={company}
      >
        <Icon icon="mdi:company" class="tab-icon" />
        Companies
      </button>
      <button 
        class="nav-tab" 
        class:active={activeButton === "Asset"} 
        on:click={asset}
      >
        <Icon icon="mdi:chart-pie" class="tab-icon" />
        Asset Classes
      </button>
      <button 
        class="nav-tab" 
        class:active={activeButton === "Fund"} 
        on:click={fund}
      >
        <Icon icon="mdi:wallet" class="tab-icon" />
        Funds
      </button>
    </div>

    <!-- Search Bar -->
    <div class="search-section" in:fly={{ y: 20, duration: 500, delay: 300 }}>
      <div class="search-wrapper">
        <Icon icon="mdi:magnify" class="search-icon" />
        <input
          type="text"
          placeholder={`Search ${activeButton === "Company" ? "companies" : activeButton === "Asset" ? "asset classes" : "funds"}...`}
          bind:value={searchTerm}
          on:input={handleSearch}
          class="search-input"
        />
        {#if searchTerm}
          <button on:click={() => searchTerm = ''} class="clear-btn">
            <Icon icon="mdi:close" />
          </button>
        {/if}
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Chart Section -->
      <div class="chart-section glass-card" in:fly={{ x: -30, duration: 600, delay: 400 }}>
        <div class="chart-header">
          <h3 class="section-title">Portfolio Distribution</h3>
          <div class="chart-total">
            ${formatNumber(totalInvestedInChart)}
          </div>
        </div>
        <div class="chart-container">
          <Pi
            {filteredData}
            {selectedSlice}
            {activeButton}
            {totalInvestedInChart}
            on:sliceClicked={handleSliceClicked}
          />
        </div>
      </div>

      <!-- Details Section -->
      <div class="details-section glass-card" in:fly={{ x: 30, duration: 600, delay: 400 }}>
        <div class="details-content">
          {#if !selectedSlice}
            <div class="no-data-message">
              <Icon icon="mdi:information-outline" class="no-data-icon" />
              <p>No data available to display</p>
            </div>
          {:else if selectedSlice && selectedSlice.isAggregate}
            <!-- Aggregated Others Item -->
            <div class="detail-header">
              <h2 class="detail-title">Others ({selectedSlice.aggregatedCount} items)</h2>
              <span class="detail-amount">
                {#if activeButton == "Company"}
                  ${formatNumber(selectedSlice["total investment"])}
                {:else if activeButton == "Fund"}
                  ${formatNumber(selectedSlice["Total Investment"])}
                {:else}
                  ${formatNumber(selectedSlice["Total Iℂnvest∈d"])}
                {/if}
              </span>
            </div>
            
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Aggregated Items</span>
                <div class="aggregated-info">
                  <div class="aggregated-summary">
                    <Icon icon="mdi:information-outline" class="info-icon" />
                    <div>
                      <p class="aggregated-text">
                        This represents the combined value of {selectedSlice.aggregatedCount} smaller 
                        {activeButton === "Company" ? "companies" : activeButton === "Fund" ? "funds" : "asset classes"} 
                        that individually have lower investment amounts.
                      </p>
                      <p class="aggregated-note">
                        Showing top 24 items individually for clarity.
                      </p>
                    </div>
                  </div>
                  {#if selectedSlice.aggregatedItems && selectedSlice.aggregatedItems.length > 0}
                    <div class="aggregated-preview">
                      <span class="preview-label">Sample items:</span>
                      <div class="preview-list">
                        {#each selectedSlice.aggregatedItems.slice(0, 5) as item}
                          <div class="preview-item">
                            {#if activeButton == "Company"}
                              <span class="preview-name">{cap(item["asset"])}</span>
                              <span class="preview-amount">${formatNumber(item["total investment"])}</span>
                            {:else if activeButton == "Fund"}
                              <span class="preview-name">{cap(item["Asset Name"])}</span>
                              <span class="preview-amount">${formatNumber(item["Total Investment"])}</span>
                            {:else}
                              <span class="preview-name">{cap(item["A.s.set ._Class"])}</span>
                              <span class="preview-amount">${formatNumber(item["Total Iℂnvest∈d"])}</span>
                            {/if}
                          </div>
                        {/each}
                        {#if selectedSlice.aggregatedItems.length > 5}
                          <div class="preview-more">
                            ... and {selectedSlice.aggregatedItems.length - 5} more
                          </div>
                        {/if}
                      </div>
                    </div>
                  {/if}
                </div>
              </div>
            </div>
            
          {:else if activeButton == "Fund"}
            <div class="detail-header">
              <h2 class="detail-title">{cap(selectedSlice["Asset Name"])}</h2>
              <span class="detail-badge">{selectedSlice["Asset Type"]}</span>
            </div>
            
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Funding Sources</span>
                <div class="funding-list">
                  {#each selectedSlice["Funding Sources"] as f}
                    <div class="funding-item" in:fade={{ duration: 300 }}>
                      <span class="funding-name">{f["Source:"]}</span>
                      <span class="funding-amount">${formatNumber(f["Ammount"])}</span>
                    </div>
                  {/each}
                </div>
              </div>
            </div>
            
          {:else if activeButton == "Company"}
            <div class="detail-header">
              <h2 class="detail-title">{cap(selectedSlice["asset"])}</h2>
              <span class="detail-amount">
                ${formatNumber(selectedSlice["total investment"])}
              </span>
            </div>
            
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Investment Sources</span>
                <div class="funding-list">
                  {#each selectedSlice["funding sources"] as fund}
                    <div class="funding-item" in:fade={{ duration: 300 }}>
                      <span class="funding-name">{fund["fund name:"]}</span>
                      <span class="funding-amount">
                        ${formatNumber(fund["ammount_invested"])}
                      </span>
                    </div>
                  {/each}
                </div>
              </div>
            </div>
            
            <!-- Control Buttons -->
            <div class="control-buttons">
              <button
                class="control-btn"
                class:active={estimation === "true"}
                on:click={estim}
              >
                <Icon icon={estimation === "true" ? "mdi:check" : "mdi:close"} class="btn-icon" />
                Include Estimates
              </button>
              <button
                class="control-btn"
                class:active={composition === "true"}
                on:click={comp}
              >
                <Icon icon={composition === "true" ? "mdi:check" : "mdi:close"} class="btn-icon" />
                Consolidate Shares
              </button>
            </div>
            
          {:else}
            <div class="detail-header">
              <h2 class="detail-title">{cap(selectedSlice["A.s.set ._Class"])}</h2>
              <span class="detail-amount">
                ${formatNumber(selectedSlice["Total Iℂnvest∈d"])}
              </span>
            </div>
            
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Investment Breakdown</span>
                <div class="funding-list">
                  {#each selectedSlice["InVesTmeNts"] as f}
                    <div class="funding-item" in:fade={{ duration: 300 }}>
                      <span class="funding-name">{f}</span>
                    </div>
                  {/each}
                </div>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    {#if activeButton == "Company"}
      <div class="disclaimer" in:fade={{ duration: 600, delay: 500 }}>
        <Icon icon="mdi:information-outline" class="disclaimer-icon" />
        <p>
          The UC does not have direct investments in these companies. Data is constructed by analyzing 
          index fund compositions and aggregating holdings across all funds. Fund compositions change daily; 
          this data reflects the most recent disclosures. View our 
          <a href="/about" class="disclaimer-link">methodology</a> for evidence-based predictions.
        </p>
      </div>
    {/if}
  </div>
{/if}

<style lang="postcss">
  :global(body) {
    overflow-x: hidden;
  }

  .warning-banner {
    background: linear-gradient(135deg, var(--golden-gate), var(--wellman));
    color: white;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 0.925rem;
    font-weight: 500;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  :global(.warning-icon) {
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .hero-section {
    padding: 1.5rem 1rem;
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    position: relative;
    overflow: hidden;
  }

  .hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  .hero-content {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
    position: relative;
    z-index: 1;
  }

  .hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
  }

  .hero-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1rem;
    flex-wrap: nowrap;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: white;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--sec);
    font-family: 'Space Grotesk', sans-serif;
  }

  .stat-divider {
    color: rgba(255, 255, 255, 0.4);
    font-size: 1.25rem;
  }

  .stat-label {
    font-size: 0.925rem;
    color: rgba(255, 255, 255, 0.95);
    font-weight: 500;
  }

  .hero-description {
    max-width: 600px;
    margin: 0 auto;
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.5;
  }

  .main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }

  .nav-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .nav-tab {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.75rem;
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-secondary);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .nav-tab::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 0;
    height: 100%;
    background: linear-gradient(90deg, var(--founder), var(--pri));
    transition: width 0.3s ease;
    z-index: -1;
  }

  .nav-tab:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--founder);
  }

  .nav-tab.active {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    border-color: transparent;
    transform: scale(1.05);
    box-shadow: var(--shadow-lg);
  }

  :global(.tab-icon) {
    font-size: 1.25rem;
  }

  .search-section {
    margin-bottom: 3rem;
    display: flex;
    justify-content: center;
  }

  .search-wrapper {
    position: relative;
    width: 100%;
    max-width: 600px;
  }

  :global(.search-icon) {
    position: absolute;
    left: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    font-size: 1.25rem;
  }

  .search-input {
    width: 100%;
    padding: 1rem 3.5rem;
    border: 2px solid var(--border);
    border-radius: 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
    box-shadow: var(--shadow-sm);
  }

  .search-input:focus {
    outline: none;
    border-color: var(--founder);
    box-shadow: 0 0 0 3px rgba(59, 126, 161, 0.1), var(--shadow-md);
    transform: translateY(-1px);
  }

  .clear-btn {
    position: absolute;
    right: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
  }

  .clear-btn:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }

  .content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .glass-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-md);
    padding: 2rem;
    transition: all 0.3s ease;
  }

  .glass-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .chart-section {
    display: flex;
    flex-direction: column;
  }

  .chart-header {
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .section-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
  }

  .chart-total {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--pri);
    letter-spacing: -0.02em;
  }

  .chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
  }

  .details-section {
    display: flex;
    flex-direction: column;
  }

  .details-content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .detail-header {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid var(--border);
  }

  .detail-title {
    font-size: 1.875rem;
    font-weight: 700;
    color: var(--pri);
    margin-bottom: 0.75rem;
    letter-spacing: -0.01em;
  }

  .detail-badge {
    display: inline-block;
    padding: 0.375rem 1rem;
    background: linear-gradient(135deg, var(--sec), var(--medalist));
    color: white;
    border-radius: 2rem;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .detail-amount {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--founder);
  }

  .detail-grid {
    flex: 1;
  }

  .detail-item {
    margin-bottom: 1.5rem;
  }

  .detail-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .funding-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .funding-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.875rem 1.25rem;
    background: var(--bg-secondary);
    border-radius: 0.75rem;
    transition: all 0.2s ease;
    border: 1px solid transparent;
  }

  .funding-item:hover {
    background: white;
    border-color: var(--founder);
    transform: translateX(4px);
    box-shadow: var(--shadow-sm);
  }

  .funding-name {
    font-weight: 500;
    color: var(--text-primary);
  }

  .funding-amount {
    font-weight: 700;
    color: var(--founder);
    font-family: 'Space Grotesk', sans-serif;
  }

  .control-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
  }

  .control-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.25rem;
    background: white;
    border: 2px solid var(--border);
    border-radius: 0.75rem;
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-secondary);
    transition: all 0.3s ease;
    cursor: pointer;
  }

  .control-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .control-btn.active {
    background: linear-gradient(135deg, var(--soybean), var(--lap-lane));
    color: white;
    border-color: transparent;
  }

  :global(.btn-icon) {
    font-size: 1rem;
  }

  .aggregated-info {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .aggregated-summary {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 1rem;
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 0.75rem;
    border: 1px solid var(--border);
  }

  :global(.info-icon) {
    font-size: 1.5rem;
    color: var(--founder);
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .aggregated-text {
    color: var(--text-primary);
    line-height: 1.6;
    margin-bottom: 0.5rem;
    font-size: 0.925rem;
  }

  .aggregated-note {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-style: italic;
    margin: 0;
  }

  .aggregated-preview {
    background: var(--bg);
    border-radius: 0.75rem;
    padding: 1rem;
    border: 1px solid var(--border);
  }

  .preview-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .preview-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .preview-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
  }

  .preview-item:last-child {
    border-bottom: none;
  }

  .preview-name {
    font-size: 0.875rem;
    color: var(--text-primary);
    font-weight: 500;
  }

  .preview-amount {
    font-size: 0.875rem;
    color: var(--founder);
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
  }

  .preview-more {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-style: italic;
    text-align: center;
    padding: 0.5rem;
  }

  .no-data-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
    color: var(--text-secondary);
  }

  :global(.no-data-icon) {
    font-size: 3rem;
    color: var(--border);
    margin-bottom: 1rem;
  }

  .no-data-message p {
    font-size: 1rem;
    margin: 0;
  }

  .disclaimer {
    display: flex;
    gap: 1rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1rem;
    border: 1px solid var(--border);
    margin-top: 2rem;
  }

  :global(.disclaimer-icon) {
    flex-shrink: 0;
    color: var(--founder);
    font-size: 1.5rem;
    margin-top: 0.125rem;
  }

  .disclaimer p {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.925rem;
  }

  .disclaimer-link {
    color: var(--founder);
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
  }

  .disclaimer-link:hover {
    color: var(--pri);
    border-bottom-color: var(--pri);
  }

  @media (max-width: 1024px) {
    .content-grid {
      grid-template-columns: 1fr;
    }
    
    .hero-title {
      font-size: 2rem;
    }
    
    .hero-stats {
      gap: 1.5rem;
    }
    
    .stat-value {
      font-size: 1.25rem;
    }
  }

  @media (max-width: 640px) {
    .hero-section {
      padding: 1rem 0.75rem;
    }
    
    .hero-title {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
    }

    .hero-stats {
      flex-direction: column;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
    }

    .stat-item {
      justify-content: center;
    }

    .stat-value {
      font-size: 1.125rem;
    }

    .stat-label {
      font-size: 0.875rem;
    }

    .hero-description {
      font-size: 0.925rem;
      padding: 0 1rem;
    }

    .warning-banner {
      font-size: 0.875rem;
      padding: 0.625rem 0.75rem;
    }
    
    .main-container {
      padding: 2rem 1rem;
    }
    
    .nav-tab {
      padding: 0.75rem 1.25rem;
      font-size: 0.875rem;
    }
    
    .chart-total {
      font-size: 2rem;
    }
    
    .detail-title {
      font-size: 1.5rem;
    }
  }
</style>