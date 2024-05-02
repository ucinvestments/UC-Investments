<script lang="ts">
  import "../app.css";
  import sam from "$lib/sam_hero.png";
  import Icon from "@iconify/svelte";
  import Pi from "$lib/pi.svelte";
  import { onMount } from "svelte";

  type button = "Asset" | "Company" | "Fund";

  const API = "https://uc-investments-80f94956a47a.herokuapp.com/"
  let activeButton: button = "Company"; // Initial value
  let searchTerm = ""; // Initialize a variable to store the search term
  let totalInvestedInChart = 0;

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

  async function fetchListedAssets() {
    try {
      const response = await fetch(API + "listed-assets");
      if (!response.ok) {
        throw new Error("Failed to fetch listed assets");
      }
      const d = await response.json();
      data = d.data;
      console.log(data);
    } catch (err) {
      console.log(err.message);
    }
  }

  let data = [
    { key: "microsfot", value: 10, type: "bad", fundingSource: [1, 2, 3] },
    { key: "big bad", value: 20, type: "bad", fundingSource: [1, 2, 3] },
    { key: "killing people", value: 30, type: "bad", fundingSource: [1, 2, 3] },
    { key: "eating people", value: 40, type: "bad", fundingSource: [1, 2, 3] },
    {
      key: "destroying housing market",
      value: 40,
      type: "bad",
      fundingSource: [1, 2, 3],
    },
    {
      key: "in socites of wealth",
      value: 40,
      type: "bad",
      fundingSource: [1, 2, 3],
    },
    { key: "guy dobirid", value: 40, type: "bad", fundingSource: [1, 2, 3] },
    {
      key: "composition book",
      value: 40,
      type: "bad",
      fundingSource: [1, 2, 3],
    },
    { key: "cocaine", value: 40, type: "bad", fundingSource: [1, 2, 3] },
    { key: "nicotine", value: 40, type: "bad", fundingSource: [1, 2, 3] },
    { key: "chadonay", value: 40, type: "bad", fundingSource: [1, 2, 3] },
  ];

  let selectedSlice = data[0]; // Initialize a variable to store the selected slice

  let filteredData = data;
  // Handler function for the 'sliceClicked' event
  function handleSliceClicked(event) {
    searchTerm = "";
    selectedSlice = event.detail;
    console.log("Selected slice:", selectedSlice);
  }
  function filterSearch() {
    const normalizedSearchTerm = searchTerm.trim().toLowerCase();
    filteredData = data.filter(
      (item) =>
        item.key.toLowerCase().includes(normalizedSearchTerm) ||
        item.type.toLowerCase().includes(normalizedSearchTerm) ||
        item.fundingSource.some((fund) =>
          fund.toString().includes(normalizedSearchTerm),
        ),
    );
    console.log(filteredData);
  }

  function handleSearch() {
    const normalizedSearchTerm = searchTerm.trim().toLowerCase();
    const matchingSlice = data.find((item) =>
      item.key.toLowerCase().includes(normalizedSearchTerm),
    );
    if (matchingSlice) {
      selectedSlice = matchingSlice; // Assign the entire object
      console.log("Search found:", selectedSlice);
      filterSearch();
    } else {
      selectedSlice = selectedSlice;
      console.log("No matching slice found");
    }
  }

  function sumTotalInvestments() {
    let totalSum = 0;
    for (let i = 0; i < filteredData.length; i++) {
      totalSum += parseInt(filteredData[i]["Total Investment"]);
    }
    return totalSum;
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
  <button
    class:active-button={activeButton === "Company"}
    on:click={() => (activeButton = "Company")}>By Company</button
  >

  <button
    class:active-button={activeButton === "Asset"}
    on:click={() => (activeButton = "Asset")}>By Asset Class</button
  >

<button
    class:active-button={activeButton === "Fund"}
    on:click={() => (activeButton = "Fund")}>By Fund</button
  >
</div>

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
    <Pi {filteredData} {selectedSlice} on:sliceClicked={handleSliceClicked} />
    <p class="text-center">Total value of chart ${totalInvestedInChart}</p>
  </div>


  <div class="text-container">
    <div class="text-left x p-3 rounded-sm">
      {#if activeButton == "Asset"}
      <p class="text-center">
        <b>Asset Name: </b>{cap(selectedSlice.key)}
      </p>
      <br />

      {:else if activeButton == "Company"}
      <p class="text-center">
        <b>Company Name: </b>{cap(selectedSlice.key)}
      </p>
      <p class=""><b>Total Invested: </b>{selectedSlice.value}</p>
        <p class=""><b>Company Type: </b>{selectedSlice.type}</p>
      {:else}{/if}
      <p class="">
        <br />
        <b>Funding Source: </b>
        {#each selectedSlice.fundingSource as fund}
          <p class=" rounded-sm p-1">{fund}</p>
        {/each}
      </p>
    </div>
  </div>
</div>

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
