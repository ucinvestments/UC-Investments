<script>
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";
  import Hero from "$lib/components/Hero.svelte";
  import Section from "$lib/components/Section.svelte";
  import Card from "$lib/components/Card.svelte";
  import Container from "$lib/components/Container.svelte";
  import PageLayout from "$lib/components/PageLayout.svelte";
  import Button from "$lib/components/Button.svelte";

  let mounted = false;

  const officialResources = [
    {
      title: "UC Investment Office",
      description:
        "The official website of the University of California's Investment Office.",
      icon: "mdi:web",
      href: "https://www.ucop.edu/investment-office/index.html",
    },
    {
      title: "2023-2024 Annual Report",
      description:
        "Comprehensive annual report detailing the UC's investment performance, asset allocation, and financial strategies for the fiscal year.",
      icon: "mdi:file-chart",
      href: "https://www.ucop.edu/investment-office/annual-report-240923_ucar24_final.pdf",
    },
    {
      title: "Investment Philosophy",
      description:
        "The 10 pillars guiding UC's investment strategy, including their approach to risk management, asset allocation, and long-term value creation. It's a slideshow very quick read.",
      icon: "mdi:lightbulb-on",
      href: "https://www.ucop.edu/investment-office/10pillarspowerpoint-1.pdf",
    },
    {
      title: "SEC 13F Filings",
      description:
        "Quarterly SEC Form 13F-HR filings showing UC's institutional investment holdings. These regulatory filings provide detailed disclosure of equity positions managed by the UC.",
      icon: "mdi:file-document-multiple",
      href: "https://www.sec.gov/edgar/search/#/ciks=0000315054&entityName=REGENTS%2520OF%2520THE%2520UNIVERSITY%2520OF%2520CALIFORNIA%2520(CIK%25200000315054)&filter_forms=13F-HR",
    },
    {
      title: "ASUC Berkeley BDS Bill",
      source: "Research Document",
      description:
        "The policy enacted by the ASUC to revoke funding for companies on their own curated BDS list.",
      icon: "mdi:file-document-outline",
      href: "https://docs.google.com/document/d/1Sp4ezAig7xX7Ti-Aq70N2Bmh2gYiIi7MFZH_wbGVoAY/edit?tab=t.0",
      highlights: [
        { icon: "mdi:school", text: "UC System" },
        { icon: "mdi:account-group", text: "Student Government" },
        { icon: "mdi:gavel", text: "Legislation" },
      ],
    },
  ];

  const criticalAnalysis = [
    {
      title: "Unmasking UCLA Whitepaper",
      source: "by Unmasking UCLA",
      description:
        "An in-depth critical examination of UC's investment practices by our friends over at UCLA. It clearly explains what the UC is invested in and what our money funds.",
      icon: "mdi:file-document-outline",
      href: "https://unmaskingucla.org/whitepaper",
      highlights: [
        { icon: "mdi:world", text: "Ethical Critique" },
        { icon: "mdi:eye", text: "Transparency Issues" },
        { icon: "mdi:leaf", text: "Sustainability Impact" },
      ],
    },
    {
      title: "Who Rules the UC",
      source: "by BDS Exploratory Committee at UC Berkeley",
      description:
        "A comprehensive analysis examining the power structures and decision-making processes within the UC system. This paper explores the relationships between UC governance, UC investments, and the economic/political influences on university policy.",
      icon: "mdi:account-group-outline",
      href: "https://docs.google.com/document/d/1-6ElQ_yAAXaDA7arZTqvXOQJWOTd-1gDDBPxMnwWT2c/edit?tab=t.0#heading=h.698vkyeikquj",
      highlights: [
        { icon: "mdi:sitemap", text: "Governance Structure" },
        { icon: "mdi:handshake", text: "Power Dynamics" },
        { icon: "mdi:scale-balance", text: "Decision Making" },
      ],
    },
    {
      title:
        '"This is How We Win": Lessons from the Bay\'s Pro-Palestine Encampments',
      source: "by Bay Area Current",
      description:
        "An insightful article examining the pro-Palestine encampment movements across Bay Area universities, including UC campuses. The piece analyzes the strategies, successes, and lessons learned from these student-led protests, providing context for understanding campus activism and its relationship to university policies including divestment demands.",
      icon: "mdi:newspaper",
      href: "https://bayareacurrent.com/this-is-how-we-win-lessons-from-the-bays-pro-palestine-encampments/",
      highlights: [
        { icon: "mdi:account-group", text: "Student Activism" },
        { icon: "mdi:school", text: "UC Campuses" },
        { icon: "mdi:strategy", text: "Movement Strategy" },
      ],
    },
    {
      title: "Public Cost of UC Workers' Frontline Housing Crisis",
      source:
        "American Federation of State, County, and Municipal Workers Local 3299",
      description:
        "A brief report on the housing crisis among rank-and-file campus workers in the AFSCME 3299 union, which represents many custodial and maintenance workers across the University of California. The report illustrates the disparity in real wage increases for low- and high-level UC employees; the fact that the vast majority of AFSCME workers qualify for housing assistance; and the UC's holdings of over $9B in surplus developable land.",
      icon: "mdi:newspaper",
      href: "https://actionnetwork.org/user_files/user_files/000/110/931/original/Public_Cost_of_UC_Housing_Crisis_-_revised_pub_date.pdf",
      highlights: [
        { icon: "mdi:account-group", text: "Unions and Labor" },
        { icon: "mdi:school", text: "UC Campuses" },
      ],
    },
  ];

  const relatedLinks = [
    {
      title: "Investment Explorer",
      description: "Interactive visualization of UC investment data",
      icon: "mdi:chart-pie",
      href: "/",
    },
    {
      title: "Methodology",
      description: "Learn about our data collection and analysis process",
      icon: "mdi:information",
      href: "/about",
    },
    {
      title: "GitHub Repository",
      description: "Access raw data and contribute to the project",
      icon: "mdi:github",
      href: "https://github.com/TheArctesian/UC-Investments",
      external: true,
    },
  ];

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  <PageLayout>
    <Hero
      icon="mdi:book-open-page-variant"
      title="Resources"
      subtitle="Official reports, documentation, and critical analysis of UC investments"
    />

    <Container>
      <Section title="Official UC Resources" icon="mdi:school" delay={200}>
        <div class="resources-grid">
          {#each officialResources as resource}
            <Card hover padding="2rem">
              <div class="resource-header">
                <Icon icon={resource.icon} class="resource-icon" />
                <h3>{resource.title}</h3>
              </div>
              <p class="resource-description">{resource.description}</p>
              <Button href={resource.href} external>View Resource</Button>
            </Card>
          {/each}
        </div>
      </Section>

      <Section title="Critical Analysis" icon="mdi:magnify-scan" delay={400}>
        <div class="analysis-grid">
          {#each criticalAnalysis as analysis}
            <Card hover padding="2.5rem">
              <div class="analysis-header">
                <Icon icon={analysis.icon} class="analysis-icon" />
                <div>
                  <h3>{analysis.title}</h3>
                  <span class="analysis-source">{analysis.source}</span>
                </div>
              </div>
              <p class="analysis-description">{analysis.description}</p>

              <div class="analysis-highlights">
                {#each analysis.highlights as highlight}
                  <div class="highlight">
                    <Icon icon={highlight.icon} class="highlight-icon" />
                    <span>{highlight.text}</span>
                  </div>
                {/each}
              </div>

              <Button href={analysis.href} variant="accent" external>
                Read the Document
              </Button>
            </Card>
          {/each}
        </div>
      </Section>

      <Section title="Related Links" icon="mdi:link-variant" delay={600}>
        <Card>
          <div class="related-links">
            {#each relatedLinks as link}
              <div class="link-item">
                <Icon icon={link.icon} class="link-icon" />
                <div>
                  <Button
                    href={link.href}
                    variant="secondary"
                    external={link.external}
                  >
                    {link.title}
                  </Button>
                  <p class="link-description">{link.description}</p>
                </div>
              </div>
            {/each}
          </div>
        </Card>
      </Section>
    </Container>
  </PageLayout>
{/if}

<style>
  /* Component-specific styles for Resources page */

  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
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

  .resource-header h3 {
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

  .analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
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

  .link-description {
    margin: 0.25rem 0 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .resources-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .analysis-grid {
      grid-template-columns: 1fr;
    }

    .analysis-highlights {
      flex-direction: column;
    }

    .highlight {
      width: fit-content;
    }

    .link-item {
      flex-direction: column;
      gap: 0.75rem;
    }
  }

  @media (max-width: 480px) {
    .analysis-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }
</style>
