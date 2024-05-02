<div>
	<h2>Methodology</h2>
	<p>
	Currently, we have analyzed $108 billion of the UC's total investment portfolio. A majority of these funds are stored in the UC Retirement Plan (UCRP) ($89.2B) and in the General Endowment Pool (GEP) ($20.7B). Although these investments are spread across a wide variety of assets, the motivation of this research was to figure out which companies the UC was directly or indirectly funding. Nearly all of the UC's money that goes to companies happens indirectly, through the use of investing in index funds, public equity funds, and private hedge funds.
	</p>
	<p>
	Some of these funds publish full composition data, but most do not. For example, our largest investment, in a fund managed by MSCI, only publishes its top 10 holdings, which only explains where 18% of this money goes. To attempt to get this data, we employed three main strategies to provide accurate estimates:
	</p>
	<ul>
	<li>
		Using provided data:
		<ul>
		<li>In the instance that a fund released its composition, we simply use this data.</li>
		</ul>
	</li>
	<li>
		Reconstructing data through re-weighting:
		<ul>
		<li>
			Some of our largest investments, such as our $35B investment in the MSCI ACWI IMI TF EX‐TOB AND FF fund, only release its top 10 holdings. They do, however, release the full composition of the non-ex-tobacco/ex-fossil fuel version of this fund (MSCI ACWI IMI). With this composition data, we conduct a re-weighting procedure.
		</li>
		<li>
			We first go through every company that this fund is invested in, then check it against a list of fossil fuel and tobacco companies, and remove those assets. This gives us a rough estimate of the composition of the specific fund the UC is invested in. 
		</li>
		<li>
			After this, we distribute the missing weight across all companies that remained post-pruning, proportional to their original investment weights.
		</li>
		<li>
			This isn't a perfect system but is currently our best method for estimating what these specific funds are comprised of.
		</li>
		</ul>
	</li>
	<li>
		Using SEC filings:
		<ul>
		<li>
			In the case of direct investments we have in hedge funds, we use a combination of SEC forms 13F, 13D, and G to discover their holdings. This data is obtained from sites such as whalewisdom.com.
		</li>
		</ul>
	</li>
	</ul>
	<p>
	For some assets though, we gain little to no data. This is especially true with investments in foreign hedge funds that are not required to file anything with the SEC or publish any of their holdings.
	</p>
	<p>
	Once we've determined the holdings of the funds that we're invested in, we multiply the weight of each company in each individual fund, and then multiply this by the total amount that we invest in that asset, thus determining how much money is indirectly going to such a company.
	</p>
	<p>
	Across all of the individual fund composition datasets, companies are often spelled slightly differently, usually due to abbreviations. We group the same company across different funds through a process of standardizing the used abbreviations, and then use a fuzzing match process to group investments. Funds also invest in different classes of each stock, and when listed, we differentiate these holdings unless you click "combine stock classes."
	</p>

	<h2>UC Finical Structuring Explained</h2>
	<h2>Sources</h2>
	<h2>Contribute</h2>
	<h2>About</h2>
	</div>

<style>
	div {
		padding-left: 2rem;
		padding-right: 2rem;
	}
	h1 {
		color: var(--pri);
		font-size: 5vw;
	}
	h2 {
		color: var(--pri);
		font-size: 3vw;
	}
	p {
		margin-top: 1rem;
	}
	h3 {
		margin-top: 1rem;
		font-size: 2vw;
		color: var(--sec);
		text-decoration-line: underline;
	}
	li {
		margin-left: 1rem;
	}
	a {
		color: var(--sec);
		text-decoration-line: underline;
	}
	@media (max-width: 580px) {
		h1 {
			font-size: 10vw;
		}
		h2 {
			font-size: 5vw;
		}
		p {
			font-size: 4vw;
		}
		h3 {
			font-size: 5vw;
		}
		h4 {
			font-size: 4.5vw;
		}
	}
</style>