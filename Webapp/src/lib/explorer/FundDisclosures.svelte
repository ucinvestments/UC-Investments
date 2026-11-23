<script lang="ts">
  import { formatSourceDate } from "./holdings";
  import type { FundDisclosure, Source } from "./holdings";

  let {
    disclosures,
    sources,
  }: {
    disclosures: FundDisclosure[];
    sources: Record<string, Source>;
  } = $props();
</script>

<h4>Supplemental UC disclosures</h4>
{#each disclosures as disclosure}
  {@const source = sources[disclosure.source]}
  {#if source}
    <details>
      <summary>{disclosure.title}</summary>
      <p>
        <a href={source.url}>{source.name}</a>
        as of {formatSourceDate(source.date)}.
      </p>
      <dl>
        {#each disclosure.metrics as metric (metric.label)}
          <div>
            <dt>{metric.label}</dt>
            <dd>{metric.value}</dd>
          </div>
        {/each}
      </dl>
    </details>
  {/if}
{/each}

<style>
  details {
    margin-top: 8px;
    padding: 8px 10px;
    border: 1px solid var(--rule);
    border-radius: 6px;
    font-size: 0.8rem;
  }
  summary {
    cursor: pointer;
    font-weight: 650;
  }
  p {
    margin-block: 6px 8px;
    color: var(--muted);
  }
  a {
    color: #2348a9;
    text-decoration: underline;
  }
  dl > div {
    display: flex;
    justify-content: space-between;
    gap: 6px;
    padding-block: 4px;
  }
  dl > div + div {
    border-top: 1px solid var(--rule);
  }
  dd {
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
</style>
