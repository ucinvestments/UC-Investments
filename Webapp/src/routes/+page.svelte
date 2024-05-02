<script lang="ts">
  import "../app.css";
  import Icon from "@iconify/svelte";
  import Pi from "$lib/pi.svelte";
  import { onMount } from "svelte";
  let end;
  type button = "Asset" | "Company" | "Fund";

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
  let activeButton: button = "Company"; // Initial value
  let searchTerm = ""; // Initialize a variable to store the search term
  let totalInvestedInChart = 0;
  let data;
  let selectedSlice; // Initialize a variable to store the selected slice
  let filteredData;
  let loading = true;
  let composition = "true"; // combine share types or not
  let estimation = "true"; // are we using estimates or not
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
    /**
     * Formats a number as a human-readable string with commas.
     *
     * @param {number} num - The number to be formatted.
     * @returns {string} The formatted number as a string.
     */
    // Convert the number to a string

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
      const response = await fetch(API + end);
      if (!response.ok) {
        throw new Error("Failed to fetch listed assets");
      }
      const d = await response.json();
      data = d;
      selectedSlice = data[0]; // Initialize a variable to store the selected slice
      filteredData = data;
      loading = false;
      console.log(data);

      sumTotalInvestments();
    } catch (err) {
      console.log(err.message);
    }
  }

  // Handler function for the 'sliceClicked' event
  function handleSliceClicked(event) {
    searchTerm = "";
    selectedSlice = event.detail;
    console.log("Selected slice:", selectedSlice);
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
    console.log(filteredData);
  }

  function handleSearch() {
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
      selectedSlice = matchingSlice; // Assign the entire object
      console.log("Search found:", selectedSlice);
      filterSearch();
      sumTotalInvestments();
    } else {
      selectedSlice = data[0];
      console.log("No matching slice found");
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
    // Add the active-button class to the "By Listed Asset" button
    const assetButton = document.querySelector('button[on\\:click*="Asset"]');
    if (assetButton) {
      assetButton.classList.add("active-button");
    }
    fetchListedAssets();
  });
</script>

<p
  class="text-center text-xl my-3 p-1
  "
>
  The University of California Manages <b>164 billion </b>dollars of
  investments. Explore where this money goes below:
</p>
<div class="flex justify-between but text-lg m-1">
  <button class:active-button={activeButton === "Company"} on:click={company}
    >By Company</button
  >

  <button class:active-button={activeButton === "Asset"} on:click={asset}
    >By Asset Class</button
  >

  <button class:active-button={activeButton === "Fund"} on:click={fund}
    >By Fund</button
  >
</div>

{#if loading}
  <p class="text-center h-full m-auto justify-center">loading</p>
{:else}
  <div class="cont">
    <div class="image-container">
      <div class="search-container text-center">
        <input
          type="text"
          placeholder="Search..."
          bind:value={searchTerm}
          on:input={handleSearch}
          class="p-3 rounded-md w-5/6 bg-white focus:outline-none focus:ring-2 focus:ring-[var(--founder)]"
        />
      </div>
      <Pi
        {filteredData}
        {selectedSlice}
        {activeButton}
        on:sliceClicked={handleSliceClicked}
      />
      <p class="text-center">
        Total value of chart ${formatNumber(totalInvestedInChart)}
      </p>
    </div>

    <div class="text-container">
      <div class="text-left x p-3 rounded-sm">
        {#if activeButton == "Fund"}
          <p class="text-center">
            <b>{cap(selectedSlice["Asset Name"])}</b>
          </p>
          <br />

          <p><b>Asset Type: </b>{selectedSlice["Asset Type"]}</p>
          <br />
          <br />
          <p>
            <b>Funding Sources: </b>

            {#each selectedSlice["Funding Sources"] as f}
              <p class=" rounded-sm px-2">
                <b>- {f["Source:"]} : </b>${formatNumber(f["Ammount"])}
              </p>
            {/each}
          </p>
        {:else if activeButton == "Company"}
          <p class="text-center text-2xl">
            <b>{cap(selectedSlice["asset"])}</b>
          </p>
          <p class="text-center">
            <b>Total Invested: </b>${formatNumber(
              selectedSlice["total investment"],
            )}
          </p>
          <br />
          <b>Funding Sources: </b>
          {#each selectedSlice["funding sources"] as fund}
            <p class=" rounded-sm px-2">
              <b>- {fund["fund name:"]} : </b>${formatNumber(
                fund["ammount_invested"],
              )}
            </p>
          {/each}
          <div class="m-auto text-center">
            <button
              class:green={estimation === "true"}
              class:red={estimation !== "true"}
              on:click={estim}
            >
              Include Estimated Figures
            </button>
            <button
              class:green={composition === "true"}
              class:red={composition !== "true"}
              on:click={comp}
            >
              Consolidate Stock Classes
            </button>
          </div>
          <!-- <p class=""><b>Total Invested: </b>{selectedSlice.value}</p> -->
          <!-- <p class=""><b>Company Type: </b>{selectedSlice.type}</p> -->
        {:else}
          <p class="text-center">
            <b>{cap(selectedSlice["A.s.set ._Class"])} </b>
          </p>
          <br />
          <b>Total Invested: </b>{selectedSlice["Total Iℂnvest∈d"]}
          <br />
          <p>
            <b>Funding Source: </b>
            {#each selectedSlice["InVesTmeNts"] as f}
              <p class=" rounded-sm p-1">- {f}</p>
            {/each}
          </p>
        {/if}
      </div>
    </div>
  </div>
{/if}
<p class="p-3">
  Note: The UC does not have direct investments in any of these companies. All
  of this data is constructed by examining the composition of the index funds we
  are invested in, and accumulating the holdings across all funds. The
  composition of these funds changes day to day, so this data is as of each
  fund’s most recent disclosure. Additionally, most funds do not publish full
  holdings, but instead their top 10 holdings, which is why you will see a
  significant amount of the assets grayed out. We’ve developed novel methodology
  to make evidence-based predictions of the compositions of our largest funds,
  and you can view our predictions by clicking “Show informed estimate”
</p>

<style lang="postcss">
  .active-button {
    background-color: var(--founder);
    transition: background-color 0.3s ease-in-out; /* Add transition */
  }

  .x {
    border-radius: 0.1rem;
    border: 2px solid rgb(197, 197, 199);
  }
  button {
    margin: 0.5rem;
    padding: 0.5rem;
    border-radius: 0.1rem;
    border: 2px solid rgb(197, 197, 199);
  }
  input {
    border-radius: 0.1rem;
    border: 2px solid rgb(197, 197, 199);
  }

  .green {
    background-color: var(--soybean);
  }

  .red {
    background-color: var(--golden-gate);
  }

  .but {
    display: flex;
    flex-direction: row; /* Default to row for larger screens */
    justify-content: center;
    margin: 1rem;
  }
  .cont {
    display: flex;
    flex-direction: row; /* Default to row for larger screens */
    justify-content: center;
  }
  .image-container,
  .text-container {
    flex: 1; /* This will make both divs take up equal space */
    display: flex;
    flex-direction: column; /* Stack children vertically */
    padding: 1rem;
    justify-content: center;
    height: max-content;
  }
  .text-container {
  }

  /* Responsive text sizes */
  h1 {
    font-size: 8rem; /* Adjust the size for mobile */
  }
  h3 {
    font-size: 4rem; /* Adjust the size for mobile */
  }
  p {
    font-size: 1rem; /* Adjust the size for mobile */
  }
  a {
    margin: 3rem;
  }
  /* Media query for tablet and mobile screens */
  @media (max-width: 768px) {
    .cont {
      flex-direction: column;
    }
    .but {
      display: flex;
      font-size: medium;
    }
  }
</style>
