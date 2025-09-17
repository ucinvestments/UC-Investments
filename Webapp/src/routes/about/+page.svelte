<script>
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";
  import Hero from "$lib/components/Hero.svelte";
  import Section from "$lib/components/Section.svelte";
  import Card from "$lib/components/Card.svelte";
  import Container from "$lib/components/Container.svelte";
  import PageLayout from "$lib/components/PageLayout.svelte";
  import Button from "$lib/components/Button.svelte";
  import { formatCurrency } from "$lib/utils/formatters";

  let mounted = false;

  const financialData = [
    { value: 162e9, label: "Total UC Portfolio" },
    { value: 89e9, label: "UCRP Holdings" },
    { value: 23e9, label: "Endowment Fund" },
    { value: 55e9, label: "Short-term & Retirement" }
  ];

  const teamMembers = [
    {
      name: "Alex Forman",
      icon: "mdi:chart-bar",
      link: "https://www.linkedin.com/in/alex-k-forman/",
      linkIcon: "mdi:linkedin",
      linkText: "LinkedIn Profile"
    },
    {
      name: "Stephen Okita",
      icon: "mdi:web",
      link: "https://stephenokita.com/",
      linkIcon: "mdi:web",
      linkText: "Website"
    }
  ];

  const cryptoAddresses = [
    {
      name: "Ethereum (ETH)",
      icon: "cryptocurrency:eth",
      address: "0x623c7559ddC51BAf15Cc81bf5bc13c0B0EA14c01",
      color: "#627eea"
    },
    {
      name: "Monero (XMR)",
      icon: "cryptocurrency:xmr",
      address: "44bvXALNkxUgSkGChKQPnj79v6JwkeYEkGijgKyp2zRq3EiuL6oewAv5u2c7FN7jbN1z7uj1rrPfL77bbsJ3cC8U2ADFoTj",
      color: "#ff6600"
    }
  ];

  function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      const button = event.target.closest('.copy-button');
      const originalHTML = button.innerHTML;
      button.innerHTML = '<span style="color: #10b981;">✓</span>';
      setTimeout(() => {
        button.innerHTML = originalHTML;
      }, 2000);
    });
  }

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  <PageLayout>
    <Hero
      icon="mdi:information-outline"
      title="About UC Investment Explorer"
      subtitle="Transparency in university endowment management through data-driven analysis"
    />

    <Container>
      <Section title="Methodology" icon="mdi:chart-line" delay={200}>
        <Card>
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
        </Card>
      </Section>

      <Section title="UC Financial Structure" icon="mdi:bank" delay={400}>
        <Card>
          <p>
            Universities within the UC system maintain individual endowments,
            with the majority sourced from the GEP. UC Berkeley, for example,
            manages a $7.4B endowment: $2.9B under direct school control and
            $4.5B from the UC's $23B total endowment.
          </p>

          <div class="financial-breakdown">
            {#each financialData as item}
              <div class="breakdown-item">
                <div class="breakdown-value">{formatCurrency(item.value)}</div>
                <div class="breakdown-label">{item.label}</div>
              </div>
            {/each}
          </div>
        </Card>
      </Section>

      <Section title="Data Sources" icon="mdi:source-branch" delay={600}>
        <Card>
          <p>
            Our research began with UCRP and GEP holding documents from the UC's
            investment office. Fund-specific data was gathered from multiple
            sources as outlined in our methodology.
          </p>
          <div class="source-link">
            <Button
              href="https://github.com/TheArctesian/UC-Investments/tree/main/Data-Collection/csv-files"
              icon="mdi:github"
              external
            >
              View all data sources on GitHub
            </Button>
          </div>
        </Card>
      </Section>

      <Section title="Contribute" icon="mdi:hand-heart" delay={800}>
        <Card>
          <p>
            Help expand this research by contributing to data collection or
            development. Join our open-source project to improve transparency in
            university investments.
          </p>
          <div class="contribute-actions">
            <Button
              href="https://github.com/thearctesian/UC-Investments/"
              icon="mdi:github"
              external
            >
              View Repository
            </Button>
            <Button
              href="mailto:dev@ucinvestments.info"
              icon="mdi:email"
              variant="secondary"
            >
              Contact Team
            </Button>
          </div>
        </Card>
      </Section>

      <Section title="Who Made This" icon="mdi:account-group" delay={1000}>
        <Card>
          <p class="team-intro">
            This project emerged from conversations about divestment and
            investment transparency. We decided to figure out what we as a
            university were actually invested in and present that in the best
            way we knew how.
          </p>

          <div class="team-grid">
            {#each teamMembers as member}
              <div class="team-member">
                <Icon icon={member.icon} class="member-icon" />
                <h3>{member.name}</h3>
                <a
                  href={member.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="member-link"
                >
                  <Icon icon={member.linkIcon} class="social-icon" />
                  {member.linkText}
                </a>
              </div>
            {/each}
          </div>
        </Card>
      </Section>

      <Section title="Support This Project" icon="mdi:heart" delay={1200}>
        <Card>
          <p class="support-intro">
            This project is currently self-funded by Stephen. He would love any monetary help to cover hosting costs, API fees, and development resources. Every contribution helps maintain transparency in UC investments.
          </p>

          <div class="donation-section">
            <h3 class="donation-title">Crypto Donations</h3>

            <div class="crypto-options">
              {#each cryptoAddresses as crypto}
                <div class="crypto-option">
                  <div class="crypto-header">
                    <Icon icon={crypto.icon} class="crypto-icon" style="color: {crypto.color}" />
                    <strong>{crypto.name}</strong>
                  </div>
                  <div class="address-container">
                    <code class="crypto-address">{crypto.address}</code>
                    <button
                      class="copy-button"
                      on:click={() => copyToClipboard(crypto.address)}
                      aria-label="Copy {crypto.name} address"
                    >
                      <Icon icon="mdi:content-copy" />
                    </button>
                  </div>
                </div>
              {/each}
            </div>

            <div class="alternative-donation">
              <Icon icon="mdi:email" class="email-icon" />
              <p>
                For alternative donation options, contact Stephen directly at
                <a href="mailto:sdokita@berkeley.edu">sdokita@berkeley.edu</a>
              </p>
            </div>

            <div class="usage-note">
              <Icon icon="mdi:information" class="info-icon" />
              <p>
                <strong>How donations are used:</strong> Hosting infrastructure, API costs, domain fees, and development tools that keep this platform running and data current.
              </p>
            </div>
          </div>
        </Card>
      </Section>
    </Container>
  </PageLayout>
{/if}

<style>
  /* Styles specific to About page - leveraging reusable components */

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

  .source-link {
    margin-top: 1rem;
  }

  .contribute-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
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

  :global(.social-icon) {
    font-size: 1.125rem;
  }

  /* Support Section Styles */
  .support-intro {
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: var(--text-primary);
  }

  .donation-section {
    background: var(--bg);
    border-radius: 1rem;
    padding: 2rem;
    border: 1px solid var(--border);
  }

  .donation-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--pri);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .crypto-options {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .crypto-option {
    background: white;
    border-radius: 0.75rem;
    padding: 1.5rem;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
  }

  .crypto-option:hover {
    box-shadow: var(--shadow-sm);
  }

  .crypto-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  :global(.crypto-icon) {
    font-size: 1.5rem;
  }

  .crypto-header strong {
    font-size: 1rem;
    color: var(--pri);
  }

  .address-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--bg-secondary);
    padding: 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid var(--border);
  }

  .crypto-address {
    flex: 1;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.8rem;
    word-break: break-all;
    color: var(--text-primary);
    background: none;
    user-select: all;
    cursor: text;
  }

  .copy-button {
    background: var(--founder);
    color: white;
    border: none;
    padding: 0.5rem;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 2rem;
    height: 2rem;
  }

  .copy-button:hover {
    background: var(--pri);
    transform: scale(1.05);
  }

  .alternative-donation {
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 0.75rem;
    padding: 1.5rem;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  :global(.email-icon) {
    font-size: 1.5rem;
    color: var(--founder);
    flex-shrink: 0;
  }

  .alternative-donation p {
    margin: 0;
    color: var(--text-secondary);
  }

  .usage-note {
    background: linear-gradient(135deg, var(--sec), var(--founder));
    color: white;
    border-radius: 0.75rem;
    padding: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
  }

  :global(.info-icon) {
    font-size: 1.5rem;
    color: white;
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .usage-note p {
    margin: 0;
    line-height: 1.6;
  }

  .usage-note strong {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .methodology-grid {
      grid-template-columns: 1fr;
    }

    .financial-breakdown {
      grid-template-columns: repeat(2, 1fr);
    }

    .contribute-actions {
      flex-direction: column;
    }
  }

  @media (max-width: 480px) {
    .financial-breakdown {
      grid-template-columns: 1fr;
    }

    .team-grid {
      grid-template-columns: 1fr;
    }

    .crypto-address {
      font-size: 0.7rem;
    }

    .donation-section {
      padding: 1.5rem;
    }

    .crypto-option {
      padding: 1rem;
    }

    .alternative-donation,
    .usage-note {
      padding: 1rem;
    }
  }
</style>