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
  <div class="about-container">
    <!-- Hero Section -->
    <div class="about-hero" in:fade={{ duration: 800 }}>
      <div class="hero-content">
        <Icon icon="mdi:information-outline" class="hero-icon" />
        <h1 class="hero-title">About UC Investment Explorer</h1>
        <p class="hero-subtitle">
          Transparency in university endowment management through data-driven
          analysis
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Methodology Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 200 }}
      >
        <div class="section-header">
          <Icon icon="mdi:chart-line" class="section-icon" />
          <h2 class="section-title">Methodology</h2>
        </div>

        <div class="content-card">
          <p class="section-intro">
            We have analyzed <strong>$108 billion</strong> of the UC's total
            investment portfolio. Within this, we were able to analyze the
            composition of funds totaling approximately <strong>$49B</strong>.
            The majority of these funds are stored in the UC Retirement Plan
            (UCRP) at $89.2B and the General Endowment Pool (GEP) at $20.7B.
          </p>

          <div class="methodology-grid">
            <div class="method-card">
              <div class="method-header">
                <Icon icon="mdi:database" class="method-icon" />
                <h3>Direct Data Usage</h3>
              </div>
              <p>
                When funds release their full composition data, we use this
                information directly for our analysis.
              </p>
            </div>

            <div class="method-card">
              <div class="method-header">
                <Icon icon="mdi:calculator" class="method-icon" />
                <h3>Re-weighting Analysis</h3>
              </div>
              <p>
                For funds like our $35B MSCI investment that only publish top 10
                holdings (18% of total), we reconstruct data by analyzing
                similar funds and applying exclusion filters for tobacco and
                fossil fuel companies.
              </p>
            </div>

            <div class="method-card">
              <div class="method-header">
                <Icon icon="mdi:file-document" class="method-icon" />
                <h3>SEC Filings</h3>
              </div>
              <p>
                For direct hedge fund investments, we utilize SEC forms 13F,
                13D, and G obtained from sources like
                <a
                  href="https://whalewisdom.com"
                  target="_blank"
                  rel="noopener noreferrer">whalewisdom.com</a
                >.
              </p>
            </div>
          </div>

          <div class="note-card">
            <Icon icon="mdi:alert-circle" class="note-icon" />
            <p>
              Some assets remain unanalyzed, particularly foreign hedge funds
              not required to file with the SEC or publish holdings data.
            </p>
          </div>
        </div>
      </section>

      <!-- Financial Structure Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 400 }}
      >
        <div class="section-header">
          <Icon icon="mdi:bank" class="section-icon" />
          <h2 class="section-title">UC Financial Structure</h2>
        </div>

        <div class="content-card">
          <p>
            Universities within the UC system maintain individual endowments,
            with the majority sourced from the GEP. UC Berkeley, for example,
            manages a $7.4B endowment: $2.9B under direct school control and
            $4.5B from the UC's $23B total endowment.
          </p>

          <div class="financial-breakdown">
            <div class="breakdown-item">
              <div class="breakdown-value">$162B</div>
              <div class="breakdown-label">Total UC Portfolio</div>
            </div>
            <div class="breakdown-item">
              <div class="breakdown-value">$89B</div>
              <div class="breakdown-label">UCRP Holdings</div>
            </div>
            <div class="breakdown-item">
              <div class="breakdown-value">$23B</div>
              <div class="breakdown-label">Endowment Fund</div>
            </div>
            <div class="breakdown-item">
              <div class="breakdown-value">$55B</div>
              <div class="breakdown-label">Short-term & Retirement</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sources Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 600 }}
      >
        <div class="section-header">
          <Icon icon="mdi:source-branch" class="section-icon" />
          <h2 class="section-title">Data Sources</h2>
        </div>

        <div class="content-card">
          <p>
            Our research began with UCRP and GEP holding documents from the UC's
            investment office. Fund-specific data was gathered from multiple
            sources as outlined in our methodology.
          </p>
          <div class="source-link">
            <Icon icon="mdi:github" class="link-icon" />
            <a
              href="https://github.com/TheArctesian/UC-Investments/tree/main/Data-Collection/csv-files"
              target="_blank"
              rel="noopener noreferrer"
            >
              View all data sources on GitHub
            </a>
          </div>
        </div>
      </section>

      <!-- Contribute Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 800 }}
      >
        <div class="section-header">
          <Icon icon="mdi:hand-heart" class="section-icon" />
          <h2 class="section-title">Contribute</h2>
        </div>

        <div class="content-card">
          <p>
            Help expand this research by contributing to data collection or
            development. Join our open-source project to improve transparency in
            university investments.
          </p>
          <div class="contribute-actions">
            <a
              href="https://github.com/thearctesian/UC-Investments/"
              target="_blank"
              rel="noopener noreferrer"
              class="action-button"
            >
              <Icon icon="mdi:github" class="button-icon" />
              View Repository
            </a>
            <a
              href="mailto:sdokita@berkeley.edu"
              class="action-button secondary"
            >
              <Icon icon="mdi:email" class="button-icon" />
              Contact Team
            </a>
          </div>
        </div>
      </section>

      <!-- About Team Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 1000 }}
      >
        <div class="section-header">
          <Icon icon="mdi:account-group" class="section-icon" />
          <h2 class="section-title">Who Made This</h2>
        </div>

        <div class="content-card">
          <p class="team-intro">
            This project emerged from conversations about divestment and
            investment transparency. We decided to figure out what we as a
            university were actually invested in and present that in the best
            way we knew how.
          </p>

          <div class="team-grid">
            <div class="team-member">
              <Icon icon="mdi:chart-bar" class="member-icon" />
              <h3>Alex Forman</h3>
              <a
                href="https://www.linkedin.com/in/alex-k-forman/"
                target="_blank"
                rel="noopener noreferrer"
                class="member-link"
              >
                <Icon icon="mdi:linkedin" class="social-icon" />
                LinkedIn Profile
              </a>
            </div>

            <div class="team-member">
              <Icon icon="mdi:web" class="member-icon" />
              <h3>Stephen Okita</h3>
              <a
                href="https://stephenokita.com/"
                target="_blank"
                rel="noopener noreferrer"
                class="member-link"
              >
                <Icon icon="mdi:web" class="social-icon" />
                Website
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  .about-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }

  .about-hero {
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .about-hero::before {
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

  .content-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    box-shadow: var(--shadow-md);
  }

  .section-intro {
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: var(--text-primary);
  }

  .methodology-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .method-card {
    background: var(--bg-secondary);
    border-radius: 1rem;
    padding: 1.5rem;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
  }

  .method-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .method-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  :global(.method-icon) {
    font-size: 1.5rem;
    color: var(--founder);
  }

  .method-card h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .method-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
  }

  .note-card {
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1rem;
    padding: 1.5rem;
    border: 1px solid var(--border);
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  :global(.note-icon) {
    font-size: 1.5rem;
    color: var(--golden-gate);
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .financial-breakdown {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .breakdown-item {
    text-align: center;
    padding: 1.5rem;
    background: var(--bg);
    border-radius: 1rem;
    border: 1px solid var(--border);
  }

  .breakdown-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--founder);
    margin-bottom: 0.5rem;
  }

  .breakdown-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
  }

  .source-link,
  .member-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  :global(.link-icon, .social-icon) {
    font-size: 1.25rem;
    color: var(--founder);
  }

  .contribute-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
  }

  .action-button {
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

  .action-button.secondary {
    background: white;
    color: var(--pri);
    border: 2px solid var(--border);
  }

  .action-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  :global(.button-icon) {
    font-size: 1.125rem;
  }

  .team-intro {
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: var(--text-primary);
  }

  .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
  }

  .team-member {
    text-align: center;
    padding: 2rem;
    background: var(--bg);
    border-radius: 1rem;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
  }

  .team-member:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  :global(.member-icon) {
    font-size: 2.5rem;
    color: var(--sec);
    margin-bottom: 1rem;
  }

  .team-member h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--pri);
    margin-bottom: 0.5rem;
  }

  .member-role {
    color: var(--text-secondary);
    margin-bottom: 1rem;
    font-size: 0.925rem;
  }

  .member-link {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    color: var(--founder);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .member-link:hover {
    color: var(--pri);
  }

  /* Global link styling */
  :global(a) {
    color: var(--founder);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    border-bottom: 1px solid transparent;
  }

  :global(a:hover) {
    color: var(--pri);
    border-bottom-color: var(--pri);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .about-hero {
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

    .content-card {
      padding: 1.5rem;
    }

    .methodology-grid {
      grid-template-columns: 1fr;
    }

    .financial-breakdown {
      grid-template-columns: repeat(2, 1fr);
    }

    .contribute-actions {
      flex-direction: column;
    }

    .action-button {
      justify-content: center;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.75rem;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .financial-breakdown {
      grid-template-columns: 1fr;
    }

    .team-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
