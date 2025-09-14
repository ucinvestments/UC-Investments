<script>
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";
  import Fuse from "fuse.js";

  let mounted = false;
  let searchQuery = "";
  let filteredArticles = [];
  let selectedTag = "all";

  // Articles data - will be populated from markdown files
  const articles = [];

  // Extract unique tags
  const allTags = [
    "all",
    ...new Set(articles.flatMap((article) => article.tags)),
  ];

  // Initialize Fuse.js for fuzzy search
  const fuseOptions = {
    keys: ["title", "excerpt", "tags", "author"],
    threshold: 0.3,
    includeScore: true,
  };

  const fuse = new Fuse(articles, fuseOptions);

  function searchArticles() {
    if (searchQuery.trim() === "" && selectedTag === "all") {
      filteredArticles = articles;
    } else if (searchQuery.trim() === "") {
      filteredArticles = articles.filter(
        (article) =>
          selectedTag === "all" || article.tags.includes(selectedTag),
      );
    } else {
      const searchResults = fuse.search(searchQuery);
      filteredArticles = searchResults
        .map((result) => result.item)
        .filter(
          (article) =>
            selectedTag === "all" || article.tags.includes(selectedTag),
        );
    }
  }

  function handleTagFilter(tag) {
    selectedTag = tag;
    searchArticles();
  }

  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  onMount(() => {
    mounted = true;
    filteredArticles = articles;
  });

  $: searchQuery, selectedTag, searchArticles();
</script>

{#if mounted}
  <div class="press-container">
    <!-- Hero Section -->
    <div class="press-hero" in:fade={{ duration: 800 }}>
      <div class="hero-content">
        <Icon icon="mdi:newspaper-variant" class="hero-icon" />
        <h1 class="hero-title">Press & Research</h1>
        <p class="hero-subtitle">
          Independent research and analysis on UC investment practices
        </p>
      </div>
    </div>

    <!-- Call to Action Banner -->
    <div class="cta-banner" in:fly={{ y: 20, duration: 600, delay: 200 }}>
      <Icon icon="mdi:email-send" class="cta-icon" />
      <p class="cta-text">
        Have relevant research on UC investment holdings? Email your findings in
        a markdown document to
        <a href="mailto:press@ucinvestments.info" class="cta-email"
          >press@ucinvestments.info</a
        >
      </p>
    </div>

    <!-- Search and Filter Section -->
    <div class="search-section" in:fly={{ y: 30, duration: 600, delay: 400 }}>
      <div class="search-container">
        <div class="search-wrapper">
          <Icon icon="mdi:magnify" class="search-icon" />
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search articles by title, content, or author..."
            class="search-input"
          />
          {#if searchQuery}
            <button
              on:click={() => (searchQuery = "")}
              class="clear-button"
              aria-label="Clear search"
            >
              <Icon icon="mdi:close" />
            </button>
          {/if}
        </div>

        <div class="tag-filters">
          {#each allTags as tag}
            <button
              class="tag-button"
              class:active={selectedTag === tag}
              on:click={() => handleTagFilter(tag)}
            >
              {tag === "all" ? "All Articles" : tag}
            </button>
          {/each}
        </div>
      </div>
    </div>

    <!-- Articles Grid -->
    <div class="content-wrapper">
      <div class="no-articles" in:fade={{ duration: 600, delay: 600 }}>
        <Icon icon="mdi:file-document-plus" class="no-articles-icon" />
        <h3 class="no-articles-title">Research Articles Coming Soon</h3>
        <p class="no-articles-text">
          We're preparing independent research and analysis on UC investment practices.
          Articles will be published here as they become available.
        </p>

        <div class="contribute-prompt">
          <Icon icon="mdi:lightbulb" class="contribute-icon" />
          <p>
            <strong>Have research to contribute?</strong><br>
            Submit your findings in markdown format to help expand our analysis.
          </p>
          <a href="mailto:press@ucinvestments.info" class="contribute-button">
            <Icon icon="mdi:email-send" class="email-icon" />
            Submit Research
          </a>
        </div>
      </div>
    </div>

    <!-- Resources Section -->
    <section
      class="resources-section"
      in:fly={{ y: 30, duration: 600, delay: 1000 }}
    >
      <div class="resources-card">
        <Icon icon="mdi:bookshelf" class="resources-icon" />
        <h2 class="resources-title">Additional Resources</h2>
        <div class="resources-grid">
          <a
            href="https://www.ucop.edu/investment-office/index.html"
            target="_blank"
            rel="noopener noreferrer"
            class="resource-link"
          >
            <Icon icon="mdi:office-building" class="resource-icon" />
            <span>UC Investment Office</span>
            <Icon icon="mdi:open-in-new" class="external-icon" />
          </a>
          <a
            href="https://regents.universityofcalifornia.edu/governance/policies/"
            target="_blank"
            rel="noopener noreferrer"
            class="resource-link"
          >
            <Icon icon="mdi:file-document" class="resource-icon" />
            <span>Investment Policies</span>
            <Icon icon="mdi:open-in-new" class="external-icon" />
          </a>
          <a
            href="https://www.universityofcalifornia.edu/press-room/"
            target="_blank"
            rel="noopener noreferrer"
            class="resource-link"
          >
            <Icon icon="mdi:newspaper" class="resource-icon" />
            <span>Official Press Releases</span>
            <Icon icon="mdi:open-in-new" class="external-icon" />
          </a>
        </div>
      </div>
    </section>
  </div>
{/if}

<style>
  .press-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }

  .press-hero {
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .press-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  .hero-content {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  :global(.hero-icon) {
    font-size: 3rem;
    color: var(--sec);
    margin-bottom: 1rem;
  }

  .hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
  }

  .hero-subtitle {
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.6;
    margin: 0;
  }

  /* CTA Banner */
  .cta-banner {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, var(--sec), var(--founder));
    border-radius: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: var(--shadow-md);
  }

  :global(.cta-icon) {
    font-size: 1.5rem;
    color: white;
    flex-shrink: 0;
  }

  .cta-text {
    color: white;
    margin: 0;
    flex: 1;
  }

  .cta-email {
    color: white;
    font-weight: 600;
    text-decoration: underline;
  }

  .cta-email:hover {
    text-decoration: none;
  }

  /* Search Section */
  .search-section {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
  }

  .search-container {
    background: white;
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2rem;
    box-shadow: var(--shadow-sm);
  }

  .search-wrapper {
    position: relative;
    margin-bottom: 1.5rem;
  }

  :global(.search-icon) {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.25rem;
    color: var(--text-secondary);
  }

  .search-input {
    width: 100%;
    padding: 0.875rem 3rem;
    border: 2px solid var(--border);
    border-radius: 0.75rem;
    font-size: 1rem;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--founder);
    box-shadow: 0 0 0 3px rgba(0, 86, 63, 0.1);
  }

  .clear-button {
    position: absolute;
    right: 1rem;
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
    transition: all 0.2s ease;
  }

  .clear-button:hover {
    color: var(--pri);
  }

  .tag-filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .tag-button {
    padding: 0.5rem 1rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .tag-button:hover {
    background: var(--bg-secondary);
    border-color: var(--founder);
  }

  .tag-button.active {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    border-color: var(--founder);
  }

  /* Content */
  .content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
  }

  .article-card {
    background: white;
    border-radius: 1rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
  }

  .article-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .article-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .article-tags {
    display: flex;
    gap: 0.375rem;
    flex-wrap: wrap;
    flex: 1;
  }

  .article-tag {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .read-time {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    white-space: nowrap;
  }

  :global(.time-icon) {
    font-size: 0.875rem;
  }

  .article-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.375rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    line-height: 1.3;
  }

  .article-link {
    color: var(--pri);
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .article-link:hover {
    color: var(--founder);
  }

  .article-excerpt {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.5rem;
    flex: 1;
  }

  .article-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
  }

  .article-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }

  .author,
  .date {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  :global(.meta-icon) {
    font-size: 0.875rem;
    color: var(--founder);
  }

  .read-more {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--founder);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
  }

  .read-more:hover {
    color: var(--pri);
    transform: translateX(2px);
  }

  :global(.arrow-icon) {
    font-size: 1rem;
  }

  /* No Articles State */
  .no-articles {
    text-align: center;
    padding: 4rem 2rem;
  }

  :global(.no-articles-icon) {
    font-size: 4rem;
    color: var(--founder);
    margin-bottom: 1.5rem;
  }

  .no-articles-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--pri);
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
  }

  .no-articles-text {
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto 3rem;
  }

  .contribute-prompt {
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    max-width: 500px;
    margin: 0 auto;
    box-shadow: var(--shadow-sm);
  }

  :global(.contribute-icon) {
    font-size: 2.5rem;
    color: var(--sec);
    margin-bottom: 1rem;
  }

  .contribute-prompt p {
    color: var(--text-primary);
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  .contribute-prompt strong {
    color: var(--pri);
  }

  .contribute-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    text-decoration: none;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .contribute-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  :global(.email-icon) {
    font-size: 1.125rem;
  }

  /* Resources Section */
  .resources-section {
    max-width: 1200px;
    margin: 4rem auto 2rem;
    padding: 0 2rem;
  }

  .resources-card {
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    text-align: center;
    box-shadow: var(--shadow-md);
  }

  :global(.resources-icon) {
    font-size: 2.5rem;
    color: var(--founder);
    margin-bottom: 1rem;
  }

  .resources-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--pri);
    margin-bottom: 2rem;
  }

  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }

  .resource-link {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem;
    background: white;
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    color: var(--text-primary);
    text-decoration: none;
    transition: all 0.3s ease;
  }

  .resource-link:hover {
    background: var(--bg);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }

  :global(.resource-icon) {
    font-size: 1.25rem;
    color: var(--founder);
  }

  :global(.external-icon) {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .press-hero {
      padding: 2rem 1rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .cta-banner {
      margin: 1rem;
      padding: 1rem;
      flex-direction: column;
      text-align: center;
    }

    .search-section {
      padding: 0 1rem;
    }

    .search-container {
      padding: 1.5rem;
    }

    .articles-grid {
      grid-template-columns: 1fr;
    }

    .article-footer {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;
    }

    .resources-grid {
      grid-template-columns: 1fr;
    }

    .contribute-prompt {
      padding: 2rem 1.5rem;
    }

    .contribute-button {
      width: 100%;
      justify-content: center;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.75rem;
    }

    .no-articles-title {
      font-size: 1.75rem;
    }

    .tag-filters {
      justify-content: center;
    }
  }
</style>
