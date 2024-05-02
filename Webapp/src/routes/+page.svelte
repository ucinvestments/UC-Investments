<script lang="ts">
  import "../app.css";
  import sam from "$lib/sam_hero.png";
  import Icon from "@iconify/svelte";
  import Pi from "$lib/pi.svelte";
  import { onMount } from "svelte";

  type button = "Asset" | "Company";
  let activeButton: button = "Company"; // Initial value
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
  let searchTerm = ""; // Initialize a variable to store the search term

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

  onMount(() => {
    // Add the active-button class to the "By Listed Asset" button
    const assetButton = document.querySelector('button[on\\:click*="Asset"]');
    if (assetButton) {
      assetButton.classList.add("active-button");
    }
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
    on:click={() => (activeButton = "Company")}>By Company Listed</button
  >

  <button
    class:active-button={activeButton === "Asset"}
    on:click={() => (activeButton = "Asset")}>By Fund</button
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
  </div>
  <div class="text-container">
    <div class="text-left x p-3 rounded-sm">
      <p class="text-center">
        <b>{cap(selectedSlice.key)}</b>
      </p>
      <br />
      <p class=""><b>Total Invested: </b>{selectedSlice.value}</p>
      {#if activeButton == "Asset"}{:else if activeButton == "Company"}
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
