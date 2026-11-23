export type View = "company" | "fund" | "asset" | "reported";

type Allocation = { name: string; amount: number; source?: string };
export type Holding = {
  name: string;
  amount: number;
  basis?: "estimate" | "reported";
  category?: string;
  allocations: Allocation[];
  funds?: string[];
  disclosures?: FundDisclosure[];
  lookThrough?: Source & {
    ticker: string;
    estimates?: { name: string; ticker: string; amount: number }[];
  };
};

export type FundDisclosure = {
  source: string;
  title: string;
  name: string;
  metrics: { label: string; value: string }[];
};

export type Source = { name: string; date: string; url: string };
export type HoldingsSnapshot = {
  schemaVersion: 1;
  checkedAt: string;
  disclosures: Record<string, Source & { amount: number }>;
  proxies: Record<string, Source & { method: string; filed?: string }>;
  privateMarkets?: Record<string, Source>;
  regents: Source & { filed: string };
  coverage: { total: number; assigned: number };
  funds: Holding[];
  assetClasses: Holding[];
  companies: { grouped: Holding[]; separate: Holding[] };
  reported: Holding[];
};

export const views = {
  company: {
    label: "Companies",
    singular: "Company",
    description:
      "Explore estimates derived from fund allocations and proxy holdings.",
  },
  fund: {
    label: "Funds",
    singular: "Fund",
    description: "See the amounts reported by the pension and endowment pools.",
  },
  reported: {
    label: "Regents 13F",
    singular: "Security",
    description:
      "See securities reported in the Regents’ latest Form 13F. These amounts are shown separately from the pension and endowment figures.",
  },
  asset: {
    label: "Asset classes",
    singular: "Asset class",
    description:
      "See how the disclosed holdings are distributed across asset classes.",
  },
} satisfies Record<
  View,
  { label: string; singular: string; description: string }
>;

const short = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  notation: "compact",
  maximumFractionDigits: 2,
});
const dollars = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});
const percent = new Intl.NumberFormat("en-US", {
  style: "percent",
  maximumFractionDigits: 1,
});

export const formatCompact = (amount: number) => short.format(amount);
export const formatDollars = (amount: number) => dollars.format(amount);
export const formatShare = (amount: number, total: number) =>
  total > 0 ? percent.format(amount / total) : "—";
export const sumHoldings = (holdings: Holding[]) =>
  holdings.reduce((sum, holding) => sum + holding.amount, 0);

const date = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric",
  timeZone: "UTC",
});
export const formatSourceDate = (value: string) => date.format(new Date(value));

export async function loadSnapshot(): Promise<HoldingsSnapshot> {
  const response = await fetch("/data/holdings-snapshot.json", {
    cache: "no-cache",
  });
  if (!response.ok) throw new Error("Could not load holdings snapshot");
  const snapshot: HoldingsSnapshot = await response.json();
  if (snapshot.schemaVersion !== 1)
    throw new Error("Unsupported holdings snapshot");

  for (const variant of [
    snapshot.companies.grouped,
    snapshot.companies.separate,
  ]) {
    for (const holding of variant) {
      holding.name = holding.name.replace(/\b\w/g, (letter) =>
        letter.toUpperCase(),
      );
    }
  }
  return snapshot;
}
