<script>
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";

  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  <div class="resources-container">
    <!-- Hero Section -->
    <div class="resources-hero" in:fade={{ duration: 800 }}>
      <div class="hero-content">
        <Icon icon="mdi:book-open-page-variant" class="hero-icon" />
        <h1 class="hero-title">Resources</h1>
        <p class="hero-subtitle">
          Official reports, documentation, and critical analysis of UC
          investments
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- UC Official Resources Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 200 }}
      >
        <div class="section-header">
          <Icon icon="mdi:school" class="section-icon" />
          <h2 class="section-title">Official UC Resources</h2>
        </div>

        <div class="resources-grid">
          <!-- Main Website -->
          <div class="resource-card">
            <div class="resource-header">
              <Icon icon="mdi:web" class="resource-icon" />
              <h3>UC Investment Office</h3>
            </div>
            <p class="resource-description">
              The official website of the University of California's Investment
              Office.
            </p>
            <a
              href="https://www.ucop.edu/investment-office/index.html"
              target="_blank"
              rel="noopener noreferrer"
              class="resource-link"
            >
              <span>Visit Official Website</span>
              <Icon icon="mdi:arrow-right" class="link-arrow" />
            </a>
          </div>

          <!-- Annual Report -->
          <div class="resource-card">
            <div class="resource-header">
              <Icon icon="mdi:file-chart" class="resource-icon" />
              <h3>2023-2024 Annual Report</h3>
            </div>
            <p class="resource-description">
              Comprehensive annual report detailing the UC's investment
              performance, asset allocation, and financial strategies for the
              fiscal year.
            </p>
            <a
              href="https://www.ucop.edu/investment-office/annual-report-240923_ucar24_final.pdf"
              target="_blank"
              rel="noopener noreferrer"
              class="resource-link"
            >
              <span>View Annual Report (PDF)</span>
              <Icon icon="mdi:arrow-right" class="link-arrow" />
            </a>
          </div>

          <!-- Investment Philosophy -->
          <div class="resource-card">
            <div class="resource-header">
              <Icon icon="mdi:lightbulb-on" class="resource-icon" />
              <h3>Investment Philosophy</h3>
            </div>
            <p class="resource-description">
              The 10 pillars guiding UC's investment strategy, including their
              approach to risk management, asset allocation, and long-term value
              creation. It's a slideshow very quick read.
            </p>
            <a
              href="https://www.ucop.edu/investment-office/10pillarspowerpoint-1.pdf"
              target="_blank"
              rel="noopener noreferrer"
              class="resource-link"
            >
              <span>View 10 Pillars (PDF)</span>
              <Icon icon="mdi:arrow-right" class="link-arrow" />
            </a>
          </div>
        </div>
      </section>

      <!-- Critical Analysis Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 400 }}
      >
        <div class="section-header">
          <Icon icon="mdi:magnify-scan" class="section-icon" />
          <h2 class="section-title">Critical Analysis</h2>
        </div>

        <div class="analysis-card">
          <div class="analysis-header">
            <Icon icon="mdi:file-document-outline" class="analysis-icon" />
            <div>
              <h3>Unmasking UCLA Whitepaper</h3>
              <span class="analysis-source">by Unmasking UCLA</span>
            </div>
          </div>
          <p class="analysis-description">
            An in-depth critical examination of UC's investment practices by our
            friends over at UCLA. The paper focuses on ethical concerns,
            transparency issues, and the impact of investment decisions on
            campus communities and if it is alignmened with humananity.
          </p>
          <div class="analysis-highlights">
            <div class="highlight">
              <Icon icon="mdi:world" class="highlight-icon" />
              <span>Ethical Critque</span>
            </div>
            <div class="highlight">
              <Icon icon="mdi:eye" class="highlight-icon" />
              <span>Transparency Issues</span>
            </div>
            <div class="highlight">
              <Icon icon="mdi:leaf" class="highlight-icon" />
              <span>Sustainability Impact</span>
            </div>
          </div>
          <a
            href="https://unmaskingucla.org/whitepaper"
            target="_blank"
            rel="noopener noreferrer"
            class="analysis-link"
          >
            <span>Read the Full Whitepaper</span>
            <Icon icon="mdi:arrow-right" class="link-arrow" />
          </a>
        </div>
      </section>

      <!-- Additional Resources Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 600 }}
      >
        <div class="section-header">
          <Icon icon="mdi:link-variant" class="section-icon" />
          <h2 class="section-title">Related Links</h2>
        </div>

        <div class="content-card">
          <div class="related-links">
            <div class="link-item">
              <Icon icon="mdi:chart-pie" class="link-icon" />
              <div>
                <a href="/" class="related-link">Investment Explorer</a>
                <p class="link-description">
                  Interactive visualization of UC investment data
                </p>
              </div>
            </div>
            <div class="link-item">
              <Icon icon="mdi:information" class="link-icon" />
              <div>
                <a href="/about" class="related-link">Methodology</a>
                <p class="link-description">
                  Learn about our data collection and analysis process
                </p>
              </div>
            </div>
            <div class="link-item">
              <Icon icon="mdi:github" class="link-icon" />
              <div>
                <a
                  href="https://github.com/TheArctesian/UC-Investments"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="related-link"
                >
                  GitHub Repository
                  <Icon icon="mdi:open-in-new" class="external-indicator" />
                </a>
                <p class="link-description">
                  Access raw data and contribute to the project
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  .resources-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }

  .resources-hero {
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .resources-hero::before {
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

  .content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }

  .content-section {
    margin-bottom: 4rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  :global(.section-icon) {
    font-size: 2rem;
    color: var(--founder);
  }

  .section-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0;
    letter-spacing: -0.01em;
  }

  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }

  .resource-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
  }

  .resource-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .resource-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  :global(.resource-icon) {
    font-size: 2rem;
    color: var(--sec);
  }

  .resource-card h3 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.375rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .resource-description {
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 1.5rem;
    flex-grow: 1;
  }

  .resource-link {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.875rem 1.25rem;
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    text-decoration: none;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .resource-link:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow-md);
  }

  :global(.link-arrow) {
    font-size: 1.25rem;
    transition: transform 0.3s ease;
  }

  .resource-link:hover :global(.link-arrow) {
    transform: translateX(4px);
  }

  .analysis-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    box-shadow: var(--shadow-md);
  }

  .analysis-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  :global(.analysis-icon) {
    font-size: 2.5rem;
    color: var(--golden-gate);
  }

  .analysis-header h3 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .analysis-source {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
    display: block;
  }

  .analysis-description {
    color: var(--text-primary);
    line-height: 1.8;
    margin-bottom: 2rem;
    font-size: 1.0625rem;
  }

  .analysis-highlights {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
  }

  .highlight {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--bg-secondary);
    border-radius: 2rem;
    border: 1px solid var(--border);
  }

  :global(.highlight-icon) {
    font-size: 1.125rem;
    color: var(--founder);
  }

  .highlight span {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
  }

  .analysis-link {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, var(--golden-gate), var(--founder));
    color: white;
    text-decoration: none;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
    width: 100%;
  }

  .analysis-link:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .content-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    box-shadow: var(--shadow-md);
  }

  .related-links {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .link-item {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
  }

  :global(.link-icon) {
    font-size: 1.75rem;
    color: var(--founder);
    margin-top: 0.125rem;
  }

  .related-link {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
  }

  .related-link:hover {
    color: var(--founder);
    transform: translateX(4px);
  }

  :global(.external-indicator) {
    font-size: 0.875rem;
  }

  .link-description {
    margin: 0.25rem 0 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .resources-hero {
      padding: 2rem 1rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .hero-subtitle {
      font-size: 1rem;
    }

    .content-wrapper {
      padding: 2rem 1rem;
    }

    .section-title {
      font-size: 1.5rem;
    }

    .resources-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .resource-card,
    .analysis-card,
    .content-card {
      padding: 1.5rem;
    }

    .analysis-highlights {
      flex-direction: column;
    }

    .highlight {
      width: fit-content;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.75rem;
    }

    .analysis-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }

    .link-item {
      flex-direction: column;
      gap: 0.75rem;
    }
  }
</style>
